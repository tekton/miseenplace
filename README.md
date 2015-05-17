Registration for chef and github
================================

Purpose
--------------------------------

To allow people to enter a github OAuth and get back a shell script to get them setup for a given company.


Setup
---------------

* Download from github
* Create a virtual environment
* Activate virtual environment
* Install requirements via: pip install -r requirements.txt
* run: python manage.py runserver 0:8000

Requirements
--------------

Python 2.7+
MongoDB 2.6+
redis 2.6+


Notes and General Ideas
=======================

When using things like chef to start things up there's still an inital "setup" that needs to happen- a default client.rb, cookbooks getting installed, chef getting installed, etc. In order to make that easier this stores a bash template that gets filled out by the system to get you started.

The "admin" section allows for the creation/editing of said templates.


Example
-------

#!/bin/bash
sudo mkdir -p /opt/[[company]]
sudo chmod [[opt_level]] /opt/[[company]]
cd /opt/[[company]]
git checkout http://[[oauth]]@github.com/[[company]]/[[cookbooks]].git
echo "cookbook_path [\"/opt/[[company]]/[[cookbooks]]\"]" >> /opt/[[company]]/[[client_rb]]
[[chef_install]]
echo "Run your setup by running: chef-solo -j /opt/[[company]]/[[cookbooks]]/[[dev_setup_json]] -c /opt/[[company]]/[[client_rb]]"