errorcode = {
    "200" : "Request success",
    "10001" : "Authentication failed",
    "10002" : "System error",
    "10005" : "SecretKey does not exist",
    "10006" : "Api_key does not exist",
    "10007" : "Signature does not match",
    "10017" : "API authentication failed",
    "41000" : "Invalid parameter",
    "51004" : "The user does not exist",
    "51043" : "Invalid price",
    "51044" : "Invalid amount",
    "51003" : "Account frozen",
    "41017" : "Enter trade type",
    "51011" : "Trade type does not exist",
    "51046" : "Invalid minimum amount",
    "51047" : "Invalid change amount",
    "51045" : "Invalid minimum trade amount",
    "51048" : "Invalid minimum change amount",
    "51040" : "Currency asset information does not exist",
    "51021" : "Inadequate currency asset information",
    "51041" : "Inadequate cash asset",
    "51023" : "Inadequate available amount",
    "51026" : "The data does not exist",
    "51027" : "Currency withdrawal request can be cancelled during application status only",
    "51018" : "Digital currency does not exist",
    "51022" : "Applied amount is too small",
    "51111" : "Insufficient wallet balance",
    "51112" : "The declared amount is invalid"
}
def getErrorCode(code):
    error = str(code)
    return errorcode[error]