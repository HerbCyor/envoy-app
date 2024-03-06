from typing import Tuple
import math
import random


def generate_point_from_coordinates(
    central_point_coordinates: Tuple[float, float], radius_from_central_point: int
):
    """
    coords tuple with latitude and longitude values,
    radius in kilometers
    n number of points to be generated (default = 1)

    returns a random coordinates inside the given radius
    """

    earth_radius = 6371000  # Earth's mean radius in meters
    latitude, longitude = central_point_coordinates

    dx = (
        random.randrange(-1000, 1000) * radius_from_central_point
    )  # distance variation in the x axis (randrange *1000 to yield result in meters)
    dy = (
        random.randrange(-1000, 1000) * radius_from_central_point
    )  # distance variation in the y axis (randrange *1000 to yield result in meters)

    # formulas to calculate new coordinate points given dx/dy from the original coords source:stackoverflow
    new_latitude = latitude + (dy / earth_radius) * (180 / math.pi)
    new_longitude = longitude + (dx / earth_radius) * (180 / math.pi) / math.cos(
        latitude * math.pi / 180
    )

    return (
        round(new_latitude, 9),
        round(new_longitude, 9),
    )  # rounds to 9 decimal places, i think even more than 4 is overkill but...
