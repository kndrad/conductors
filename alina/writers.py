from alina.tools.utils import fetch_credentials


class ModelRelatedObjectsWriter:

    def __init__(self, model):
        self._model = model
        self._objects = self._model.get_related_objects()

    def write_on_request(self, request):
        username, password = fetch_credentials(request)

