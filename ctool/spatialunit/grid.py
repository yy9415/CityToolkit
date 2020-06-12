from ctool.spatialunit.region import Region
import numpy as np

class Grid:

    def __init__(self, city_geojson=None, region=None, size=1000):
        assert (not city_geojson or not region)
        if not region:
            self.region = Region(city_geojson)
        else:
            self.region = region
        self.width = self.region.width
        self.height = self.region.height
        self.num_col = int(np.ceil(self.width / size))
        self.num_row = int(np.ceil(self.height / size))
        self.cols = np.linspace(region.max_lon, region.min_lon, num=self.num_col)
        self.rows = np.linspace(region.max_lat, region.min_lat, num=self.num_row)

        # create matrix
        self.matrix = {}
        for i in range(self.num_row):
            if i not in self.matrix:
                self.matrix[i] = {}
            for j in range(self.num_col):
                if j not in self.matrix[i]:
                    self.matrix[i][j] = []

    def init_cell(self, fun):
        for i in range(self.num_row):
            for j in range(self.num_col):
                self.matrix[i][j] = fun()

    def get_row_index(self, lat):
        return np.searchsorted(-self.rows, [-lat])[0]

    def get_col_index(self, lon):
        return np.searchsorted(-self.cols, [-lon])[0]

    def get_index(self, lon, lat):
        return self.get_col_index(lon), self.get_row_index(lat)

    def get_all_index(self, lons, lats):
        return np.searchsorted(-self.cols, -np.array(lons)), np.searchsorted(-self.rows, -np.array(lats))

    def gps_in_grid(self, lon, lat):
        return (lon<=self.region.max_lon) and (lon>self.region.min_lon) and (lat<=self.region.max_lat) and (lat>self.region.min_lat)

    def index_in_grid(self, row_id, col_id):
        if (col_id >= self.num_col) or (col_id == 0) or (row_id >= self.num_row) or (row_id==0):
            return False
        else:
            return True