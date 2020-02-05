import os, json
import hmac, hashlib, base64

class OrderInfo:
    __BASE_URL = "https://api.IDCM.cc:8323"
    __HEADER = {
        "X-IDCM-APIKEY": "",
        "X-IDCM-SIGNATURE": "",
        "X-IDCM-INPUT": '',
        "Content-Type": "application/json",
        "Accept" : "text/html, application/xhtml+xml, */*"
    }

    def __init__(self):
        with open(os.getcwd() + "\\orderService\\user.json") as json_data:
           apiData = json.load(json_data)

        self.__API_KEY = apiData["ApiKey"].encode('ascii', 'ignore')
        self.__SECRET_KEY = apiData['Sign'].encode('ascii', 'ignore')
        self.__HEADER["X-IDCM-APIKEY"] = self.__API_KEY.decode()

    def __get_signature(self, inputdata):
        payload = json.dumps(inputdata).encode('utf8')
        hmacSha384 = hmac.new(self.__SECRET_KEY, payload, hashlib.sha384).digest()
        return base64.b64encode(hmacSha384).decode()

    def set_headers(self, inputdata):
        sign = self.__get_signature(inputdata)
        payload = json.dumps(inputdata)

        self.__HEADER["X-IDCM-SIGNATURE"] = sign
        self.__HEADER["X-IDCM-INPUT"] = payload

        return self.__HEADER

    def set_url(self, path):
        return self.__BASE_URL + path
