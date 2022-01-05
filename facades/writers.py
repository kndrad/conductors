from facades.backends import facade_authentication


class ModelRelatedObjectsWriter:

    def __init__(self, model):
        self._model = model
        self._objects = self._model.get_related_objects()

    def write_on_request(self, request):
        facade = facade_authentication(request)

