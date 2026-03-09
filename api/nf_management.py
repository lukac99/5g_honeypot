from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from models import NFProfile
from registry import register_nf, update_nf, delete_nf, get_nf

# router endpointe v main.py dodamo z app.include_router(nf_management.router)
router = APIRouter()

ALLOWED_PATCH_FIELDS = {
    "nfStatus",
    "fqdn",
    "ipv4Addresses",
    "priority",
    "capacity",
    "load",
    "locality",
    "heartBeatTimer",
}


# registracija NF instance
@router.put("/nnrf-nfm/v1/nf-instances/{nfInstanceId}", response_model=NFProfile) # response_model - poskrbi, da FastAPI vedno vrne objekt NFProfile (če endpoint vrne kaj drugega, bo FastAPI samodejno poskušal pretvoriti v NFProfile, če to ni mogoče, bo vrnil napako)
async def register_nf_instance(nfInstanceId: str, profile: NFProfile):  # nfInstanceId iz URL-ja, profile iz JSON body-ja (ker profile definiran kot path ali query parameter, ga FastAPI samodejno išče v body-ju)
    # preverimo ali NF že obstaja
    NF_already_exists = get_nf(nfInstanceId) is not None
    profile.nfInstanceId = nfInstanceId
    register_nf(nfInstanceId, profile)

    # če obstaja -> 200
    if NF_already_exists:
        return JSONResponse( # vrni odgovor kot JSON, nastavi status code + vsebino
            status_code=status.HTTP_200_OK, # default status code je 200
            content=profile.model_dump()  # pretvori v python slovar
        )

    # če ne obstaja -> 201
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=profile.model_dump(),
        headers={"Location": f"/nnrf-nfm/v1/nf-instances/{nfInstanceId}"} # dodamo header Location, ki kaže na URL novega resource-a
    )


# update NF
@router.patch("/nnrf-nfm/v1/nf-instances/{nfInstanceId}")
async def patch_nf_instance(nfInstanceId: str, updates: dict): # updates dobimo iz body-ja
    invalid_fields = [k for k in updates if k not in ALLOWED_PATCH_FIELDS]
    if invalid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid patch fields: {', '.join(invalid_fields)}"
        )

    updated = update_nf(nfInstanceId, updates)
    if not updated: # če NF ne obstaja
        raise HTTPException(status_code=404, detail="NF instance not found") # ustavi izvajanje funkcije, vrni 404 code

    return updated.model_dump()


# delete NF
@router.delete("/nnrf-nfm/v1/nf-instances/{nfInstanceId}")
async def remove_nf_instance(nfInstanceId: str):

    deleted = delete_nf(nfInstanceId)
    if not deleted: # če NF ne obstaja
        raise HTTPException(status_code=404, detail="NF instance not found")

    return {"message": "NF deregistered", "nfInstanceId": nfInstanceId}












#tega daj v discovery
@router.get("/nnrf-nfm/v1/nf-instances/{nfInstanceId}")
async def get_nf_instance(nfInstanceId: str):
    nf = get_nf(nfInstanceId)

    if not nf:
        raise HTTPException(status_code=404, detail="NF instance not found")

    return nf.model_dump()