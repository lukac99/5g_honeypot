from models import NFProfile


# fake registry (simulira NRF bazo)
registry = {

    # NRF
    "nrf-001": NFProfile(
        nfInstanceId="nrf-001",
        nfType="NRF",
        fqdn="nrf.5gc.local",
        ipv4Addresses=["10.10.0.5"],
        priority=1,
        capacity=200,
        load=15,
        locality="area1",
        heartBeatTimer=60
    ),

    # AMF instances
    "amf-001": NFProfile(
        nfInstanceId="amf-001",
        nfType="AMF",
        fqdn="amf-001.5gc.local",
        ipv4Addresses=["10.10.0.10"],
        priority=1,
        capacity=120,
        load=18,
        locality="area1",
        heartBeatTimer=60
    ),

    "amf-002": NFProfile(
        nfInstanceId="amf-002",
        nfType="AMF",
        fqdn="amf-002.5gc.local",
        ipv4Addresses=["10.10.0.11"],
        priority=2,
        capacity=120,
        load=12,
        locality="area1",
        heartBeatTimer=60
    ),

    # SMF instances
    "smf-001": NFProfile(
        nfInstanceId="smf-001",
        nfType="SMF",
        fqdn="smf-001.5gc.local",
        ipv4Addresses=["10.10.0.20"],
        priority=1,
        capacity=140,
        load=33,
        locality="area1",
        heartBeatTimer=60
    ),

    "smf-002": NFProfile(
        nfInstanceId="smf-002",
        nfType="SMF",
        fqdn="smf-002.5gc.local",
        ipv4Addresses=["10.10.0.21"],
        priority=2,
        capacity=140,
        load=21,
        locality="area1",
        heartBeatTimer=60
    ),

    # UDM
    "udm-001": NFProfile(
        nfInstanceId="udm-001",
        nfType="UDM",
        fqdn="udm-001.5gc.local",
        ipv4Addresses=["10.10.0.30"],
        priority=1,
        capacity=100,
        load=14,
        locality="area1",
        heartBeatTimer=60
    ),

    # UDR
    "udr-001": NFProfile(
        nfInstanceId="udr-001",
        nfType="UDR",
        fqdn="udr-001.5gc.local",
        ipv4Addresses=["10.10.0.31"],
        priority=1,
        capacity=150,
        load=10,
        locality="area1",
        heartBeatTimer=60
    ),

    # AUSF
    "ausf-001": NFProfile(
        nfInstanceId="ausf-001",
        nfType="AUSF",
        fqdn="ausf-001.5gc.local",
        ipv4Addresses=["10.10.0.40"],
        priority=1,
        capacity=110,
        load=17,
        locality="area1",
        heartBeatTimer=60
    ),

    # PCF
    "pcf-001": NFProfile(
        nfInstanceId="pcf-001",
        nfType="PCF",
        fqdn="pcf-001.5gc.local",
        ipv4Addresses=["10.10.0.50"],
        priority=1,
        capacity=120,
        load=23,
        locality="area1",
        heartBeatTimer=60
    ),

    # NSSF
    "nssf-001": NFProfile(
        nfInstanceId="nssf-001",
        nfType="NSSF",
        fqdn="nssf-001.5gc.local",
        ipv4Addresses=["10.10.0.60"],
        priority=1,
        capacity=80,
        load=8,
        locality="area1",
        heartBeatTimer=60
    ),

    # BSF
    "bsf-001": NFProfile(
        nfInstanceId="bsf-001",
        nfType="BSF",
        fqdn="bsf-001.5gc.local",
        ipv4Addresses=["10.10.0.70"],
        priority=1,
        capacity=90,
        load=9,
        locality="area1",
        heartBeatTimer=60
    ),

    # CHF
    "chf-001": NFProfile(
        nfInstanceId="chf-001",
        nfType="CHF",
        fqdn="chf-001.5gc.local",
        ipv4Addresses=["10.10.0.80"],
        priority=1,
        capacity=100,
        load=11,
        locality="area1",
        heartBeatTimer=60
    ),

    # SCP
    "scp-001": NFProfile(
        nfInstanceId="scp-001",
        nfType="SCP",
        fqdn="scp-001.5gc.local",
        ipv4Addresses=["10.10.0.90"],
        priority=1,
        capacity=150,
        load=19,
        locality="area1",
        heartBeatTimer=60
    ),

    # UPF (data plane)
    "upf-001": NFProfile(
        nfInstanceId="upf-001",
        nfType="UPF",
        fqdn="upf-001.5gc.local",
        ipv4Addresses=["10.10.0.100"],
        priority=1,
        capacity=200,
        load=27,
        locality="edge-site-1",
        heartBeatTimer=60
    )
}


# vrne vse NF-je
def get_all_nfs():
    return list(registry.values())


# vrne NF-je določenega tipa
def get_nfs_by_type(nf_type: str):
    return [nf for nf in registry.values() if nf.nfType == nf_type.upper()]


# vrne NF po ID
def get_nf(nf_id: str):
    return registry.get(nf_id)


# registracija NF
def register_nf(nf_id: str, profile: NFProfile):
    registry[nf_id] = profile


# update NF
def update_nf(nf_id: str, updates: dict):
    current = registry.get(nf_id)

    if not current:
        return None

    data = current.model_dump() # Pretvori trenutni Pydantic model v Python slovar
    data.update(updates) # Posodobi slovar 'data' z vrednostmi iz 'updates'
    # Razpakira slovar 'data' v ključ–vrednost argumente in jih posreduje konstruktorju NFProfile
    # Primer: data = {"nfType": "AMF", "nfId": "12345"} → NFProfile(nfType="AMF", nfId="12345")
    updated = NFProfile(**data)    
    registry[nf_id] = updated

    return updated


# odstranimo NF
def delete_nf(nf_id: str):
    return registry.pop(nf_id, None)  # pop odstrani zapis iz slovarja in vrne vrednost (če v slovarju ni nf_id vrne None)