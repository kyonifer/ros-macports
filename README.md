ros-macports
============

Simple instructions on how to use these scripts to generate the ros portfiles found in other branches.

1) Grab the desired .rosinstall from the rosinstall-snapshots branch (they are timestamped MMDDYYYY).
2) Run "wstool init -j1 <some_directory> <foo>.rosinstall", where foo is the rosinstall file you got in #1 and some_directory is where you want to dump all the ROS source.
3) Delete all .git folders and the opencv2 folder.
4) Copy the scripts found here into some_directory.
5) Run parser.py. This will make a directory called some_directory/../ports and will generate a huge number of port files, one for each package still in some_directory.
6) Copy the ports into a macports index.