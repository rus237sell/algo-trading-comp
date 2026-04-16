"""
Round 1 - Naive Market Maker v1
================================
Products: ASH_COATED_OSMIUM, INTARIAN_PEPPER_ROOT
Position limit: 80 each

Strategy:
---------
INTARIAN_PEPPER_ROOT (steady):
  - Market-make around the mid-price with tight spread
  - Aggressively take any mispriced orders (buy below fair, sell above fair)
  - Fair value estimated from mid of best bid/ask

ASH_COATED_OSMIUM (volatile, hidden pattern):
  - Same market-making approach but wider spread
  - Track a simple moving average via traderData to detect trends
  - Lean into direction if trend is detected

Both products:
  - Respect position limit of 80
  - Take every profitable order in the book first, then place passive orders
"""

import json
from datamodel import OrderDepth, TradingState, Order
from typing import Dict, List, Any

POSITION_LIMIT = 80

PRODUCTS = ["ASH_COATED_OSMIUM", "INTARIAN_PEPPER_ROOT"]


class Trader:

    def run(self, state: TradingState) -> tuple:
        result: Dict[str, List[Order]] = {}
        conversions = 0

        # Load persistent state
        trader_state = {}
        if state.traderData and state.traderData != "":
            try:
                trader_state = json.loads(state.traderData)
            except:
                trader_state = {}

        for product in PRODUCTS:
            orders: List[Order] = []

            if product not in state.order_depths:
                result[product] = orders
                continue

            order_depth: OrderDepth = state.order_depths[product]
            position = state.position.get(product, 0)

            # Calculate fair value from mid-price
            fair_value = self.get_fair_value(order_depth, product, trader_state)

            if fair_value is None:
                result[product] = orders
                continue

            # Store price history for tracking
            history_key = f"{product}_prices"
            if history_key not in trader_state:
                trader_state[history_key] = []
            trader_state[history_key].append(fair_value)
            # Keep last 50 prices only
            trader_state[history_key] = trader_state[history_key][-50:]

            # STEP 1: Take any mispriced orders (aggressive fills)
            position, orders = self.take_mispriced_orders(
                product, order_depth, position, fair_value, orders
            )

            # STEP 2: Place passive market-making orders
            orders = self.place_passive_orders(
                product, position, fair_value, orders
            )

            result[product] = orders

        trader_data = json.dumps(trader_state)
        return result, conversions, trader_data

    def get_fair_value(self, order_depth: OrderDepth, product: str,
                       trader_state: dict) -> float:
        """Calculate fair value from the order book."""
        best_bid = max(order_depth.buy_orders.keys()) if order_depth.buy_orders else None
        best_ask = min(order_depth.sell_orders.keys()) if order_depth.sell_orders else None

        if best_bid is not None and best_ask is not None:
            mid = (best_bid + best_ask) / 2

            # For INTARIAN_PEPPER_ROOT, mid-price is a good estimate
            # For ASH_COATED_OSMIUM, we can use EMA from history for smoothing
            if product == "ASH_COATED_OSMIUM":
                history_key = f"{product}_prices"
                prices = trader_state.get(history_key, [])
                if len(prices) >= 5:
                    # Simple EMA with alpha=0.3
                    ema = prices[-1]
                    alpha = 0.3
                    for p in reversed(prices[-10:]):
                        ema = alpha * p + (1 - alpha) * ema
                    # Blend mid and EMA
                    return (mid + ema) / 2
            return mid

        elif best_bid is not None:
            return best_bid
        elif best_ask is not None:
            return best_ask
        return None

    def take_mispriced_orders(self, product: str, order_depth: OrderDepth,
                              position: int, fair_value: float,
                              orders: List[Order]) -> tuple:
        """
        Aggressively take orders that are mispriced relative to fair value.
        Buy anything offered below fair value, sell anything bid above fair value.
        """
        buy_room = POSITION_LIMIT - position
        sell_room = POSITION_LIMIT + position  # how much we can sell (go short)

        # Take cheap asks (buy below fair value)
        if order_depth.sell_orders:
            sorted_asks = sorted(order_depth.sell_orders.keys())
            for ask_price in sorted_asks:
                if ask_price < fair_value and buy_room > 0:
                    # sell_orders quantities are negative in the IMC framework
                    ask_vol = abs(order_depth.sell_orders[ask_price])
                    take_qty = min(ask_vol, buy_room)
                    orders.append(Order(product, ask_price, take_qty))
                    position += take_qty
                    buy_room -= take_qty

        # Take expensive bids (sell above fair value)
        if order_depth.buy_orders:
            sorted_bids = sorted(order_depth.buy_orders.keys(), reverse=True)
            for bid_price in sorted_bids:
                if bid_price > fair_value and sell_room > 0:
                    bid_vol = order_depth.buy_orders[bid_price]
                    take_qty = min(bid_vol, sell_room)
                    orders.append(Order(product, bid_price, -take_qty))
                    position -= take_qty
                    sell_room -= take_qty

        return position, orders

    def place_passive_orders(self, product: str, position: int,
                             fair_value: float, orders: List[Order]) -> List[Order]:
        """
        Place passive buy/sell orders around fair value to capture spread.
        """
        buy_room = POSITION_LIMIT - position
        sell_room = POSITION_LIMIT + position

        # Set spread based on product volatility
        if product == "INTARIAN_PEPPER_ROOT":
            spread = 1  # tight spread for steady product
        else:
            spread = 2  # wider spread for volatile product

        bid_price = int(round(fair_value)) - spread
        ask_price = int(round(fair_value)) + spread

        # Place passive buy order
        if buy_room > 0:
            passive_buy_qty = min(buy_room, 20)
            orders.append(Order(product, bid_price, passive_buy_qty))

        # Place passive sell order
        if sell_room > 0:
            passive_sell_qty = min(sell_room, 20)
            orders.append(Order(product, ask_price, -passive_sell_qty))

        return orders
