from .conf import settings
from . import utils


class BaseViewSetRegistry:

    def __init__(self):
        pass

    def get_urlpatterns(self, prefix=''):

        urlpatterns = []

        for viewset in settings.ITEM_TYPE_REGISTRY.viewsets:

            if isinstance(viewset, str) is True:
                viewset = utils.load(viewset)

            item_type = getattr(viewset, 'item_type', None)
            pydantic_model = getattr(viewset, 'pydantic_model', None)

            # if item_type is not None and pydantic_model is not None:
            #     settings.ITEM_TYPE_REGISTRY.register(pydantic_model)

            urlpatterns += viewset.get_urlpatterns(prefix=prefix)

        return urlpatterns


class BaseItemTypeRegistry:

    item_types = {}

    def __init__(self):
        for x in settings.SERIALIZER_LIST:
            self.register(x)

    def find(self, item_type):
        return self.item_types.get(item_type, None)

    def register(self, serializer):
        if isinstance(serializer, str) is True:
            serializer = utils.load(serializer)
        self.item_types[serializer._item_type] = serializer

    @property
    def viewsets(self):
        viewsets = []
        for key in self.item_types.keys():
            viewsets += self.item_types[key].viewsets()
        return viewsets

    def get_item_types(
            self,
            for_admin=False,
            item_types=None,
            format='list'
            ):

        format_choices = [
            'list',
            'choices'
        ]

        if isinstance(item_types, list) is False and item_types is not None:
            item_types = [item_types, ]

        if format not in format_choices:
            raise ValueError('Format is not supported')

        _item_types = []

        for key in self.item_types.keys():

            add = True
            serializer = self.item_types[key]

            if for_admin is False and serializer._project_admin_required is True:
                add = False

            if item_types is not None and add is True:
                if len(item_types) != 0:
                    if serializer._item_type not in item_types:
                        add = False

            if add is True:
                _item_types.append(serializer)

        if format == 'choices':
            choices = []
            for x in _item_types:
                choices.append([
                    x._item_type,
                    x._display_name_plural
                ])
            return choices

        return _item_types

    def serialize(self, objects):
        results = []
        for object in objects:
            for key in self.item_types.keys():
                model = self.item_types[key]
                if model._item_type == model.get_item_type(object):
                    results.append(model(**object))
                    break
        return results


class ViewSetRegistry(BaseViewSetRegistry):
    pass


class ItemTypeRegistry(BaseItemTypeRegistry):
    pass
