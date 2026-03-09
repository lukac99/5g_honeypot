from fastapi import APIRouter, Query

from models import DiscoveryResponse
from registry import get_all_nfs, get_nfs_by_type, get_nf

router = APIRouter()


# discovery endpoint
@router.get("/nnrf-disc/v1/nf-instances", response_model=DiscoveryResponse)  # /?target_nf_type=AMF
async def discover_nf_instances(target_nf_type: str = Query(default=None, alias="target-nf-type")):
    # če je podan nfType filtriramo
    if target_nf_type:
        nfs = get_nfs_by_type(target_nf_type.upper())
    else:
        nfs = get_all_nfs()

    # vrnemo discovery response
    return DiscoveryResponse(nfInstances=nfs)  # returnamo objekt DiscoveryResponse, FastAPI ga avtomatsko serializira v JSON response


@router.get("/nnrf-disc/v1/nf-instances/{nfInstanceId}", response_model=DiscoveryResponse)
async def discover_nf_instance_by_id(nfInstanceId: str):
    nf = get_nf(nfInstanceId)
    if not nf:
        return None

    return DiscoveryResponse(nfInstances=[nf])