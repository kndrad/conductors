from IVU.abstracts.parsers.responses import IVURequestResponseContentParser
from .containers import IVUTripCrewMemberContainerHTML


class IVUTrainCrewRequestResponseParser(IVURequestResponseContentParser):
    container = IVUTripCrewMemberContainerHTML
