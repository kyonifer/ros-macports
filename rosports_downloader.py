#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A simple script that takes in a .rosinstall file as input, along with a desired
workspace directory and downloads a ros distribution
"""

import os
import sys
import argparse
import requests
import yaml

def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rosinstall",
                        help="The .rosinstall file listing the ros packages" \
                        "that you wish to download",
                        required=True)

    parser.add_argument("--workspace",
                        "-w",
                        help="the directory for the downlaoded ros packages",
                        nargs="?",
                        default="../ports")
    return parser.parse_args()

def download_file(url, dl_path):
    local_filename = os.path.join(dl_path, url.split('/')[-2] + '-' + url.split('/')[-1])
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
    return local_filename


if __name__ == "__main__":

    args = parseargs()
    dl_path = os.path.abspath(args.workspace)

    #Get Rosports file
    ros_pkgs = yaml.load(file(args.rosinstall,'r'))
    for rp in ros_pkgs:
        url = rp['git']['uri'][0:-4] + '/archive/' +  rp['git']['version'] + '.tar.gz'
        print "Downloading %s" % url
        download_file(url, dl_path)


