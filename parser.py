#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A simple script to take a set of packages in a ROS workspace and conver them
into a set of macports ports with a fully working dependency tree.
"""

import os
import sys
from xml.dom import minidom as xml


def readfile(file):
    with open(file) as f:
        return "".join(f.readlines())


def writefile(fname, data):
    with open(fname, "w") as f:
        f.write(data)


if __name__ == "__main__":
    pkgs = [pkg for pkg in os.listdir(".") if
            not pkg.startswith(".") and os.path.isdir(pkg)]
    prefix = "ros-hydro-"
    portdir = sys.argv[1] if len(sys.argv) > 1 else ".."
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
        template = template.replace("$$name$$", pkgname)
        template = template.replace("$$run_depends$$", run_deps_str)
        template = template.replace("$$build_depends$$", build_deps_str)

        # Make ports
        if not os.path.exists(portdir + "/ports"):
            os.mkdir(portdir + "/ports")
        if not os.path.exists(portdir + "/ports/" + pkgname):
            os.mkdir(portdir + "/ports/" + pkgname)
        writefile(portdir + "/ports/" + pkgname + "/Portfile", template)

        # Make tarballs
        if not os.path.exists(portdir + "/tarballs"):
            os.mkdir(portdir + "/tarballs")
        os.system(
            "tar -zcvf {0}.tar.gz {1}".format(portdir + "/tarballs/" + pkgname,
                                              pkg))

