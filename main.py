from fastapi import FastAPI, Request
from api import nf_management, nf_discovery
from logger import log_request

app = FastAPI(title="NRF") # glavna aplikacija, ki runna na serverju

# vključimo endpointe iz drugih datotek (brez tega bi FastAPI poznal samo endpointe, ki so zapisani v main.py)
app.include_router(nf_management.router)
app.include_router(nf_discovery.router)

# za vsak HTTP request se izvede ta funkcija (logging + posredovanje do endpointa)
@app.middleware("http")
async def logging_middleware(request: Request, call_next):  # request = celoten HTTP request, call_next = funkcija, ki posreduje request do endpointa
    await log_request(request)
    response = await call_next(request) # posreduj request do endpointa (drugače samo blokira)
    return response # vrni response od endpointa clientu

