import os
import json
import requests

class OrderService:
    baseURL = "https://api.IDCM.cc:8323"
    headers = {
        "X-IDCM-APIKEY": "",
        "X-IDCM-SIGNATURE": "",
        "X-IDCM-INPUT": '',
        "Content-Type": "application/json"
    }

    def __init__(self):
        with open(os.getcwd() + "\\orderService\\user.json") as json_data:
           apiData = json.load(json_data)
        
        self.headers['X-IDCM-APIKEY'] = apiData['ApiKey']
        self.headers['X-IDCM-SIGNATURE'] = apiData['Sign']

    def getTicker(self, symbol):
        url = "/api/vi/getticker"
        inputData = { "Symbol": symbol }
        request = self.headers
        request['headers']["X-IDCM-INPUT"] = inputData

        # post
        response = requests.post(self.baseURL+url, headers=request, data={})
        
        print response
    