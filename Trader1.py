from typing import Dict,List
import math
from itertools import permutations
class Trader1:

    def __init__(self,trader_id:int,hand:Dict[str,int]):
        self.id=trader_id
        self.hand=hand
        self.cash=300
        self.fair_price = {}
        self.probabilities_goal_suit = {}
    def get_post(self,deck,suit):
        post_prob=0
        other_keys = [k for k in deck.keys() if k!=suit]
        value_perms = set(permutations([10,10,8]))
        for p in value_perms:
            count = math.comb(12,deck[suit])
            for k,v in zip(other_keys,p):
                count*=math.comb(v,deck[k])
            post_prob+=count
    
        return post_prob
    def compute_fair_prices(self,orderbook):

        p_spades_prior,p_clubs_prior,p_diamonds_prior,p_hearts_prior=0.25,0.25,0.25,0.25
        p_spades_post,p_clubs_post,p_diamonds_post,p_hearts_post = self.get_post(self.hand,'Spades'),self.get_post(self.hand,'Clubs'),self.get_post(self.hand,'Diamonds'),self.get_post(self.hand,'Hearts')
        total_sum = p_spades_post+p_clubs_post+p_diamonds_post+p_hearts_post
        # print(p_spades_post/total_sum,p_clubs_post/total_sum,p_hearts_post/total_sum,p_diamonds_post/total_sum)
        goal_spades_post =  p_clubs_post/total_sum
        goal_clubs_post =  p_spades_post/total_sum
        goal_hearts_post =  p_diamonds_post/total_sum
        goal_diamonds_post =  p_hearts_post/total_sum

        self.probabilities_goal_suit['Spades'] = goal_spades_post
        self.probabilities_goal_suit['Clubs'] = goal_clubs_post
        self.probabilities_goal_suit['Hearts'] = goal_hearts_post
        self.probabilities_goal_suit['Diamonds'] = goal_diamonds_post

        for suit,prob in self.probabilities_goal_suit.items():
            self.fair_price[suit]=prob*10
        print("====================================================================")
        print(f"TRADER 1 : {self.hand}======")
        print(f"Fair prices : {self.fair_price}=======")
        print(f"Probabs of goal suit : {self.probabilities_goal_suit}=======")
        print("====================================================================")
    def submit_orders(self, orderbook, suits: List[str]):
        """Submit buy and sell orders"""
        # for suit in suits:
        #     fair_price = self.fair_prices.get(suit, 5.0)
        #     my_count = self.hand.get(suit, 0)
        #     if my_count > 0:
        #         ask_price = round(fair_price + 0.8, 2)
        #         if ask_price <= 10:
        #             orderbook.add_order(suit, 'ask', ask_price, 1, self.id)
        #     if fair_price > 2.5:
        #         bid_price = round(fair_price - 0.3, 2)
        #         if bid_price >= 0:
        #             orderbook.add_order(suit, 'bid', bid_price, 1, self.id)
        pass


