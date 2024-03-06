from django.urls import path
from . import views

urlpatterns = [
    path("", views.geolocation, name="geolocation"),
    path("generate_points", views.generate_points, name="generate-points"),
    path(
        "address_from_geolocation",
        views.address_from_geolocation,
        name="address-from-geolocation",
    ),
    path(
        "geolocation_from_address",
        views.geolocation_from_address,
        name="geolocation-from-address",
    ),
]
