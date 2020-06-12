from math import sin, cos, atan2, sqrt, degrees, radians, pi

from geopy import Point
from geopy.distance import distance

def point_point_distance(p1, p2):
    """
    Calculate distance from point to point
    :param p1: (lon, lat)
    :param p2: (lon, lat)
    :return: meters
    """
    a = Point(latitude=p1[1], longitude=p1[0])
    b = Point(latitude=p2[1], longitude=p2[0])
    return distance(a, b).m

def sequence_distance(seq, lon_index=0, lat_index=1):
    """
    Distance of (lon, lat) sequence
    :param G:
    :param seq:
    :return:
    """
    length = 0
    for i in range(len(seq) - 1):
        d = point_point_distance((seq[i][lon_index], seq[i][lat_index]),
                           (seq[i+1][lon_index], seq[i+1][lat_index]))
        length += d
    return length