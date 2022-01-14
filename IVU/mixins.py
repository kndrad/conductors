from .backends import get_server_or_redirect


class FetchIVUResourcesMixin:
    model = None
    related_model = None
    resource_cls = None
    request = None

    def add_fetched_resources(self, instance):
        if not getattr(instance, self.related_model.query_name).exists():
            server = get_server_or_redirect(self.request)
            resources = self.resource_cls(**instance.attrs_dict).request(server)

            for kwargs in resources:
                obj, _ = self.related_model.objects.get_or_create(**kwargs)
                getattr(instance, self.related_model.query_name).add(obj)

            instance.update_now()
            instance.save()

    def update_fetched_resources(self, instance):
        getattr(instance, self.related_model.query_name).clear()
        return self.add_fetched_resources(instance)
