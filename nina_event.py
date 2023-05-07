from enum import Enum
import json

# TODO these strings are all over the place
class EventSource(str, Enum):
    biwapp = 'biwapp'
    dwd = 'dwd'
    katwarn = 'katwarn'
    lhp = 'lhp'
    mowas = 'mowas'
    police = 'police'


def is_clockwise(coordinate_list):
    # https://stackoverflow.com/questions/1165647/how-to-determine-if-a-list-of-polygon-points-are-in-clockwise-order
    edge_sum = 0
    for i in range(len(coordinate_list) - 1):
        dx = coordinate_list[i + 1][0] - coordinate_list[i][0]
        dy = coordinate_list[i + 1][1] - coordinate_list[i][1]
        edge_sum += dx * dy
    return edge_sum < 0 # TODO src has inverse, but we need it other way around?


def is_counterclockwise(coordinate_list):
    return not is_clockwise(coordinate_list)


class NinaEvent:

    def __init__(self, source, summary, details, geo_data):
        self.source = source
        self.summary = summary
        self.details = details
        self.geo_data = geo_data

        if self.geo_data is not None:
            self.fix_geo_data()

    def fix_geo_data(self):
        # Mapbox has simpler spec -> adapt to it
        # https://github.com/mapbox/simplestyle-spec
        # supported properties:
        # title, description, marker-size, marker-symbol, marker-color for markers
        # stroke, stroke-opacity, stroke-width, fill, fill-opacity for polys

        features = self.geo_data['features']
        feature_sizes = []
        for feature in features:
            poly_sizes = []

            properties = feature['properties']  # TODO if crash here log with file.

            # rename attributes
            properties['stroke'] = properties.pop('strokeColor')
            properties['stroke-opacity'] = properties.pop('strokeOpacity')
            properties['stroke-width'] = properties.pop('strokeWeight')
            properties['fill'] = properties.pop('fillColor')
            properties['fill-opacity'] = properties.pop('fillOpacity')

            geometry = feature['geometry']
            if geometry['type'] != 'Polygon':
                feature_sizes.append(poly_sizes)
                continue

            for i, coordinate_list in enumerate(geometry['coordinates']):
                poly_sizes.append(len(coordinate_list))
                # first list (i=0) is shape, needs to be ccw.
                # inner holes (i>0) needs to be cw.
                if (i == 0 and is_clockwise(coordinate_list)) or (i > 0 and is_counterclockwise(coordinate_list)):
                    print(f"Reverse {i}")
                    geometry['coordinates'][i] = list(reversed(coordinate_list))

            feature_sizes.append(poly_sizes)

        # if too long, reduce file size. URL can be max 8000, do max 7000 for geojson
        cur_len = len(json.dumps(self.geo_data))
        while cur_len > 7000:
            print(f"JSON too long {cur_len}, reducing...")

            # get the polygon with most nodes
            max_poly_per_feature = list(map(max, feature_sizes))
            feature_idx = max_poly_per_feature.index(max(max_poly_per_feature))

            max_geometry = features[feature_idx]['geometry']
            max_geometry_sizes = feature_sizes[feature_idx]
            max_poly_index = max_geometry_sizes.index(max(max_geometry_sizes))

            max_poly = max_geometry['coordinates'][max_poly_index]
            # reduce by 10%
            del max_poly[9:-2:10] # delete every 10th, not last

            feature_sizes[feature_idx][max_poly_index] = len(max_poly)

            cur_len = len(json.dumps(self.geo_data))


