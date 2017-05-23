from promise import promisify
from promise.dataloader import DataLoader
from pydash import key_by

from people.models import Relationship


class RelationshipLoader(DataLoader):
    @promisify
    def batch_load_fn(self, keys):
        indexed = key_by(Relationship.objects.filter(pk__in=keys).all(), lambda m: m.pk)
        return [indexed.get(key, None) for key in keys]


class FromRelationshipByPersonLoader(DataLoader):
    @promisify
    def batch_load_fn(self, keys):
        indexed = key_by(Relationship.objects.filter(from_person_id__in=keys).all(), lambda m: m.from_person_id)
        return [indexed.get(key, None) for key in keys]
