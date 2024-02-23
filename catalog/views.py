import json
import os
import sys

from django.http import HttpRequest, JsonResponse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view
from rest_framework import status

from .utils import get_model_class, get_serializer_class, BaseModelSubclass, ModelSerializerSubclass

__dir_location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
FIELD_MAPPING = json.load(open(os.path.join(__dir_location__, "field_mapping.json"), "r"))


def _serialize_and_save_item(model_class: BaseModelSubclass, serializer_class: ModelSerializerSubclass,
                             item_type: str, item_data: dict):
    try:
        model = model_class.objects.get(pk=item_data.get('id'))
        serializer = serializer_class(model, data=item_data, partial=True)
    except model_class.DoesNotExist:
        serializer = serializer_class(data=item_data)

    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)
        print(f"Could not save {item_type} model with following data: {item_data}.", file=sys.stderr)


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'body': openapi.Schema(type=openapi.TYPE_STRING, description='string')}
    )
)
@api_view(['POST'])
def upload_data(request: HttpRequest) -> JsonResponse:
    """
    Upload data in JSON format and save it to the database.
    The data should be an array of objects, where each object represents a model instance.

    Args:
        request: Http request, containing the JSON data in body.

    Returns:
        A JSON object with a message and status code indicating the outcome of the request -
        201 if successful,
        400 if data are not valid JSON.
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"Message": "Data are not valid JSON."}, status=status.HTTP_400_BAD_REQUEST)

    for item in data:
        for item_type, item_data in item.items():
            # Get the appropriate model class
            model_class = get_model_class(item_type)
            if not model_class:
                print(f"Could not get model class for item: {item}", file=sys.stderr)
                continue

            # Get the appropriate serializer class
            serializer_class = get_serializer_class(item_type)
            if not serializer_class:
                print(f"Could not get serializer class for item: {item}", file=sys.stderr)
                continue

            item_data_renamed = {FIELD_MAPPING.get(k, k): v for k, v in item_data.items()}
            _serialize_and_save_item(model_class, serializer_class, item_type, item_data_renamed)

    return JsonResponse({"Message": "Data successfully loaded."}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_model_entry(request: HttpRequest, model_type: str, model_id: int) -> JsonResponse:
    """
    Get specific model instance for given model type and model id.

    Args:
        request: Http request.
        model_type: Model type.
        model_id: Model id.

    Returns:
        A JSON object with the model instance if successful (200).
        Error message if model type or instance are not found (404).
    """
    model_class = get_model_class(model_type)
    if not model_class:
        return JsonResponse({"Message": f"Could not find model class for {model_type}."},
                            status=status.HTTP_404_NOT_FOUND)

    serializer_class = get_serializer_class(model_type)
    if not serializer_class:
        return JsonResponse({"Message": f"Could not find serializer for {model_type}"},
                            status=status.HTTP_404_NOT_FOUND)

    try:
        entry = model_class.objects.get(pk=model_id)
    except model_class.DoesNotExist:
        return JsonResponse({"Message": f"Could not find {model_type} with id {model_id}"},
                            status=status.HTTP_404_NOT_FOUND)

    entry_data = serializer_class(entry).data

    return JsonResponse({model_class.__name__: entry_data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_all_model_entries(request: HttpRequest, model_type: str) -> JsonResponse:
    """
    Get list of all model instances for provided model type.

    Args:
        request: Http request.
        model_type: Model type.

    Returns:
        A JSON object with the list of all model instances if successful (200).
        Error message if model type or instance are not found (404).
    """
    model_class = get_model_class(model_type)

    if not model_class:
        return JsonResponse({"Message": f"Could not find model class for {model_type}."},
                            status=status.HTTP_404_NOT_FOUND)

    serializer_class = get_serializer_class(model_type)
    if not serializer_class:
        return JsonResponse({"Message": f"Could not find serializer for {model_type}"},
                            status=status.HTTP_404_NOT_FOUND)

    entries_data = []
    for entry in model_class.objects.all():
        entries_data.append(serializer_class(entry).data)

    return JsonResponse({f"{model_class.__name__}s": entries_data}, status=status.HTTP_200_OK)
