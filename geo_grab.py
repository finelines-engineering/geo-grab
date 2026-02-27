from typing import Literal
import subprocess
import sys
from argparse import ArgumentParser
from pathlib import Path
import webbrowser

# TODO: Do not install packages unless the user asks for it
# Best way to do this is to specify an argument that runs the pip install
try:
    from PIL import Image
except (ModuleNotFoundError, ImportError):
    pass


HAS_PIL = 'PIL' in sys.modules


# Internal type aliases
type GPSInfo = dict[int, Any]
type Latitude = float
type Longitude = float
type Coordinates = tuple[Latitude, Longitude]
type PointInfo = list[tuple[Path, Coordinates, float, str]]

# Literal options
Service = Literal['google', 'osm', 'apple', 'bing']
Services: tuple[Service, ...] = get_args(Service)
Format = Literal['shp', 'kml']
Formats: tuple[Format, ...] = get_args(Format)


def _install_pillow():
    print(f'installing PIL for {sys.executable}')
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'pillow'])
    sys.modules['PIL.Image'] = __import__('PIL', fromlist=['Image'])


def dms_to_dd(d: float, m: float, s: float, b: Literal['N', 'S', 'E', 'W']) -> float:
    """Convert DMS coordiantes to Decimal Degrees

    Args:
        d: Degrees component
        m: Minutes component
        s: Seconds component
        b: Bearing of the coordinate (`NSEW`)

    Returns:
        The Lat/Lon value in Decimal Degrees (float)

    Example:
        ```python
        >>> dms_to_dd(95, 12, 100, 'E')
        95.22777777777777
    """
    dd = float(d) + float(m) / 60 + float(s) / 3600
    if b in 'NE':
        return dd
    else:
        return -1 * dd


# TODO: Add a docstring to this function
def get_geo_exif(img: Path, o: bool) -> None:
    i = Image.open(str(img))
    
    # TODO: Hide behind --verbose flag
    print(img.name)
    
    # TODO: Use a cleaner method of getting the tag info. There are documented methods 
    # in PIL for accessing nested EXIF tags https://pillow.readthedocs.io/en/latest/reference/Image.html#PIL.Image.Exif
    try:
        lat_dir, (lat_d, lat_m, lat_s), lon_dir, (lon_d, lon_m, lon_s) = (
            i.getexif().get_ifd(34853).values()
        )
        
    # TODO: Narrow Exception Handling (or remove altogether) and provide logging/printing only when --verbose is set
    except Exception:
        print('\tFailed to get Exif')
        return
    
    lat = dms_to_dd(lat_d, lat_m, lat_s, lat_dir)
    lon = dms_to_dd(lon_d, lon_m, lon_s, lon_dir)
    
    # TODO: Allow opening in other webmap services?
    url = f'https://www.google.com/maps/search/?api=1&query={lat},{lon}'
    if o:
        webbrowser.open(url)
    
    # TODO: Move this to a seperate function and allow exporting in other formats
    # each format should have its own function and be exposed as a flag to the ArgumentParser
    with open(img.with_suffix('.url'), 'wt') as u_file:
        u_file.write('[InternetShortcut]\n')
        u_file.write(f'URL={url}\n')
    
    # TODO: Hide this behind a --verbose/-v flag in the ArgumentParser
    print(f'\t{lat_d}°{lat_m}\'{lat_s}"{lat_dir}, {lon_d}°{lon_m}\'{lon_s}"{lon_dir}')


def main(folder: Path, o: bool):
    # TODO: Allow other image formats?
    for img in folder.glob('*.jp*g'):
        get_geo_exif(img, o)


if __name__ == '__main__':
    # TODO: Add a flag for toggling .url file export
    # TODO: Add --verbose flag
    # TODO: Add service options (google, osm, shapefile, kml, etc.)
    parser = ArgumentParser('GeoTag Getter')
    parser.add_argument('directory', help='Image directory to geolocate')
    parser.add_argument(
        '-o',
        '--open',
        action='store_true',
        default=False,
        help='Open a Google Maps browser tab for each image location',
    )
    if not HAS_PIL:
        # TODO: Handle PIL not being installed (accept a command line flag for installation)
        # If that flag is not passed, print a warning message to the user stating that PIL is
        # required and they can install it using the specified flag
        #
        # NOTE: This option should only be available if the user DOES NOT have PIL installed
        ...

    args = parser.parse_args()

    if not HAS_PIL and args.install:
        _install_pillow()

    main(Path(args.directory), args.open)
