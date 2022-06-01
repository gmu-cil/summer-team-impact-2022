Development Environment
==========

This folder has a Vagrantfile and Ansible scripts that automatically install PHP, PostgreSQL, Git, Apache, and other needed packages on Ubuntu Trusty for developing a Human Face of Big Data platform. If you see any problems, contact Myeong Lee. 

# Requirements
	- Virtualbox 6.1
	- Vagrant 2.2.19
	- Python

# Quickstart

1. Launch and configure the virtual machine by running the following command.

For Windows user,

```
cd vm/windows 	# Go to the folder where Vagrantfile and other configuration files are located.
vagrant up		# Run the Vagrantfile.
```

For Mac user,

```
cd vm/mac 	# Go to the folder where Vagrantfile and other configuration files are located.
vagrant up		# Run the Vagrantfile.
```

2. Open browser and go to location `http://192.168.56.12`

If the URL does not work check `vm/basic/Vagrantfile` and check file Vagrant configuration.


## Updates (3/7/2018)

Vagrant boxes are not working with old versions, so a new Vagrant version is embedded in the repository. 
When you run Vagrant commands, in a designated folder, try to type like this:

```
../vagrant/exec/vagrant up
```

In this way, you can use the recent version of vagrant to download and configure the Linux machine. 

