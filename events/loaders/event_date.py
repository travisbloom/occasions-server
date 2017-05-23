import pendulum
from promise import promisify
from pydash import key_by, group_by
from promise.dataloader import DataLoader

from events.models import EventDate


class EventDateLoader(DataLoader):

    @promisify
    def batch_load_fn(self, keys):
        indexed = key_by(EventDate.objects.filter(pk__in=keys).all(), lambda m: m.pk)
        return [indexed.get(key, None) for key in keys]


class EventDateByEventLoader(DataLoader):

    @promisify
    def batch_load_fn(self, keys):
        indexed = group_by(EventDate.objects.filter(event_id__in=keys).all(), lambda m: m.event_id)
        return [indexed.get(key, None) for key in keys]


class NextEventDateByEventLoader(DataLoader):

    @promisify
    def batch_load_fn(self, keys):
        indexed = group_by(
            EventDate.objects.filter(
                event_id__in=keys,
                date_start__gte=pendulum.now().subtract(days=1)
            ).all(),
            lambda m: m.event_id
        )
        return [indexed.get(key, [None])[0] for key in keys]