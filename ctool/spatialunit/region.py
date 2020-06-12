import json
import math

from shapely.geometry import Point
from shapely.geometry import Polygon

from ctool.gis.distance import point_point_distance
from ctool.gis.coordinates import to_webmercator
from ctool.gis.coordinates import to_geographic

class Region:

    COORDINATES = 1
    FEATURE_COLLECTION = 2

    def __init__(self, geojson_file):
        with open(geojson_file, "r", encoding="utf-8") as js:
            region = json.load(js)
            ring = []
            raw_ring = []
            self.polygons = []
            self.raw_polygons = []

            if "coordinates" in region:
                for lng, lat in region["coordinates"][0][0]:
                    ring.append(to_webmercator(lng, lat))
            else:
                if region["features"][0]["geometry"]["type"] == "Polygon":
                    ps = region["features"][0]["geometry"]["coordinates"]
                    for r in ps:
                        for lng, lat in r:
                            ring.append(to_webmercator(lng, lat))
                            raw_ring.append((lng, lat))

                        self.polygons.append(Polygon(ring))
                        self.raw_polygons.append(Polygon(raw_ring))
                        ring = []
                        raw_ring = []
                else:
                    ps = region["features"][0]["geometry"]["coordinates"]
                    for p in ps:
                        for r in p:
                            for lng, lat in r:
                                ring.append(to_webmercator(lng, lat))
                                raw_ring.append((lng, lat))

                            self.polygons.append(Polygon(ring))
                            self.raw_polygons.append(Polygon(raw_ring))
                            ring = []
                            raw_ring = []

        self.min_lon = self.largest_raw_polygon().bounds[0]
        self.max_lon = self.largest_raw_polygon().bounds[2]
        self.min_lat = self.largest_raw_polygon().bounds[1]
        self.max_lat = self.largest_raw_polygon().bounds[3]
        self.bound = (self.min_lon, self.min_lat, self.max_lon, self.max_lat)
        self.width = point_point_distance((self.min_lon, self.min_lat), (self.max_lon, self.min_lat))
        self.height = point_point_distance((self.min_lon, self.min_lat), (self.min_lon, self.max_lat))
        self.geometry = region["features"][0]["geometry"]

    # def __init__(self, ring, from_ring):
    #     self.polygons = []
    #     self.raw_polygons = []
    #
    #     web_ring = []
    #     for lng, lat in ring:
    #         web_ring.append(self.to_webmercator(lng, lat))
    #
    #     self.polygons.append(Polygon(web_ring))
    #     self.raw_polygons.append(Polygon(ring))
    #
    #     self.min_lon = self.largest_raw_polygon().bounds[0]
    #     self.max_lon = self.largest_raw_polygon().bounds[2]
    #     self.min_lat = self.largest_raw_polygon().bounds[1]
    #     self.max_lat = self.largest_raw_polygon().bounds[3]
    #     self.bound = (self.min_lon, self.min_lat, self.max_lon, self.max_lat)
    #     self.width = point_distance((self.min_lon, self.min_lat), (self.max_lon, self.min_lat))
    #     self.height = point_distance((self.min_lon, self.min_lat), (self.min_lon, self.max_lat))

    def contains(self, lng, lat):
        if not self.in_bound(lng, lat):
            return False
        try:
            point = Point(to_webmercator(lng, lat))
        except Exception:
            # bad coordinates data.txt eg: (700.28, 361.5433)
            return False
        if self.largest_polygon().contains(point):
            return True
        return False

    def in_bound(self, lng, lat):
        if lng < self.min_lon or lng > self.max_lon or lat < self.min_lat or lat > self.max_lat:
            return False
        else:
            return True

    def in_bound_vec(self, lngs, lats):
        # vectorizing in bound
        return lngs.between(self.min_lon, self.max_lon) & lats.between(self.min_lat, self.max_lat)

    def largest_polygon(self):
        return max(self.polygons, key=lambda p: p.area)

    def largest_raw_polygon(self):
        return max(self.raw_polygons, key=lambda p: p.area)