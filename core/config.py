import os
from dotenv import load_dotenv
load_dotenv()

#Paper trading mode, false means its actual money, true when paper trading
PAPER_MODE=True

#Alpaca Details
ALPACA_API_KEY=os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY=os.getenv("ALPACA_SECRET_KEY")
#if PAPER_MODE=true then this is active, else its to live url
if(PAPER_MODE==True):
    ALPACA_BASE_URL ="https://paper-api.alpaca.markets"

elif(PAPER_MODE==False):
    ALPACA_BASE_URL="https://api.alpaca.markets"




#Polygon details for stocks and etf
POLYGON_API_KEY=os.getenv("POLYGON_API_KEY") #now will also be for crypto


#KRAKEN for Crypto bot- Invalid due to geolocation restrictions.
#KRAKEN_API_KEY=os.getenv("KRAKEN_API_KEY")
#KRAKEN_SECRET_KEY=os.getenv("KRAKEN_SECRET_KEY")

#Allocation of capital, basically starting funds

CAPITAL ={
    "stable":1000.00,
    "risky1": 200.00,
    "risky2": 200.00,
}

#Max position size of each bot
MAX_POSITION_SIZE ={
    "stable": (CAPITAL["stable"]*.2),
    "risky1": (CAPITAL["risky1"]*.25),
    "risky2":(CAPITAL["risky2"]*.25)
}

#Emergency Kill switches
MAX_DRAWDOWN={
    "stable":(-.15), #15 percent loss= stop
    #30 percent loss = stop
    "risky1":(-.3), 
    "risky2":(-.3)
}





#assets to invest in
#adjust stable assets to include whichever you want to invest in, it can't be populated like the risky1 because its supposed to be stable
STABLE_ASSETS = ["SPY", "QQQ", "AAPL", "MSFT", "DIA", "IWM"]
#Risky1 will be modified by ML model so its dynamically changing
RISKY1_ASSETS=[]
#risky2 is in crypto and i don't reallyy know what to do for making it "risky", the X is for polygon prefix of crypto
RISKY2_ASSETS = ["X:BTCUSD","X:ETHUSD","X:SOLUSD","X:AVAXUSD","X:LINKUSD","X:ADAUSD","X:XRPUSD","X:DOGEUSD"
]

#Retraining of model occurances in days
RETRAIN_INTERVAL_DAYS=14