# Countgrab

_**Notice!** Before you use this script please know that you 
should adhere to its limit of [100,000 API requests per 
day](http://sharedcount.com/documentation.php)!_

A script to grab social metrics from the SharedCount API.  
Requires Python &ge; 3.2.

## Usage

```
usage: countgrab.py [-h] [-d DEST] {url,list} source

Pull social metrics from SharedCount API

positional arguments:
  {url,list}            specify operating mode
  source                specify a URL or text file as appropriate

optional arguments:
  -h, --help            show this help message and exit
  -d DEST, --dest DEST  specify an output file; used in list mode
```

### Example

```
countgrab.py list urls.txt -d outfile.csv
```

## Thanks

Special thanks go obviously to [Yahel Carmon](http://yahelc.com/) 
for developing [SharedCount](http://sharedcount.com/)! And check 
out [Distilled](http://www.distilled.net/) (no affiliation with 
Yahel Carmon or SharedCount), as I'm a member of the Distilled 
team and this was written primarily for their benefit.
