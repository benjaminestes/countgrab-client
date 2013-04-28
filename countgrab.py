#!/usr/bin/python3

import argparse
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
    "Iterate over urls and return data as a JSON style string."

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

def build_parser():
    parser = argparse.ArgumentParser(description = 'Pull social metrics from SharedCount API')

    command_opts = ['url','list']

    parser.add_argument('command',
                        choices = command_opts,
                        help = 'specify operating mode')

    parser.add_argument('source',
                        help = 'specify a URL or text file as appropriate')

    parser.add_argument('-d', '--dest',
                        help = 'specify an output file; used in list mode')

    return parser

def main():

    parser = build_parser()
    args = parser.parse_args()

    if args.command == "url":
        # Human readable output is desirable for the url case
        json_pretty(count_grab(args.source))

    elif args.command == "list":
        # List mode requires output file
        if not args.dest:
            parser.print_help()
            sys.exit()

        # Read list of URLs
        urls = []
        with open(args.source, 'r') as f:
            for line in f:
                urls.append(line.rstrip())

        output = bulk_grab(urls)

        print("Writing output CSV.")
        with open(args.dest, 'w', newline='') as c:
            writer = csv.writer(c, delimiter=',',
                                quotechar='"', 
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerows(output)

if __name__ == '__main__':
    sys.exit(main())
