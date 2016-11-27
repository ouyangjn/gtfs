#!/usr/bin/python

# This script looks up tripid and blockid from tatripid and tablockid
#   input: <date>-vehicle-strip.txt
#   output: rows of vehicle locations (json objects)
#

import json
import io
import sys


def main():
  if len(sys.argv) < 2:
    print "Error: no input file given"
    print "Usage: %s <date>-vehicle-strip.txt" % sys.argv[0]
    return

  input_fname = sys.argv[1]
  with open(input_fname) as data_file:    
    for line in data_file:
      vehicle = json.loads(line)
      route = vehicle[u'rt']
      # pattern_id = vehicle[u'pid'] # did not find a matching field in GTFS
      tatripid = vehicle[u'tatripid']
      tablockid = vehicle[u'tablockid']
      print route, "|", tatripid, "|", tablockid


if __name__ == "__main__":
    main()
