# geo-grab
<!-- TODO Write a README explaining what this script is and how to use it -->
<!-- TODO Outline basic contribution guidelines -->

## Requirements
`PIL`/`pillow`

## Installing
```
git clone https://github.com/finelines-engineering/geo-grab.git
cd geo-grab
```

## Usage
```
$ python geo_grab.py --help
usage: GeoTag Getter [-h] [-v] [-o] [-u] [-k KML] [-z KMZ] [-g GEOJSON] [-c CSV]
                     [--services {google,osm,apple,bing} [{google,osm,apple,bing} ...]]
                     directory

positional arguments:
  directory             Image directory to geolocate

options:
  -h, --help            show this help message and exit
  -v, --verbose         Set verbosity level on command line
  -o, --open            Open a browser tab for each image location and service
  -u, --url             Write the link(s) to Windows url file(s) [one file per chosen service]
  -k KML, --kml KML     If populated, write a kml file with the given name
  -z KMZ, --kmz KMZ     If populated, write a kmz file with the given name
  -g GEOJSON, --geojson GEOJSON
                        If populated, write a geojson file with the given name
  -c CSV, --csv CSV     If populated, write a csv file with the given name
  --services {google,osm,apple,bing} [{google,osm,apple,bing} ...]
                        Optional webmap service to use for location
```

## Features

### URL Files
Use the `-u/--url` option to generate `.url` files for all enabled services

Example:
```
$ python geo_grab.py -u --services google osm
```

### KML
Use the `-k/--kml` option to specify a kml output file in the target directory

Example:
```
$ python geo_grab.py -k
```
**Note:** The output kml will use *relative* references to the images 

### KMZ
Use the `-z/--kmz` option to specify a kmz output file in the target directory

Example:
```
$ python geo_grab.py -z
```
**Note:** The output kmz will contain all tagged images and can be shared 

### GeoJSON
Use the `-g/--geojson` option to specify a geojson output file in the target directory

Example:
```
$ python geo_grab.py -g
```
**Note:** The output geojson features will contain timestamp and absolute filepath info

### CSV
Use the `-c/--csv` option to specify a csv output file in the target directory
Example:
```
$ python geo_grab.py -c
```
**Note:** The output csv contains timestamp, filename, and filepath fields

### Combining
If you wish to specify multiple output types, you have several options:

#### Shared Name
```
$ python geo_grab.py -n $DATE -kgcz
```
#### Individual Names
```
$ python geo_grab.py -k my_kml -g my_geojson -c my_csv -z my_kmz
```
#### Footguns
Specifying output flags only:
```
$ python geo_grab.py -kgcz
```
will lead to the first argument getting the next arguments as its filename (`gcz.kml`) while the rest will get the default `output` (`output.csv`, `output.kmz`, `output.geojson`). Alyways specify a global name if chaining output flags.

Specifying global name *and* per-file names:
```
$ python geo_grab.py -n $DATE -k my_kml -gcz
```
The global name takes precedence over local names. In this case the kml will be `$DATE.kml`

## Additional flags

### `-n/--name`
Set the default name for all output files. This will override specified filenames

### `--verbose`
Emit actions to the terminal

### `--help`
Emit the help/usage message

### `--open`
Open urls for all specified services in browser tabs