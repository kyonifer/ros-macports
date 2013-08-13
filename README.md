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

3. At this point, you should be good to install the ros-core port:

	$ sudo port install ros-groovy

4. If all went well, source the ros environment and start using ROS:

	$ source /opt/local/setup.bash
	
	$ roscore &

