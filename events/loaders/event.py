from promise import promisify
from promise.dataloader import DataLoader
from pydash import key_by

from events.models import Event


class EventLoader(DataLoader):
    @promisify
    def batch_load_fn(self, keys):
        indexed = key_by(Event.objects.filter(pk__in=keys).all(), lambda m: m.pk)
        return [indexed.get(key, None) for key in keys]
