import googlemaps
from dotenv import load_dotenv

from .coordinates import generate_point_from_coordinates
import os

load_dotenv()
gmaps = googlemaps.Client(os.environ.get("GOOGLEMAPS_API_KEY"))


def get_address_from_geolocation(coords):
    """
    'route' = street name
    'administrative_area_level_2' = state
    'administrative_area_level_1' = city

    """
    #####CHECAR LINHA VAZIA#####
    lat, long = coords
    reverse_geocode_result = gmaps.reverse_geocode((lat, long))
    address_dict = {
        "street_number": "n/a",
        "route": "n/a",
        "sublocality": "n/a",
        "administrative_area_level_2": "n/a",
        "administrative_area_level_1": "n/a",
        "country": "n/a",
        "postal_code": "n/a",
    }
    for key in address_dict.keys():
        try:
            for data in reverse_geocode_result[0]["address_components"]:
                if key in data["types"]:
                    address_dict[key] = data["short_name"]

        except:
            print(reverse_geocode_result)

    return address_dict


def get_geolocation_from_address(address: str):
    ##################TO DO : TRY/EXCEPT NOT FOUND #######################
    geocode_result = gmaps.geocode(address)
    latitude = geocode_result[0]["geometry"]["location"]["lat"]
    longitude = geocode_result[0]["geometry"]["location"]["lng"]

    return (latitude, longitude)


def get_zipcode_from_address(address):
    search_result = gmaps.find_place(address, "textquery")
    result = [gmaps.place(i["place_id"]) for i in search_result["candidates"]]
    zip_code = None
    try:
        for component in result[0]["result"]["address_components"]:
            if "postal_code" in component["types"]:
                zip_code = component["long_name"]
    except:
        zip_code = "não encontrado"
    return zip_code


def validate_address(address_dict):
    """return True if address has street number and street name"""

    if address_dict["postal_code"] == "n/a":
        return False

    if address_dict["street_number"] == "n/a" and address_dict["route"] == "n/a":
        return False
    else:
        return True


def validate_geolocation(coords):
    "returns an address if coords are valid, and False if not"
    nearest_roads = gmaps.nearest_roads(coords)
    try:
        nearest_road_coords = (
            nearest_roads[0]["location"][["latitude"]],
            nearest_roads[0]["location"][["longitude"]],
        )
        validated_address = get_address_from_geolocation(nearest_road_coords)
        if validate_address(validated_address):
            return validated_address
        else:
            return False
    except:
        return False


def random_addresses_from_central_geolocation(quantity, center_coords, radius):

    address_list = []
    i = 0
    while i < quantity:
        random_coord = generate_point_from_coordinates(
            central_point_coordinates=center_coords, radius_from_central_point=radius
        )
        address_dict = get_address_from_geolocation(random_coord)

        if not validate_address(address_dict):
            address_dict = validate_geolocation(random_coord)
            if address_dict:
                address_list.append(address_dict)
                i += 1
        else:
            address_list.append(address_dict)
            i += 1

    return address_list
