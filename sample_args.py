#!/usr/bin/python

import sys, getopt

def main(argv):
    src_loc = ''
    dst_loc = ''   
    try:
        opts, args = getopt.getopt(argv, "hd:s", ["sloc=","dloc="])
    except getopt.GetoptError:
        print 'generate_traffic.py -s <traffic_source_location> -d <traffic_destination_location>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'generate_traffic.py -s <traffic_source_location> -d <traffic_destination_location>'
            sys.exit()
        elif opt in ("-s", "--sloc"):
            src_loc = arg
        elif opt in ("-d", "--dloc"):
            dst_loc = arg
    print 'Source Location for traffic generation is: ', src_loc
    print 'Destination Location for traffic end is: ', dst_loc

if __name__ == "__main__":
    main(sys.argv[1:])
