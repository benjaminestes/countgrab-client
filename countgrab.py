#!/usr/bin/python3

import sys
import json
import urllib.request
import csv

KEYLIST = ['Pinterest', 'LinkedIn', 'Facebook like_count', 'StumbleUpon',
           'Facebook share_count', 'Facebook total_count', 'GooglePlusOne', 
           'Delicious', 'Twitter', 'Facebook commentsbox_count', 
           'Facebook click_count', 'Diggs', 'Buzz', 'Facebook comment_count', 'Reddit']

def count_grab(url, strict = True):
    "Grab social metrics for url. Will exit script if it fails unless strict == False."
    request_url = 'http://api.sharedcount.com/?url=' + url

    try:
        api_data = urllib.request.urlopen(request_url)
        api_json = json.loads(api_data.read().decode('utf-8'))
    except:
        if strict:
            exit('Error: Request unsuccessful')
        else:
            return None

    return api_json

def json_pretty(data):
    if data:
        print(json.dumps(data, sort_keys = True, indent = 4))

def linear_data(url, data):
    "SharedCount returns 'two-dimensional' JSON string. This flattens it." 
    flattened = {}

    for i in data:
        if isinstance(data[i], dict):
            for j in data[i]:
                # "Promoted" elements need names derived from the
                # subdictionary key
                label = i + " " + j
                flattened[label] = data[i][j] 
        else:
            flattened[i] = data[i]
    
    # now prepend the url and generate a list ready for csv processing
    url_entry = [url]
    for i in KEYLIST:
        url_entry.append(flattened[i])

    return url_entry

def dump_grab(urls):
    "Iterate over urls and return data as a string."

    out = {}

    for url in urls:
        out[url] = count_grab(url, strict = False) 
    
    # format the output to be json compatible
    out_string = str(out)
    out_string = out_string.replace('\'', '\"')
    out_string = out_string.replace("None", "null")

    return out_string

def bulk_grab(urls):
    "Iterate over urls and return data as a list for CSV."

    out = []
    
    # KEYLIST is based on output from API, we need to add
    # URL as first CSV column
    headerlist = KEYLIST[:]
    headerlist.insert(0, "URL")
    out.append(headerlist)

    for url in urls:
        print("Fetching data for:", url, end="... ")
        try:
            url_data = linear_data(url, count_grab(url, strict = False))
            out.append(url_data)
            print('Data retrieved.')
        except:
            print('Error fetching info.')

    return out

def help():
    print()
    print('Usage: ./countgrab.py [url|list] <resource> (outfile)')
    print()
    print('    url: Return JSON string with social metrics for')
    print('            the URL specified by <resource>. URL')
    print('            must begin with "http://".')
    print('    list: Return a JSON file with social metrics for')
    print('            the list of URLs, in the .txt file specified')
    print('            by resource. One URL per line. If no CSV is')
    print('            specified, dump all data to command line after')
    print('            request is complete.')
    print('    outfile: If specified, write to this CSV instead')
    print('            of the terminal. This is ignored in url mode.')
    print()

def main():

    command = sys.argv[1] if len(sys.argv) > 1 else None
    option = sys.argv[2] if len(sys.argv) > 2 else None
    csvfile = sys.argv[3] if len(sys.argv) > 3 else None

    # If not invoked properly print help and exit
    if not command:
        help()
        sys.exit()

    if command == "url":
        if not option:
            help()
            sys.exit()

        # Human readable output is desirable for the url case
        json_pretty(count_grab(option))

    elif command == "list":
        if not option:
            help()
            sys.exit()

        # Read list of URLs
        urls = []
        with open(option, 'r') as f:
            for line in f:
                urls.append(line.rstrip())

        if not csvfile:
            print(dump_grab(urls))
        else:
            output = bulk_grab(urls)

            print("Writing output CSV.")
            with open(csvfile, 'w', newline='') as c:
                writer = csv.writer(c, delimiter=',',
                                    quotechar='"', 
                                    quoting=csv.QUOTE_MINIMAL)
                writer.writerows(output)

if __name__ == '__main__':
    sys.exit(main())
