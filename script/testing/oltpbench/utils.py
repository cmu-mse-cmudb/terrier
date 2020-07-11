#!/usr/bin/python3

import argparse

def parse_command_line_args():
    '''Command line argument parsing methods'''

    aparser = argparse.ArgumentParser(description="Timeseries")

    aparser.add_argument(
        "--config-file", help="File containing a collection of test cases")
    aparser.add_argument("--db-host", help="DB Hostname")
    aparser.add_argument("--db-port", type=int, help="DB Port")
    aparser.add_argument("--db-output-file", help="DB output log file")
    aparser.add_argument("--build-type",
                         default="debug",
                         choices=["debug", "release", "relwithdebinfo"],
                         help="Build type (default: %(default)s")
    aparser.add_argument("--publish-results", action='store_true',
                         help="Stores performance results in TimeScaleDB")

    args = vars(aparser.parse_args())

    return args

