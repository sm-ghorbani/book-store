import os

DEFAULT_RENDERER_CLASSES = ("rest_framework.renderers.JSONRenderer",)
if os.getenv("DEBUG", default=True):
    DEFAULT_RENDERER_CLASSES += ("rest_framework.renderers.BrowsableAPIRenderer",)

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("user.authentication.CustomJWTAuthentication",),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_RENDERER_CLASSES": DEFAULT_RENDERER_CLASSES,
}
