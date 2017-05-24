from promise import promisify
from promise.dataloader import DataLoader
from pydash import key_by

from products.models import Product


class ProductLoader(DataLoader):
    @promisify
    def batch_load_fn(self, keys):
        indexed = key_by(Product.objects.filter(pk__in=keys).all(), lambda m: m.pk)
        return [indexed.get(key, None) for key in keys]
