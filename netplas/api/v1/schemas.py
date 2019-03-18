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


RegisterSchema = ManualSchema(fields=[
    coreapi.Field(
        'user["name"]',
        required=True,
        location="body",
        schema=coreschema.String()
    ),
    coreapi.Field(
        'user["surname"]',
        required=True,
        location="body",
        schema=coreschema.String()
    ),
    coreapi.Field(
        'user["email"]',
        required=True,
        location="body",
        schema=coreschema.String()
    ),
    coreapi.Field(
        'user["password"]',
        required=True,
        location="body",
        schema=coreschema.String()
    ),
    coreapi.Field(
        'user["password_again"]',
        required=True,
        location="body",
        schema=coreschema.String()
    ),
    coreapi.Field(
        'device["onesignal_token"]',
        required=True,
        location="body",
        schema=coreschema.String()
    ),
])


LoginSchema = ManualSchema(fields=[
    coreapi.Field(
        'email',
        required=True,
        location="body",
        schema=coreschema.String()
    ),
    coreapi.Field(
        'password',
        required=True,
        location="body",
        schema=coreschema.String()
    ),
    coreapi.Field(
        "onesignal_token",
        required=True,
        location="body",
        schema=coreschema.String()
    ),
])
