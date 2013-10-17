#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A simple script to take a set of packages in a ROS workspace and conver them
into a set of macports ports with a fully working dependency tree.
"""

import os
import sys
import argparse
from xml.dom import minidom as xml


def readfile(file):
    with open(file) as f:
        return "".join(f.readlines())


def writefile(fname, data):
    with open(fname, "w") as f:
        f.write(data)


def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tar_dir",
                        help="the directory for the generated " \
                             "tarballs. if not specified, defaults to " \
                             "../tarballs",
                        nargs="?",
                        default="../tarballs")

    parser.add_argument("--port_dir",
                        help="the directory for the generated ports. if not " \
                             "specified, defaults to ../ports",
                        nargs="?",
                        default="../ports")
    parser.add_argument("--ports-only",
                        help="only generate portfiles",
                        action="store_true")
    parser.add_argument("--tarballs-only",
                        help="only generate tarballs",
                        action="store_true")
    return parser.parse_args()


if __name__ == "__main__":

    args = parseargs()

    pkgs = [pkg for pkg in os.listdir(".") if
            not pkg.startswith(".") and os.path.isdir(pkg)]
    prefix = "ros-hydro-"
    portdir = args.port_dir
    tardir = args.tar_dir
    try:
        os.mkdir(portdir)
    except OSError:
        pass
    for pkg in pkgs:
        pkgname = prefix + pkg
        manifest = xml.parse(pkg + "/package.xml")
        build_deps = [prefix + ele.lastChild.nodeValue for ele in
                      manifest.getElementsByTagName("build_depend")]
        if pkg != "catkin":
            build_deps.append(prefix + "catkin")
        build_deps_str = " \\\n                    port:".join(build_deps)
        if build_deps_str is not "":
            build_deps_str = "\\\n                    port:" + build_deps_str
        run_deps = [prefix + ele.lastChild.nodeValue for ele in
                    manifest.getElementsByTagName("run_depend")]
        run_deps_str = " \\\n                    port:".join(run_deps)
        if run_deps_str is not "":
            run_deps_str = "\\\n                    port:" + run_deps_str
        print (pkgname + " run_depends: " + run_deps_str)
        print (pkgname + " build_depends: " + build_deps_str)

        template = readfile("Portfile-template")
        template = template.replace("$$fullname$$", pkgname)
        template = template.replace("$$name$$", pkg)
        template = template.replace("$$run_depends$$", run_deps_str)
        template = template.replace("$$build_depends$$", build_deps_str)

        # Make ports
        if not os.path.exists(portdir):
            os.mkdir(portdir)
        if not os.path.exists(portdir + "/" + pkgname):
            os.mkdir(portdir + "/" + pkgname)
        writefile(portdir + "/" + pkgname + "/Portfile", template)

        # Make tarballs
        if not os.path.exists(tardir):
            os.mkdir(tardir)
        os.system(
            "tar -zcvf {0}.tar.gz {1}".format(tardir + "/" + pkgname, pkg))
