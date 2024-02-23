import importlib
from rest_framework import serializers
from typing import Optional, Type, TypeVar

from .models import BaseModel


BaseModelSubclass = TypeVar('BaseModelSubclass', bound=BaseModel)
ModelSerializerSubclass = TypeVar('ModelSerializerSubclass', bound=Type[serializers.ModelSerializer])


def get_model_class(class_name: str) -> Optional[BaseModelSubclass]:
    """
    Dynamically retrieves a model class for the given class name.

    Args:
        class_name: The name of the model class.

    Returns:
        The model class or None if not found.
    """

    model_module = f"catalog.models"
    try:
        model_class = getattr(importlib.import_module(model_module), class_name)
        return model_class
    except (ModuleNotFoundError, AttributeError):
        return None


def get_serializer_class(class_name: str) -> Optional[ModelSerializerSubclass]:
    """
    Dynamically retrieves a serializer class for the given class name.

    Args:
        class_name: The name of the serializer class.

    Returns:
        The serializer class or None if not found.
    """

    serializers_module = f"catalog.serializers"
    try:
        serializer_class = getattr(importlib.import_module(serializers_module), f"{class_name}Serializer")
        return serializer_class
    except (ModuleNotFoundError, AttributeError):
        return None
