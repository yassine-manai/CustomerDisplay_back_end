from typing import Optional
from pydantic import BaseModel


#Location Data 
class Locationdata(BaseModel):
    message : int = 100
    icon: str
    name: str = "PUMC Carpark"
    exit_point: str = "Exit 704"
    timezone: str = "Asia/Kuwait"


#Footer Data
class footerData(BaseModel):
    message : int = 110
    timerFooter : int = 6

# S1- IDLE Model
class IdleModel(BaseModel):
    message: int = 1
    timerIntervale: int = 6


# S2 - Short term parker-Price display
class STppd(BaseModel):
    message: int = 2
    DispTime: int = 10
    entryTime: str = "21-02-2024 14:36"
    exitTime: str = "21-02-2024 17:36"
    lenghtOfStay: str = "2 hours"
    amount: str = "150"
    currency: str = "KWD"
    licencePlate: str = "ABC1234"
    pathImage: str

# S3 - Exit short term parker - Goodbye message
class EstpGm(BaseModel):
    message: int = 3
    DispTime: int = 10
    paymentSuccess: str = "Payment Done Successfully"
    visitMessage: str = "Thank you for your visit, Drive Safe !"


# S4 -  Pay as you go-GOODBYE Message
class paygm(BaseModel):
    message: int = 4
    DispTime: int = 10
    name: str = "Mr. Yassine Manai"
    thankYouMessage: str = "Thank you for your visit"
    licencePlate: str = "ABC123"
    entryTime: str = "21-02-2024 14:36"
    exitTime: str = "21-02-2024 17:36"
    lenghtOfStay: str = "2 hours"
    amount: str = "150"
    currency: str = "KWD"
    carImage: str


# S5 - Prebooking + Subscriber - GOODBYE Message
class psgm(BaseModel):
    message: int = 5
    DispTime: int = 10
    name: str = "Mr. Yassine Manai"
    thankYouMessage: str = "Thank you for your visit"
    licencePlate: str = "ABC123"
    entryTime: str = "21-02-2024 14:36"
    exitTime: str = "21-02-2024 17:36"
    lenghtOfStay: str = "2 hours"
    carImage: str


# S6 + S7 + S8 -  Pay as you go-GOODBYE Message

class payggm(BaseModel):
    message: int
    DispTime: int = 10
    name: str = "Mr. Yassine Manai"
    thankYouMessage: str = "mesasge = 7 : You don’t have enough credit in your wallet / message = 8 : You exceed your booking period / message = 9 :Your subscription is expired "
    licencePlate: str = "ABC123"
    entryTime: str = "21-02-2024 14:36"
    exitTime: str = "21-02-2024 17:36"
    lenghtOfStay: str = "2 hours 31 minutes"
    currency: str = "KWD"
    amount: str = "150"
    carImage: str


""" # S7 -  Pay as you go-GOODBYE Message - V2
class PAYGGM(BaseModel):
    message: int = 7
    DispTime: int = 10
    name: str
    thankYouMessage: str
    licencePlate: str
    entryTime: str
    exitTime: str
    lenghtOfStay: str
    currency: str
    amount: str
    carImage: str


# S8 -  Pay as you go-GOODBYE Message - V3
class PAYGGM(BaseModel):
    message: int = 8
    DispTime: int = 10
    name: str
    thankYouMessage: str
    licencePlate: str
    entryTime: str
    exitTime: str
    lenghtOfStay: str
    amount: str
    currency: str
    carImage: str """


#S9 -  Pay as you go-apology message - 404 V1 + V2 + V3
class paygam(BaseModel):
    message: int 
    DispTime: int = 10
    apologyMessage: Optional[str] = "We apologize, the license plate is not recognized or not found in our system !"
    apologyTitle: Optional[str] = "We apologize !"
    apologyDescription: Optional[str] = "The license plate is not recognized or not found in our system!Our help desk cashier will help you to pay your fees."
    apologyDescription: Optional[str] = "Our help desk cashier will help you to pay your fees."
    helpDescription: Optional[str] = "Our help desk cashier will help you to pay your fees."
    carImage: str



""" #S10 -  Pay as you go-apology message - 404 V2
class PAYGAMV2(BaseModel):
    message: int = 10
    DispTime: int = 10
    apologyTitle: str
    apologyDescription: str
    carImage: str


#S11 -  Pay as you go-apology message - 404 V3
class PAYGAMV3(BaseModel):
    message: int = 11
    DispTime: int = 10
    apologyHeading: str
    apologyDescription: str
    helpDescription: str
    carImage: str """








