ros-macports
============

ROS Portfiles for installation of ros on OS X.

Using This Repository
=====================
The following steps will allow you to use the portfiles in this repository with your local macports installation. Please replace /Users/kyonifer with your local home directory as appropriate.

1. Clone the repository locally:

	$ cd ~

	$ git clone https://github.com/kyonifer/ros-macports.git

2. Edit /opt/local/etc/macports/sources.conf to include the path to the local clone:

	file:///Users/kyonifer/ros-macports

	Be sure that this line is above the rsync:// line.

3. Make sure that python is installed and set as the default system interpreter:

	$ sudo port install python27
	$ sudo port select --set python python27

4. At this point, you should be good to start installing ports. A good place to start might be ros-hydro-roslaunch, which brings roscore & friends:

	$ sudo port install ros-hydro-roslaunch

	Note: that ros-hydro-desktop doesnt build currently, due to issues with visualization packages (e.g. rqt-image-view). However, you can install any individual packages that you want and they will build dependencies as needed (so you don't have to manually install every package one by one). This will hopefully be fixed very shortly.

5. If all went well, source the ros environment and start using ROS:

	$ source /opt/local/setup.bash
	
	$ roscore &

