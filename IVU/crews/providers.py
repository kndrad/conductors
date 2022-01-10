from IVU.abstracts.providers import IVUResourceProvider
from .requests import IVUTrainCrewRequest


class IVUTrainCrewProvider(IVUResourceProvider):
    request = IVUTrainCrewRequest
