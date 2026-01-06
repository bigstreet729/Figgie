import random
import threading
from collections import defaultdict
from typing import Dict,List,Tuple

class Orderbook:

    def __init__(self):
        self.bids = {}
        self.asks = {}
        self.trades=[]
        self.lock=threading.Lock()
        self.__deck={}
        self.__common_suit=None
        self.__goal_suit=None

    def make_deck(self)->Dict[str,int]:

        suits = ['Spades','Hearts','Diamonds','Clubs']  
        random.shuffle(suits)
        self.__common_suit = suits[0]
        if(self.__common_suit=='Spades'):
            self.__goal_suit='Clubs'
        elif(self.__common_suit=='Clubs'):
            self.__goal_suit='Spades'
        elif(self.__common_suit=='Hearts'):
            self.goal_suit='Diamonds'
        elif(self.__common_suit=='Diamonds'):
            self.__goal_suit='Hearts'
        self.__deck[self.__common_suit]=12
        self.__deck[suits[1]]=10
        self.__deck[suits[2]]=10
        self.__deck[suits[3]]=8
        print("=== DECK CREATED ===")
        print(f"DECK COMPOSITION == {self.__deck}")
        return self.__deck

    def distribute_deck(self)->List[Dict[str,int]]:
        cards = []
        for suit,count in self.__deck.items():
            cards.extend([suit]*count)
        random.shuffle(cards)
        hands = []
        for i in range(4):
            hand = defaultdict(int)
            player_cards = cards[i*10:(i+1)*10]
            for card  in player_cards:
                hand[card]+=1
            for suit in ['Spades','Hearts','Diamonds','Clubs']:
                if suit not in hand:
                    hand[suit]=0
            hands.append(dict(hand))
        print("===DECK DISTRIBUTED===")
        for i,hand in enumerate(hands,1):
            print(f"Trader {i} hand:{hand}")
        print()
        return hands
    def add_order(self,suit:str,side:str,price:int,trader_id:int):
        with self.lock:
            order = (price,trader_id)
            if side == 'bid':
                if suit in self.asks:
                    ask_price,ask_trader=self.asks[suit]
                    if price>=ask_price:
                        trade_price = ask_price
                        trade = {'suit':suit,'price':trade_price,'buyer':trader_id,'seller':ask_trader}
                        self.trades.append(trade)
                        print(f"\n*** TRADE EXECUTED ***")
                        print(f"Suit: {suit} | Price: ${trade_price:.2f}")
                        print(f"Buyer: Trader {trader_id} | Seller: Trader {ask_trader}")
                        print("*********************\n")

                        del self.asks[suit]
                        return 
                if suit not in self.bids or price>self.bids[suit][0]:
                    self.bids[suit]=order
            else:
                if suit in self.bids:
                    bid_price,bid_trader=self.bids[suit]
                    if price<=bid_price:
                        trade_price = bid_price
                        trade = {'suit':suit,'price':trade_price,'buyer':bid_trader,'seller':trader_id}
                        self.trades.append(trade)
                        print(f"\n*** TRADE EXECUTED ***")
                        print(f"Suit: {suit} | Price: ${trade_price:.2f}")
                        print(f"Buyer: Trader {bid_trader} | Seller: Trader {trader_id}")
                        print("*********************\n")

                        del self.bids[suit]
                        return 
                if suit not in self.asks or price>self.asks[suit][0]:
                    self.asks[suit]=order

    def display_book(self):
        print("\n=== ORDER BOOK ===")
        for suit in ['Spades', 'Hearts', 'Diamonds', 'Clubs']:
            print(f"\n{suit}:")
            
            if suit in self.bids:
                print(f" Best Bid: ${self.bids[suit][0]:.2f}  (Trader {self.bids[suit][1]})")
            else:
                print(f" Best Bid: None")           
            if suit in self.asks:
                print(f" Best Ask: ${self.asks[suit][0]:.2f}  (Trader {self.asks[suit][1]})")
            else:
                print(f" Best Ask: None")  
        # Display all trades
        if self.trades:
            print("\n=== TRADE HISTORY ===")
            for i, trade in enumerate(self.trades, 1):
                print(f"Trade {i}: {trade['suit']} | ${trade['price']:.2f} x {trade['quantity']} | "
                      f"Buyer: Trader {trade['buyer']} | Seller: Trader {trade['seller']}")
        else:
            print("\n=== TRADE HISTORY ===")
            print("No trades executed")