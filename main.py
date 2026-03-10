from fastapi import FastAPI, Request
from api import nf_management, nf_discovery
from logger import log_request
from icmp_logger import listen_for_ping
import threading
from contextlib import asynccontextmanager



# funkcija, ki se izvede ob zagonu aplikacije
@asynccontextmanager
async def lifespan(app: FastAPI):
    # ustvarimo nov thread, ki bo poslušal ICMP (ping)
    thread = threading.Thread(target=listen_for_ping, daemon=True)
    # zaženemo thread
    thread.start()
    yield  # yield pove fastAPI: inicializacija je končana, app lahko začne sprejemati requeste
    # če damo kodo za yield, bi se ta izvedla ob shutdownu aplikacije

app = FastAPI(title="NRF", lifespan=lifespan) # glavna aplikacija, ki runna na serverju
# lifespan=lifespan pove FastAPI, katero funkcijo naj izvede ob zagonu in ob ustavitvi aplikacije

# vključimo endpointe iz drugih datotek (brez tega bi FastAPI poznal samo endpointe, ki so zapisani v main.py)
app.include_router(nf_management.router)
app.include_router(nf_discovery.router)

# za vsak HTTP request se izvede ta funkcija (logging + posredovanje do endpointa)
@app.middleware("http")
async def logging_middleware(request: Request, call_next):  # request = celoten HTTP request, call_next = funkcija, ki posreduje request do endpointa
    await log_request(request)
    response = await call_next(request) # posreduj request do endpointa (drugače samo blokira)
    return response # vrni response od endpointa clientu

