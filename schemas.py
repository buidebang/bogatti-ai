from pydantic import BaseModel, Field
from typing import List, Dict

class ModelInfo(BaseModel):
    display_name: str
    provider_api: str
    cost_per_request: float
    icon: str

class PersonaInfo(BaseModel):
    display_name: str
    system_prompt: str

class ConfigInfo(BaseModel):
    strings: Dict[str, str]
    personas: Dict[str, PersonaInfo]
    rates: Dict[str, int]
    admin_secret: str
