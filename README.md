# Countgrab

_**Notice!** Before you use this script please know that you should adhere to its limit of [100,000 API requests per day](http://sharedcount.com/documentation.php)!_

A script to grab social metrics from the SharedCount API. Uses Python 3.

Basically, if you run this script as `./countgrab.py url http://www.google.com`, a JSON string will be output directly from the SharedCount API to your console. If you make a text file `urls.txt` which has one URL per line, you can run `./countgrab.py list urls.txt out.csv` to get a handy CSV file with all of the fields that SharedCount provides.

## Usage

```
./freecounts.py [url|list] <resource> (outfile)

    url: Return JSON string with social metrics for
            the URL specified by <resource>. URL
            must begin with "http://".
    list: Return a JSON file with social metrics for
            the list of URLs, in the .txt file specified
            by resource. One URL per line. If no CSV is
            specified, dump all data to command line after
            request is complete.
    outfile: If specified, write to this CSV instead
            of the terminal. This is ignored in url mode.
```

## Thanks

Special thanks go obviously to [Yahel Carmon](http://yahelc.com/) for developing [SharedCount](http://sharedcount.com/)! And check out [Distilled](http://www.distilled.net/) (no affiliation with Yahel Carmon or SharedCount), as I'm a member of the Distilled team and this was written primarily for their benefit.
