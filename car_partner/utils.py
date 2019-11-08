from typing import Type

from django.http import Http404
from django.db import models

from car_partner.constants import DELETED_AT_NULL_VALUE


def get_object_from_db(obj: Type[models.Model], pk: int) -> models.Model:
    try:
        return obj.objects.get(pk=pk)
    except obj.DoesNotExist:
        raise Http404


def is_object_deleted(obj: models.Model) -> bool:
    if obj.deleted_at == DELETED_AT_NULL_VALUE:
        return False
    return True


def str_to_bool(converting_str: str) -> bool:
    return converting_str.lower() == 'true'
