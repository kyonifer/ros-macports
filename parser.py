# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
A simple script to take a set of packages in a ROS workspace and conver them
into a set of macports ports with a fully working dependency tree.
"""

import os
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
    try:
        os.mkdir("../ports")
    except OSError:
        pass
    for pkg in pkgs:
        pkgname = prefix + pkg
        manifest = xml.parse(pkg + "/package.xml")
        build_deps = [prefix+ele.lastChild.nodeValue for ele in
                      manifest.getElementsByTagName("build_depend")]
        build_deps_str = " \\\n                    port:".join(build_deps)
        if build_deps_str is not "":
            build_deps_str = "\\\n                    port:" + build_deps_str
        run_deps = [prefix+ele.lastChild.nodeValue for ele in
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
        try:
            os.mkdir("../ports/" + pkgname)
        except OSError:
            pass
        writefile("../ports/" + pkgname + "/Portfile", template)