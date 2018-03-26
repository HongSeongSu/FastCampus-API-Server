from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True


class CreatedDateModel(BaseModel):
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class ModifiedDateModel(BaseModel):
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TimeStampedModel(CreatedDateModel, ModifiedDateModel):
    class Meta:
        abstract = True
