#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A simple script that generates a ros dependency file (yaml) for macports
by hashing the current packages in the osx-homebrew.yaml system dependency list
against the available portfiles. 
"""

import os
import sys
import argparse
import yaml

def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rosdep",
                        help="The rosdep yaml file listing the system " \
                        "dependency packages that you want to try to " \
                        "resolve against MacPorts",
                        required=True)
    
    parser.add_argument("--outdep",
                        help="The output rosdep yaml file containing " \
                        "potential macport names",
                        required=True)
    return parser.parse_args()

if __name__ == "__main__":

    args = parseargs()
    ports = '/opt/local/var/macports/sources/rsync.macports.org/' \
        'release/tarballs/ports'
    
    #Walk through and collect all the portnames 
    portnames = []
    for dirname, dirnames, filenames in os.walk(ports):
        #Iterate through all the files
        for filename in filenames:
            if (os.path.join(dirname, filename).find('Portfile') >= 0):
                portnames.append(
                    os.path.split(
                    os.path.split(
                    os.path.join(dirname, filename))[0])[1])

    #Now we have the port names, let's load the ros system dependencies that we
    #need to hack through 
    rosdeps = yaml.load(file(args.rosdep,'r'))
    out_dict = {}
    for rosdep in rosdeps.keys():
        #Check if library:
        port_hits = [] 
        if rosdep.find('lib') == 0: 
            port_hits = [k for k in portnames if rosdep.strip('lib').rstrip('-dev') in k]
            out_dict[rosdep] = {'osx': {'macports': {'packages': port_hits}}}
        elif rosdep.find('python') == 0: 
            port_hits = [k for k in portnames if ('py' + rosdeps.keys()[2].strip('python')) in k]
            out_dict[rosdep] = {'osx': {'macports': {'packages': port_hits}}}
        else:
            port_hits = [k for k in portnames if rosdep in k]
            out_dict[rosdep] = {'osx': {'macports': {'packages': port_hits}}}


 


