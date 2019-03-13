import coreapi
import coreschema
from rest_framework.schemas import ManualSchema


HelloSchema = ManualSchema(fields=[
    coreapi.Field(
        "email",
        location="query",
        required=False,
        schema=coreschema.String()
    ),
])