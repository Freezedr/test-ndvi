import math

from pymodis import downmodis
from pyproj import Proj, Transformer

VERTICAL_TILES = 18
HORIZONTAL_TILES = 36
EARTH_RADIUS = 6371007.181
EARTH_WIDTH = 2 * math.pi * EARTH_RADIUS

TILE_WIDTH = EARTH_WIDTH / HORIZONTAL_TILES
TILE_HEIGHT = TILE_WIDTH

wgs84_proj = Proj('EPSG:4326')
modis_grid = Proj(f'+proj=sinu +R={EARTH_RADIUS} +nagrids=@null '
                  f'+ellps=WGS84 +wktext')

transformer = Transformer.from_proj(wgs84_proj, modis_grid, always_xy=True)


def wgs84_to_modis_tile(xx, yy):
    x, y = transformer.transform(xx, yy)
    h = (EARTH_WIDTH * .5 + x) / TILE_WIDTH
    v = (VERTICAL_TILES * TILE_HEIGHT - y - EARTH_WIDTH * .25) / TILE_HEIGHT
    return f'h{int(h)}v{int(v):02},'


modisOgg = downmodis.downModis(
    user='ndvitest',
    password='LtnQy998yTQLdBd',
    destinationFolder='/home/artem/Code/ndvi-test/modis_data',
    tiles=wgs84_to_modis_tile(127.551270, 35.793457),
    product='MOD09GA.006', delta=0,
    today='2021-02-09', enddate='2021-02-09', jpg=True
)

modisOgg.connect()
if modisOgg.nconnection <= 20:
    modisOgg.downloadsAllDay(clean=True, allDays=False)
