from ctool.spatialunit.region import Region
from ctool.gis.distance import point_point_distance

import numpy as np

class Grid:
        
    def init_by_region(self, city_geojson=None, region=None, extra_dims=None, size=1000):
        assert (not city_geojson or not region)
        if not region:
            self.region = Region(city_geojson)
        else:
            self.region = region
        
        self.init_by_boundary(self.region.min_lat, self.region.max_lat, self.region.min_lon, self.region.max_lon, extra_dims, size)
        return self

    def init_by_boundary(self, min_lat, max_lat, min_lon, max_lon, extra_dims=None, size=1000):

        self.width = point_point_distance((min_lon, min_lat), (max_lon, min_lat))
        self.height = point_point_distance((min_lon, min_lat), (min_lon, max_lat))
        
        self.num_col = int(np.ceil(self.width / size))
        self.num_row = int(np.ceil(self.height / size))

        self.cols = np.linspace(min_lon, max_lon, num=self.num_col)
        self.rows = np.linspace(max_lat, min_lat, num=self.num_row)

        # create matrix
        if extra_dims:
            self.tensor = np.zeros((self.num_row, self.num_col, *extra_dims))
        else:
            self.tensor = np.zeros((self.num_row, self.num_col))
        return self


    def get_row_index(self, lat):
        return np.searchsorted(self.rows, [lat])[0] - 1

    def get_col_index(self, lon):
        return np.searchsorted(self.cols, [lon])[0] - 1

    def get_index(self, lon, lat):
        return self.get_col_index(lon), self.get_row_index(lat)

    def get_all_index(self, lons, lats):
        return np.searchsorted(self.rows, np.array(lats)) - 1, np.searchsorted(self.cols, np.array(lons)) - 1

    def gps_in_grid(self, lon, lat):
        return (lon<=self.region.max_lon) and (lon>self.region.min_lon) and (lat<=self.region.max_lat) and (lat>self.region.min_lat)

    def index_in_grid(self, row_id, col_id):
        if (col_id >= self.num_col) or (col_id < 0) or (row_id >= self.num_row) or (row_id < 0):
            return False
        else:
            return True

    def get_coordinates_from_grid_index(self, row_id, col_id):
        if row_id == 0 or col_id == 0 or row_id >= self.num_row-1 or col_id >= self.num_col-1:
            return None
        return self.rows[row_id], self.cols[col_id], self.rows[row_id+1], self.cols[col_id+1]