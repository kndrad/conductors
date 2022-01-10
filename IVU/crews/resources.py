from IVU.abstracts.resources import IVUResource
from IVU.crews.providers import IVUTrainCrewProvider


class IVUTrainCrewResource(IVUResource):
    def fetch(self, train_number, date):
        provider = IVUTrainCrewProvider(self._server, train_number, date)
        crew = provider.run()
        return crew
