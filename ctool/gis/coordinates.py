import math

def to_webmercator(lng, lat):
        """
        geographic to web mercator
        :param lng:
        :param lat:
        :return:
        """
        if abs(lng) > 180 or abs(lat) > 90:
            return
        num = lng * 0.017453292519943295
        x = 6378137.0 * num
        a = lat * 0.017453292519943295
        return int(x), int(3189068.5 * math.log((1.0 + math.sin(a)) / (1.0 - math.sin(a))))


def to_geographic(lng, lat):
    """
    web mercator to geographic
    :param lng:
    :param lat:
    :return:
    """
    if abs(lng) < 180 and abs(lat) < 90:
        return
    if abs(lng) > 20037508.3427892 or abs(lat) > 20037508.3427892:
        return
    x = lng
    y = lat
    num3 = x / 6378137.0
    num4 = num3 * 57.295779513082323
    num5 = math.floor((num4 + 180.0) / 360.0)
    num6 = num4 - (num5 * 360.0)
    num7 = 1.5707963267948966 - (2.0 * math.atan(math.exp((-1.0 * y) / 6378137.0)))
    return round(num6, 6), round(num7 * 57.295779513082323, 6)