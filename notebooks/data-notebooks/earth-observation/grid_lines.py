import numpy as np
import osr


def get_meters(lat, lon):
    """
    Transfrom coords from Sentinel to MODIS
    """

    # Get spatial reference
    wgs84 = osr.SpatialReference()
    # and initialize it by EPSG
    wgs84.ImportFromEPSG(4326)
    modis_sinu = osr.SpatialReference()
    # initialize by a string
    modis_sinu.ImportFromProj4("+proj=sinu +R=6371007.181 +nadgrids=@null +wktext")
    # define coordinate transformation
    # in this case from WGS84 to MODIS sinusoidal
    tx = osr.CoordinateTransformation(wgs84, modis_sinu)
    # transform couple of coordinates to MODIS
    mx, my, mz = tx.TransformPoint(lon, lat)

    return mx, my



def get_pixels(geo, lat, lon):
    """
    Get pixel coordinates by given latitude, longitude and geotransformation

    Parameters
    ----------
    geo: array
        geo-transformation, usually obtained by gdal.GetGeoTransform()
    lat: float
        latitude
    lon: float
        longitude

    Returns
    -------
    px: int
        x pixel coordinate
    py: int
        y pixel coordinate

    """
    if  True in (np.array(geo) > 1000):
        # print 'meters'
        mx, my = get_meters(lat, lon)
        py = int(np.round((my - geo[3]) / (geo[5])))
        px = int(np.round((mx - geo[0]) / geo[1]))
        # print px_0, px_1, py_0, py_1
    else:
        # print 'lat-lon'
        py = int(np.round((lat - geo[3]) / (geo[5])))
        px = int(np.round((lon - geo[0]) / geo[1]))

    return px, py



def line_intersection(line1, line2, size_x, size_y):
    """

    Parameters
    ----------
    line1
    line2

    Returns
    -------

    """
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])  # Typo was here

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        # print Exception('lines do not intersect')
        return 0, 0

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div

    condition1 = np.any(np.array([x, y]) > (size_x+1))
    condition2 = np.any(np.array([x, y]) < -1)
    # print condition1, condition2
    if np.logical_or(condition1, condition2):
        # print Exception('lines do not intersect')
        return 0, 0

    return x, y

    # print line_intersection((A, B), (C, D))



def find_inter(x1, x2, y1, y2, size_x, size_y):
    """

    Parameters
    ----------
    x1
    x2
    y1
    y2

    Returns
    -------

    """
    line1 = [[x1, y1], [x2, y2]]
    line2 = [[size_x+1, 0], [size_x+1, size_y]]
    x3, y3 = line_intersection(line1, line2, size_x, size_y)
    if np.logical_and(x3!=0, y3!=0):
        if np.logical_or(x2 > size_x, y2 > size_y):
            x2 = x3
            y2 = y3
        elif np.logical_or(x1 > size_x, y1 > size_y):
            x1 = x3
            y1 = y3
    #print 'line2'
    line2 = [[-1, 0], [-1, size_x]]
    x3, y3 = line_intersection(line1, line2, size_x, size_y)
    if np.logical_and(x3!=0, y3!=0):
        #print 'interception'
        if np.logical_or(x2<0, y2<0):
            x2 = x3
            y2 = y3
        elif np.logical_or(x1<0, y1<0):
            x1 = x3
            y1 = y3
    return x1, x2, y1, y2



# import matplotlib.pyplot as plt
# import netCDF4 as nc
# ds = nc.Dataset('/home/ucfamc3/max_python/data/baci_wp2_files/lst_h18v04_2015_7day.nc')
# crs_proj = ds['crs'].spatial_ref
# crs_geo = ds['crs'].GeoTransform
#
# img = ds['lst'][0,:,:]
#
# fig = plt.figure(figsize=(15, 15))
# plt.imshow(img)
#
# print np.min(ds['lat']), np.max(ds['lat'])
# print np.min(ds['lon']), np.max(ds['lon'])
#
# lat_max = np.round(np.max(ds['lat'])).astype(int)
# lat_min = np.round(np.min(ds['lat'])).astype(int)
# lon_min = np.round(np.min(ds['lon'])).astype(int)
# lon_max = np.round(np.max(ds['lon'])).astype(int)
#
# for lon in xrange(lon_min, lon_max, 2):
#     x1, y1 = get_pixels(crs_geo, lat_max, lon)
#     x2, y2 = get_pixels(crs_geo, lat_min, lon)
#     x1, x2, y1, y2 = find_inter(x1, x2, y1, y2, img.shape[0], img.shape[1])
#     plt.plot([x1, x2], [y1, y2], c='k')
#
# # lon = 15
# for lat in xrange(lat_min, lat_max, 2):
#     x1, y1 = get_pixels(crs_geo, lat, lon_max)
#     x2, y2 = get_pixels(crs_geo, lat, lon_min)
#     x1, x2, y1, y2 = find_inter(x1, x2, y1, y2, img.shape[0], img.shape[1])
#     plt.plot([x1, x2], [y1, y2], c='k')
#
# plt.show()