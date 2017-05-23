from promise import promisify
from pydash import key_by
from promise.dataloader import DataLoader

from locations.models import AssociatedLocation


class AssociatedLocationLoader(DataLoader):

    @promisify
    def batch_load_fn(self, keys):
        indexed = key_by(AssociatedLocation.objects.filter(pk__in=keys).all(), lambda m: m.pk)
        return [indexed.get(key, None) for key in keys]