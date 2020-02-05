#-*- coding:utf-8 -*-
import json
import requests
from .errocode import *
from .orderinfo import OrderInfo
from decimal import Decimal
import pdb

class OrderService(OrderInfo): 
    # get error code
    def __getError(self, code):
        return getErrorCode(code)
        
    # Obtain IDCM Currency Market Price
    def get_ticker(self, symbol):
        """ Returns Obtain IDCM Currency Market Price
        Args:
            symbol (str): Trade Pair(example. "CXAT-ETH")

        Returns:
            content['data'] : Result IDCM API Data
                {
		            "timestamp": 000    //Timestamp
		            "buy": 0.002,       //Offer price 1
		            "high": 0.0,        //Highest price
		            "last": 0.0,        //Last price
		            "low": 0.0,         //Lowest price
		            "sell": 0.002,      //Ask price 1
		            "vol": 0.0          //Trading volume (past 24 hours)
	            }
            error : Error Code 
        """
        url = self.set_url("/api/v1/getticker")
        inputData = {"Symbol": symbol}

        headers = self.set_headers(inputData)

        # post
        response = requests.post(url, headers=headers, data={})
        content = json.loads(response.content, parse_float=Decimal)

        # result => 0 Fail / 1 Success
        if(content['result'] == 0):
            code = content['code']
            return self.__getError(code)
        
        return content['data']
    
    # Obtain IDCM market depth 
    def get_depth(self, symbol):
        """ Returns Obtain IDCM market depth
        Args:
            symbol (str): Trade Pair(example. "CXAT-ETH")

        Returns:
            content['data'] : Result IDCM API Data
                {
                    "asks": [{
                        "symbol": "BTC-USDT",
	                    "price": 0.01,
	                    "amount": 1
                    }],
	                "bids": [{
	                    "symbol": "BTC-USDT",
	                    "price": 0.01,
	                    "amount": 1
                    }]
	            }
            error : Error Code 
        """
        url = self.set_url("/api/v1/getdepth")
        inputData = {"Symbol": symbol}

        headers = self.set_headers(inputData)

        # post
        response = requests.post(url, headers=headers, data={})
        content = json.loads(response.content, parse_float=Decimal)

        # result => 0 Fail / 1 Success
        if(content['result'] == 0):
            code = content['code']
            return self.__getError(code)

        return content['data']

    # Obtain IDCM trading information
    def get_trades(self, symbol, since):
        """ Returns Obtain IDCM trading information
        Args:
            symbol (str) : Trade Pair(example. "CXAT-ETH")
            since  (str) : Timestamp. Maximum of 500 points of data returned after the timestamp is returned

        Returns:
            content['data'] : Result IDCM API Data
                {
	            	[{
	            	    "date": "2018-05-10 11:15:59",  //Trading time
	            	    "price": 0.01,                  //Trading price
	            	    "amount": 1,                    //Amount
	            	    "side":"sell"                   //buy or sell
	            	}]
	            }
            error : Error Code 
        """
        url = self.set_url("/api/v1/gettrades")
        inputData = {"Symbol" : symbol, "Since" : since}

        headers = self.set_headers(inputData)

        # post
        response = requests.post(url, headers=headers, data={})
        content = json.loads(response.content, parse_float=Decimal)

        # result => 0 Fail / 1 Success
        if(content['result'] == 0):
            code = content['code']
            return self.__getError(code)

        return content['data']

    # Obtain IDCM candlestick data 
    def get_kline(self, symbol, since, size, lineType):
        """ Returns Obtain IDCM candlestick data
        Args:
            symbol   (str) : Trade Pair(example. "CXAT-ETH")
            since    (str) : Timestamp. Maximum of 500 points of data returned after the timestamp is returned
            size     (str) : Specify the amount of pieces of data
            lineType (str) : K line chart type -> ordertype.py > CandlestickType

        Returns:
            content['data'] : Result IDCM API Data
                {
	            	[{
	            	    "date": "2018-05-10 11:15:59",  //Trading time
	            	    "price": 0.01,                  //Trading price
	            	    "amount": 1,                    //Amount
	            	    "side":"sell"                   //buy or sell
	            	}]
	            }
            error : Error Code 
        """
        url = self.set_url("/api/v1/getkline")
        inputData = {
            "Symbol" : symbol, 
            "Since"  : since,
            "Size"   : size,
            "Type"   : lineType
        }
        headers = self.set_headers(inputData)

        # post
        response = requests.post(url, headers=headers, data={})
        content = json.loads(response.content, parse_float=Decimal)

        # result => 0 Fail / 1 Success
        if(content['result'] == 0):
            code = content['code']
            return self.__getError(code)

        return content['data']

    # Obtain IDCM user information
    def get_user_info(self):
        """ Returns Obtain IDCM user information
        Returns:
            content['data'] : Result IDCM API Data
                {
	            	[{
	            	    "code": "BTC",  //currency type
	            	    "free": 0.01,   //available
	            	    "freezed": 1,   //frozen
	            	}]
	            }
            error : Error Code 
        """
        url = self.set_url("/api/v1/getuserinfo")
        inputData = "1"
        headers = self.set_headers(inputData)

        # post
        response = requests.post(url, headers=headers, data={})
        content = json.loads(response.content, parse_float=Decimal)

        # result => 0 Fail / 1 Success
        if(content['result'] == 0):
            code = content['code']
            return self.__getError(code)

        return content['data']

    # Order transaction
    def trade(self, symbol, size, price, side, chartType):
        """ Returns Order transaction
        Args:
            symbol    (str) : Trade Pair(example. "CXAT-ETH")
            size      (str) : Amount (at least 1000)
            price     (str) : Order Price
            side      (str) : Trade Direction(sell, buy) -> orderType.py > TradeDirection
            chartType (str) : Order Chart Type -> orderType.py > OrderType

        Returns:
            content['data'] : Result IDCM API Data
                {
	                "orderid":"21321321321334"  //Order ID
	            }
            error : Error Code
        """
        url = self.set_url("/api/v1/trade")
        inputData = {
            "Symbol" : symbol, 
            "Size"   : size,
            "Price"  : price,
            "Side"   : side,        # side => 0 Buy / 1 => Sell
            "Type"   : chartType,
        }
        headers = self.set_headers(inputData)
        
        # post
        response = requests.post(url, headers=headers, data={})
        content = json.loads(response.content, parse_float=Decimal)
        
        # result => 0 Fail / 1 Success
        if(content['result'] == 0):
            code = content['code']
            return self.__getError(code)

        return content['data']

    # Obtain IDCM user order information
    def get_order_info(self, symbol, orderID):
        """ Returns Obtain IDCM user order information
        Args:
            symbol   (str) : Trade Pair(example. "CXAT-ETH")
            orderID  (str) : Order ID

        Returns:
            content['data'] : Result IDCM API Data
                {
	               [{
	            	"orderid":"123",        //Order ID
	            	"symbol":"BTC-USDT",    //Trade pair
                    "price":0.1,            //Traded price
	            	"avgprice":1.0,         //Average price
	            	"side":0,               //Trade direction
	            	"type":1,               //Order type
	            	"timestamp":"123",      //Timestamp
	            	"amount":1,             //Amount
	            	"executedamount":1,     //Executed amount
	            	"status":1              //Order status
	              }]
	            }
            error : Error Code
        """
        url = self.set_url("/api/v1/getorderinfo")
        inputData = {
            "Symbol"  : symbol, 
            "OrderID" : orderID
        }
        headers = self.set_headers(inputData)

        # post
        response = requests.post(url, headers=headers, data={})
        content = json.loads(response.content, parse_float=Decimal)

        # result => 0 Fail / 1 Success
        if(content['result'] == 0):
            code = content['code']
            return self.__getError(code)

        return content['data']

    # Obtain IDCM historical order information (last two days of data only) 
    def get_history_order(self, symbol, pageIndex, pageSize, status):
        """ Returns Obtain IDCM historical order information (last two days of data only)
        Args:
            symbol    (str) : Trade Pair(example. "CXAT-ETH")
            pageIndex (str) : Current Page
            pageSize  (str) : Data displayed on each page, not exceeding 200 points
            status    (str) : Check the list of order status

        Returns:
            content['data'] : Result IDCM API Data
                {
	                [{
	            	    "orderid":"213",        //Order ID
	            	    "symbol":"BTC-USDT",    //Trade pair
	            	    "price":0.1,            //Traded price
	            	    "avgprice":1.0,         //Average price
	            	    "side":0,               //Trade direction
	            	    "type":1,               //Order type
	            	    "timestamp":"123",      //Timestamp
	            	    "amount":1,             //Amount
	            	    "executedamount":1,     //Executed Amount
	            	    "status":1              //Order status
	               }]
	            }
            error : Error Code
        """
        url = self.set_url("/api/v1/gethistoryorder")
        inputData = {
            "Symbol"    : symbol, 
            "PageIndex" : pageIndex,
            "PageSize"  : pageSize,
            "Status"    : [status]
        }
        headers = self.set_headers(inputData)

        # post
        response = requests.post(url, headers=request, data={})
        content = json.loads(response.content, parse_float=Decimal)

        # result => 0 Fail / 1 Success
        if(content['result'] == 0):
            code = content['code']
            return self.__getError(code)

        return content['data']

    # Withdraw currency
    def withdraw(self, symbol, address, amount):
        """ Returns Withdraw currency
        Args:
            symbol    (str) : Trade Pair(example. "CXAT-ETH")
            address   (str) : Wallet Address
            amount    (str) : Withdrawal Amount

        Returns:
            content['data'] : Result IDCM API Data
                {
                    "23123213213"   //Withdrawal request ID
                }
            error : Error Code
        """
        url = self.set_url("/api/v1/withdraw")
        inputData = {
            "Symbol"  : symbol,
            "Address" : address,
            "Amount"  : amount
        }
        headers = self.set_headers(inputData)

        # post
        response = requests.post(url, headers=request, data={})
        content = json.loads(response.content, parse_float=Decimal)

        # result => 0 Fail / 1 Success
        if(content['result'] == 0):
            code = content['code']
            return self.__getError(code)

        return content['data']

    # Cancel currency withdrawal
    def cancel_withdraw(self, symbol, withdrawID):
        """ Returns Withdraw currency
        Args:
            symbol     (str) : Trade Pair(example. "CXAT-ETH")
            withdrawID (str) : Withdrawal request ID

        Returns:
            content['data'] : Result IDCM API Data
                {
 	                true    //result
                }
            error : Error Code
        """
        url = self.set_url("/api/v1/cancel_withdraw")
        inputData = {
            "Symbol"    : symbol,
            "WithdrawID": withdrawID
        }
        headers = self.set_headers(inputData)

        # post
        response = requests.post(url, headers=headers, data={})
        content = json.loads(response.content, parse_float=Decimal)

        # result => 0 Fail / 1 Success
        if(content['result'] == 0):
            code = content['code']
            return self.__getError(code)

        return content['data']

    # Inquire currency withdrawal information
    def get_withdraw_info(self, symbol, withdrawID):
        """ Returns Withdraw currency
        Args:
            symbol     (str) : Trade Pair(example. "CXAT-ETH")
            withdrawID (str) : Withdrawal request ID

        Returns:
            content['data'] : Result IDCM API Data
                {
                    "address":"342",                    //Withdrawal address
                    "amount":1,                         //Withdrawal amount
                    "createtime":"2018-05-10 13:47:00", //Withdrawal time
	                "status":1,                         //Withdrawal status
	                "withdrawid":"4zb"                  //Withdrawal request ID
                }
            error : Error Code
        """
        url = self.set_url("/api/v1/getwithdrawinfo")
        inputData = {
            "Symbol"    : symbol,
            "WithdrawID": withdrawID
        }
        headers = self.set_headers(inputData)

        # post
        response = requests.post(url, headers=headers, data={})
        content = json.loads(response.content, parse_float=Decimal)

        # result => 0 Fail / 1 Success
        if(content['result'] == 0):
            code = content['code']
            return self.__getError(code)

        return content['data']
    
    # Cancel Order
    def cancel_order(self, symbol, orderID, side):
        """ Returns Cancel Order
        Args:
            symbol     (str) : Trade Pair(example. "CXAT-ETH")
            orderID    (str) : Order ID
            side       (str) : Trade Direction

        Returns:
            content['data'] : Result IDCM API Data
                true    //Result
            error : Error Code
        """
        url = self.set_url("/api/v1/cancel_order")
        inputData = {
            "Symbol"    : symbol,
            "OrderID"   : orderID,
            "Side"      : side
        }
        headers = self.set_headers(inputData)

        # post
        response = requests.post(url, headers=headers, data={})
        content = json.loads(response.content, parse_float=Decimal)

        # result => 0 Fail / 1 Success
        if(content['result'] == 0):
            code = content['code']
            return self.__getError(code)

        return content['data']

    # Batch Orders 
    def batch_trade(self, orderID, symbol, size, price, side, orderType, amount):
        """ Returns Batch Orders
        Args:
            orderID     (str) : Client-supplied order ID that you can customize
                It should be comprised of alpha-numeric characters with length 1 to 32. Both uppercase and lowercase are supported
            symbol      (str) : Trade Pair(example. "CXAT-ETH")
            size        (str) : Trade Amount
            price       (str) : Order Price
            side        (str) : Trade Direction
            orderType   (str) : Order Type Chart
            amount      (str) : Ther market price will be

        Returns:
            content['data'] : Result IDCM API Data
                [{
	                "orderid":"213",        //Order ID
                    "clientorderid":"123",  //Client-supplied order ID
                    "result":true,          //Result of the order. Error message will be returned if the order failed.
                    "errorcode":"200"       //Error code
	            }]
            error : Error Code
        """
        url = self.set_url("/api/v1/batch_trade")
        inputData = [{
            "ClientOrderID" : orderID,
            "Symbol"        : symbol,
            "Size"          : size,
            "Price"         : price,
            "Side"          : side,
            "Type"          : orderType,
            "Amount"        : amount
        }]

        headers = self.set_headers(inputData)

        response = requests.post(url, headers=headers, data={})
        content = json.loads(response.content, parse_float=Decimal)

        if(content['result'] == 0):
            code = content['code']
            return self.__getError(code)
        
        return content['data']
    