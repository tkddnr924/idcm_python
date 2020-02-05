import enum

class OrderType(enum.Enum):
    Market                  = 0
    Limit                   = 1
    Stop                    = 2
    TrailingStop            = 3
    FillOrKill              = 4
    ExchangeMarket          = 5
    ExchangeLimit           = 6
    ExchangeStop            = 7
    ExchangeTrailingStop    = 8
    ExchangeFillOrKill      = 9

class TradeDirection(enum.Enum):
    Buy     = 0
    Sell    = 1

class CandlestickType(enum.Enum):
    OneMin      = "1min"
    FiveMin     = "5min"
    FifteenMin  = "15min"
    HalfHour    = "30min"
    OneHour     = "1hour"
    OneDay      = "1day"
    Week        = "1week"

class OrderStatus(enum.Enum):
    CancelledTrade  = -2
    Invalid         = -1
    Pending         = 0
    PartialTrade    = 1
    FullTrade       = 2
    Executed        = 3

class WithdrawalStatus(enum.Enum):
    Accepted                = 1
    Under_Approval          = 2
    Processing              = 3
    Wallet_Process_Failure  = 4
    Not_Approved            = 5
    Completed               = 12
    Cancel                  = 7
    Waiting_for_Deposit     = 8
    Confirming              = 9
    Amount_received         = 10
    Withdrawn               = 11
    Abnormal_Order          = 99