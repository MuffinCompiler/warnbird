from config import MapConfig
import requests, shutil, json
from PIL import Image
from io import BytesIO

from nina_event import NinaEvent

def flatten_recursive_lists(S):
    if S == []:
        return S
    if isinstance(S[0], list):
        return flatten_recursive_lists(S[0]) + flatten_recursive_lists(S[1:])
    return S[:1] + flatten_recursive_lists(S[1:])

class BoundingBox:
    def __init__(self, min_lon=0, min_lat=0, max_lon=0, max_lat=0):
        self.min_lon = min_lon
        self.min_lat = min_lat
        self.max_lon = max_lon
        self.max_lat = max_lat

    def set_from_geodata(self, geo_data, scale_factor=1.0):
        # geo_data_json['features']
        features = geo_data['features']

        lonlat_flattened = []
        for feature in features:
            geometry = feature['geometry']

            # flatten to supported nested lists (polygons) and non-nested
            lonlat_flattened = lonlat_flattened + flatten_recursive_lists(geometry['coordinates'])

        self.min_lon = min(lonlat_flattened[::2])
        self.max_lon = max(lonlat_flattened[::2])
        self.min_lat = min(lonlat_flattened[1::2])
        self.max_lat = max(lonlat_flattened[1::2])

        # compensate with scale-factor
        dlon = self.max_lon - self.min_lon
        dlat = self.max_lat - self.min_lat

        self.min_lon -= dlon * (scale_factor - 1.0)
        self.max_lon += dlon * (scale_factor - 1.0)
        self.min_lat -= dlat * (scale_factor - 1.0)
        self.max_lat += dlat * (scale_factor - 1.0)


    def to_mapbox_str(self):
        return f"[{self.min_lon},{self.min_lat},{self.max_lon},{self.max_lat}]"


class MapBox:

    def __init__(self, cfg: MapConfig):
        # initialize API

        # load key
        with open(cfg.key_file, 'r') as file:
            self.token = file.read()

        pass

    def build_url(self, bbox, geo_json, config: MapConfig):
        base_url = config.api_endpoint
        if geo_json is not None:
            trimmed_jsons = json.dumps(geo_json, separators=(',', ':'))
            r = trimmed_jsons.replace('#', '%23')
            base_url += 'geojson(' + r + ")/"
        base_url += bbox.to_mapbox_str() + "/"
        base_url += f"{config.width}x{config.height}"
        if config.double_resolution:
            base_url += "@2x"
        base_url += f"?logo=false"
        base_url += f"&access_token={self.token}"

        return base_url

    def get_map(self, event: NinaEvent, config: MapConfig):
        bbox = BoundingBox()

        if event.geo_data is None:
            print("No geodata, cant create map.")
            return None
        bbox.set_from_geodata(event.geo_data, scale_factor=config.scale)

        url = self.build_url(bbox, event.geo_data, config)

        print(url)

        if config.test_mode:
            return None

        response = requests.get(url)

        # TODO do we want to cache images?
        if not response.ok:
            print("Couldnt get image, status code not ok." + str(response.status_code))
            return None

        img = Image.open(BytesIO(response.content))
        img.save(event.summary['id'] + '.png')

        return img

