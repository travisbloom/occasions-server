from promise import promisify
from promise.dataloader import DataLoader
from pydash import group_by

from events.models import EventToEventType
from products.models import ProductToEventType


class EventTypesByEventLoader(DataLoader):
    @promisify
    def batch_load_fn(self, keys):
        indexed = group_by(
            EventToEventType.objects.filter(event_id__in=keys).prefetch_related('event_type').all(),
            lambda m: m.event_id
        )
        return [
            [join.event_type for join in indexed.get(key, [])]
            for key in keys
        ]


class EventTypesByProductLoader(DataLoader):
    @promisify
    def batch_load_fn(self, keys):
        indexed = group_by(
            ProductToEventType.objects.filter(product_id__in=keys).prefetch_related('event_type').all(),
            lambda m: m.product_id
        )
        return [
            [join.event_type for join in indexed.get(key, [])]
            for key in keys
        ]
