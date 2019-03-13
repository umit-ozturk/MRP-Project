import coreapi
import coreschema
from rest_framework.schemas import ManualSchema


HelloSchema = ManualSchema(fields=[
    coreapi.Field(
        "asset",
        location="query",
        required=True,
        schema=coreschema.String()
    ),
])