import pytest

import json

from spatiounit.region import Region


def test_contains():
    geojson = json.load(
        open("/Users/yuyang/Dropbox/Projects/StateMobility/data/map/city/shenzhen.geojson", 'r', encoding="utf-8"))
    ring = geojson["features"][0]["geometry"]["coordinates"][0][0]
    shenzhen = Region(ring)
    assert shenzhen.contains(113.975613, 22.598209) == True