import threading
import time
from orderbook import Orderbook
from Trader1 import Trader1
from Trader2 import Trader2
from Trader3 import Trader3
from Trader4 import Trader4

def trader_thread(trader,orderbook,suits):

    print(f"Thread {trader.id} Starting..")
    trader.compute_fair_prices(orderbook)
    print(f"Trader {trader.id} Submitted")

def main():

    orderbook = Orderbook()
    
    deck = orderbook.make_deck()
    hands = orderbook.distribute_deck()

    trader1 = Trader1(1,hands[0])
    trader2 = Trader2(2,hands[1])
    trader3 = Trader3(1,hands[2])
    trader4 = Trader4(4,hands[3])
    traders = [trader1, trader2, trader3, trader4]
    print(deck)
    suits = list(deck.keys())
    
    # Start trader threads
    print("="*50)
    print("STARTING TRADER THREADS")
    print("="*50)
    threads = []
    for trader in traders:
        thread = threading.Thread(
            target=trader_thread, 
            args=(trader, orderbook, suits)
        )
        thread.start()
        threads.append(thread)
    # Wait for all traders to finish
    for thread in threads:
        thread.join()    
    print("\n" + "="*50)
    print("ALL TRADER THREADS COMPLETED")
    print("="*50)
    # Display final orderbook
    orderbook.display_book()
    
    print("\n" + "="*50)
    print("SIMULATION COMPLETE")
    print("="*50)
if __name__ == "__main__":
    main()

