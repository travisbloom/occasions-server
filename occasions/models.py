from django.db import models


class BaseModel(models.Model):
    datetime_created = models.DateTimeField(auto_now_add=True, db_index=True)
    datetime_updated = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ['-datetime_updated']
