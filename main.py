#-*- coding:utf-8 -*-
from orderService.orderService import OrderService
from orderService.orderType import OrderType as OT, TradeDirection as TD
import os, random, threading, logging, atexit
from datetime import datetime
from decimal import Decimal
from time import sleep
from queue import Queue
import numpy as np
from termcolor import colored
import pdb 

SYMBOL = "CXAT-ETH"
orderQueue = Queue()
loggers = {}
workers = []
exit_flag = True
FORMAT = "%(asctime)-15s %(message)s %(method)s %(orderID)s %(price)s %(amount)s"

@atexit.register
def program_exit():
    exit_flag = False
    orderQueue = None
    loggers = {}
    get_thread_alive()
    print("\n\tThis Program Exit...\n")

def get_thread_alive():
    flag = False
    for worker in workers:
        if worker.is_alive():
            flag = True
    
    if flag:
        text = colored("Worker Running...", "green")
        print(text)
    else:
        text = colored("Worker None", "magenta")
        print(text)

def display_title_bar():
    os.system('cls')

    print(colored("\t**********************************************","yellow", attrs=["bold"]))
    print(colored("\t*********   ", "yellow", attrs=["bold"]),colored("IDCM Auto Exchanging", "green", attrs=["bold"]), colored("  **********", "yellow", attrs=["bold"]))
    print(colored("\t**********************************************", "yellow", attrs=["bold"]))
    get_thread_alive()
    # current_idcm()

def get_user_choice():
    print(colored("\n[1]", "cyan", attrs=["bold"]), "Auto Exchanging Start")
    print(colored("[r]", "cyan", attrs=["bold"]), "Reload")
    print(colored("[h]", "cyan", attrs=["bold"]), "Help")
    print(colored("[q]", "magenta", attrs=["bold"]), "Quit")

    return input("\n(IDCM)$ ")

def current_idcm():
    """Test 필요"""
    service = OrderService()
    result = service.getTicker(SYMBOL)

    # timestamp
    timestamp = result["timestamp"]
    date = datetime.fromtimestamp(timestamp)
    
    print("\tCurrent Time: " + str(date))
    print("\tHighest Price: " + str(result['high'].quantize(Decimal('1.00000000'))))
    print("\tLowest Price: " + str(result['low'].quantize(Decimal('1.00000000'))))
    print("\tLast Price: " + str(result['last'].quantize(Decimal('1.00000000'))))
    print("\tBuy: " + str(result['buy'].quantize(Decimal('1.00000000'))))
    print("\tSell: " + str(result['sell'].quantize(Decimal('1.00000000'))))
    print("\tVol: " + str(result['vol']))

def idcm_logging(name, filename):
    if loggers.get(name):
        return loggers.get(name)
    else:
        logger = logging.getLogger(name)
        formatter = logging.Formatter(FORMAT)
        fileHandler = logging.FileHandler(filename)
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)
        loggers[name] = logger

        return logger

def set_log(method, orderid, price, amount):
    log = {
        'method'  : method,
        "orderID" : "OrderID: [" + orderid + "]",
        "price"   : str(price)  + " ETH",
        "amount"  : str(amount) + " CXAT"
    }

    return log

# Thread
def SellWork(maxprice, minprice, cycle, amount):
    logger = idcm_logging("sell_logger", "./log/sell.log")
    chartType = OT.Limit.value
    test = 0
    service = OrderService()
    try:
        while test < 5: # exit_flag:
            price = str(round(Decimal(random.uniform(minprice, maxprice)), 8))
            result = service.trade(SYMBOL, amount, price, TD.Sell.value, chartType)

            if not 'orderid' in result.keys():
                print(colored("\nSell Error", attrs=["bold"]), ":", colored(result, 'red'))
                break
            orderID = result["orderid"]

            # put Queue
            orderQueue.put((orderID, price, amount, chartType), False)

            # logging
            log = set_log("SELL", orderID, price, amount)
            logger.warning("Exchanging", extra=log)

            real_cycle = random.randrange(0, cycle)
            sleep(real_cycle)
            test = test + 1
    except:
        print("Sell Work Error...")
        raise

# Thread
def BuyWork(cycle):
    logger = idcm_logging("buy_logger", "./log/buy.log")
    service = OrderService()
    test = 0
    if orderQueue == None:
        print("Order Queue None")
        sleep(10)
    try:
        while test < 5:# exit_flag:
            if not orderQueue.empty():
                # Get Queue
                sellID, price, amount, chartType = orderQueue.get(False)
                result = service.trade(SYMBOL, amount, price, TD.Buy.value, chartType)

                if not 'orderid' in result.keys():
                    print(colored("\nBuy Error", attrs=["bold"]), ":", colored(result, 'red'))
                    break
                orderID = result['orderid']

                # logging
                log = set_log("BUY", orderID, price, amount)
                logger.warning("Exchanging", extra=log)

                real_cycle = random.randrange(0, cycle)
                sleep(real_cycle)
                test = test + 1
            else:
                print("None Order Queue...")
                sleep(cycle)
    except:
        print("Buy Work Error...")
        raise
    

def work(maxPrice, minPrice, sellbyone, sellcycle, buycycle):
    sellWorker = threading.Thread(target=SellWork, args=(maxPrice, minPrice, sellcycle, sellbyone))
    buyWorker = threading.Thread(target=BuyWork, args=(buycycle, ))
    
    workers.append(sellWorker)
    workers.append(buyWorker)

    # Daemon Thread
    sellWorker.setDaemon(True)
    buyWorker.setDaemon(True)

    # Thread Start
    sellWorker.start()
    buyWorker.start()

    display_title_bar()

def main():
    try:
        input_maxPrice = input("Max Sell Amount: ")
        maxPrice = float(input_maxPrice)
        
        input_minPrice = input("Min Sell Amount: ")
        minPrice = float(input_minPrice)

        if((maxPrice - minPrice) < 0):
            print("\n\"Min Sell Amount\" cannot be greater than the \"Max Sell Amount\".")
            return
        
        input_byOne = input("Sell quantity per turn: ")
        sellbyone = int(input_byOne)

        if int(input_byOne) < 1000:
            print("\nSell Quantity at least 1000")
            return

        input_sellCycle = input("Sell Cycle: ")
        sellCycle = int(input_sellCycle)

        input_buyCycle = input("Buy Cycle: ")
        buyCycle = int(input_buyCycle)

        if((buyCycle - sellCycle) < 0):
            print("\n\"Sell Cycle\" cannot be greater than the \"Buy Cycle\".")
            return
        
        work(maxPrice, minPrice, sellbyone, sellCycle, buyCycle)
        
    except ValueError:
        print("\nPlease enter numbers only... Try again...")
        return
    except TypeError:
        print("\nType Error... Try again")
        return
    
def format_float(num):
    return np.format_float_positional(num, trim='-')
    
def testService():
    import pdb
    pdb.set_trace()
    

if __name__ == "__main__":
    choice = ""
    display_title_bar()
    while choice != "q":
        choice = get_user_choice()

        display_title_bar()
        if choice == "1":
            main()
        elif choice == "h":
            testService()
            print("\nHelp!!")
        elif choice == "q":
            print("\nQuit!!")
            sleep(1)
        elif choice == "r":
            print("Reload!!")
        else:
            print("\nInvaild Choice...")
            
    
    # main()


