from orderService import orderService

def main():
    oS = orderService.OrderService
    oS.getTicker(symbol="BTC-USDT")


if __name__ == "__main__":
    main()

