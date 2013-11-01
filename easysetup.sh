#!/bin/bash

# Must be sudo
su=`whoami`
if [ $su != "root" ]; then
	echo "Must be run with sudo!"
	exit
fi

#install software
apt-get install mongodb
apt-get install redis-server

# install python library
easy_install kpages

