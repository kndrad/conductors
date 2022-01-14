from .backends import get_server_or_redirect


class ManageRelatedResourcesMixin:
    model = None
    related_model = None
    resource_cls = None
    request = None

    def add_related_resources(self, instance):
        if not getattr(instance, self.related_model.query_name).exists():
            server = get_server_or_redirect(self.request)
            resources = self.resource_cls(**instance.attrs_dict).request(server)

            for kwargs in resources:
                obj, _ = self.related_model.objects.get_or_create(**kwargs)
                getattr(instance, self.related_model.query_name).add(obj)

            instance.update_now()
            instance.save()

    def update_related_resources(self, instance):
        getattr(instance, self.related_model.query_name).clear()
        return self.add_related_resources(instance)
