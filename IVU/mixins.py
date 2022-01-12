from django.views import View

from .backends import get_server_or_redirect


class ModelRelatedObjectsMixin(View):
    model = None
    related_model = None
    resource = None

    def add_related_objects(self, instance):
        if not getattr(instance, self.related_model.query_name).exists():
            server = get_server_or_redirect(self.request)
            resources = self.resource(**instance.resource_kwargs).request(server)

            for kwargs in resources:
                obj, _ = self.related_model.objects.get_or_create(**kwargs)
                getattr(instance, self.related_model.query_name).add(obj)

            instance.update_now()
            instance.save()

    def update_related_objects(self, instance):
        getattr(instance, self.related_model.query_name).clear()
        return self.add_related_objects(instance)