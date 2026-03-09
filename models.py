from pydantic import BaseModel, Field  # preverja ali je pravi tip podatkov
from typing import List, Optional # used to enforce data types (lists, optional fields) - they aren't included by default


# FastAPI samodejno pretvori JSON body v NFProfile objekt
# to je objekt, ki ga NRF hrani za vsako registrirano NF instanco
class NFProfile(BaseModel):
    nfInstanceId: str
    nfType: str    # tip NF (AMF, SMF, UDM ...)
    nfStatus: str = "REGISTERED"
    fqdn: str = None    # optional: (string or None)
    ipv4Addresses: List[str] = Field(default_factory=list)
    priority: int = 1
    capacity: int = 100
    load: int = 10
    locality: str = "area-1"
    heartBeatTimer: int = 60


# response model za discovery
class DiscoveryResponse(BaseModel):
    # koliko časa je rezultat veljaven
    validityPeriod: int = 60
    # seznam najdenih NF instanc
    nfInstances: List[NFProfile]
