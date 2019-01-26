import boto, urllib2
from   boto.ec2 import connect_to_region
from dotenv import Dotenv
from fabric import Connection
from fabric import task
import os
import sys
from stat import *

dotenv = Dotenv(os.path.join(os.path.dirname(__file__), ".env"))
os.environ.update(dotenv)

# --------------------------------------------------------
# Strip whitespaces from array
# --------------------------------------------------------
def _striplist(l):
    return([x.strip() for x in l])

# --------------------------------------------------------
# Private method to print errors
# --------------------------------------------------------
def _printError(val):
	print("\n")
	print('-------------- Error ---------------------------')
	print(val)
	print('------------------------------------------------')
	print("\n")
	sys.exit(os.EX_SOFTWARE)

# --------------------------------------------------------
# Private method for getting AWS connection
# --------------------------------------------------------
def _create_connection(region):

	connection = connect_to_region(
		region_name = os.getenv("aws_ec2_region"), 
		aws_access_key_id=os.getenv("aws_access_key_id"), 
		aws_secret_access_key=os.getenv("aws_secret_access_key")
	)
	return connection

# --------------------------------------------------------
# Private method for getting all instances based on a tag
# --------------------------------------------------------
def _get_public_dns():

	hosts   = []
	connection   = _create_connection(os.getenv("aws_ec2_region"))
	
	try:
		reservations = connection.get_all_instances(filters = {'tag:Name' : os.getenv("ec2_tag")})
		for reservation in reservations:
			for instance in reservation.instances:
				hosts.append(str(instance.public_dns_name))
	except boto.exception.EC2ResponseError as e:
		_printError(e)

	hosts = filter(None, hosts)
	return hosts

# --------------------------------------------------------
# Setting the global variables
# --------------------------------------------------------
if(os.getenv("type") == 'ec2bytag'):
	hosts=_get_public_dns()
else:
	hosts=_striplist(os.getenv("hosts").split(','))

user=os.getenv("user")
pem=os.getenv("pem")
webroot=os.getenv("webroot")


# --------------------------------------------------------
# Check cpu utilization 
# Top 10 memory consuming processes
# --------------------------------------------------------
@task
def cpu(cxt):

	hostConnections = _connect()

	for c in hostConnections:
		_print(c.host)
		with c.cd(webroot):c.run('free -m')
		print("\n")
		print('------------------------------------------------')
		print("\n")
		with c.cd(webroot):c.run('ps aux --sort=-%mem | awk \'NR<=10{print $0}\'')

# --------------------------------------------------------
# Check git status
# --------------------------------------------------------
@task
def git_status(cxt):

	hostConnections = _connect()

	for c in hostConnections:
		_print(c.host)
		with c.cd(webroot):c.run('git status', pty=True)

# --------------------------------------------------------
# Do git pull
# It will promt for passwords if ssh key is not set for git
# --------------------------------------------------------
@task
def git_pull(cxt):
	
	hostConnections = _connect()

	for c in hostConnections:
		_print(c.host)
		with  c.cd(webroot):c.run('git pull origin master', pty=True)

# --------------------------------------------------------
# When git pull is done run artisan commands
# --------------------------------------------------------
@task
def refresh_artisan(cxt):
	
	hostConnections = _connect()

	for c in hostConnections:
		_print(c.host)
		with c.cd(webroot):c.run('php artisan migrate')
		with c.cd(webroot):c.run('php artisan config:clear')
		with c.cd(webroot):c.run('php artisan view:clear')

# --------------------------------------------------------
# Tinker to the first instance
# --------------------------------------------------------
@task
def tinker(cxt):
	
	hostConnections = _connect()
	c = hostConnections[0]

	_print(c.host)
	with c.cd(webroot):c.run('php artisan tinker')

# --------------------------------------------------------
# Run Composer Install
# --------------------------------------------------------
@task
def composer_install(cxt):
	
	hostConnections = _connect()
	c = hostConnections[0]

	_print(c.host)
	with c.cd(webroot):c.run('composer install --optimize-autoloader')

# --------------------------------------------------------
# Run NPM Install
# --------------------------------------------------------
@task
def npm_install(cxt):
	
	hostConnections = _connect()
	c = hostConnections[0]

	_print(c.host)
	with c.cd(webroot):c.run('npm install')

# --------------------------------------------------------
# Private method to connect all host instances
# --------------------------------------------------------
def _connect():

	hostConnections = []

	_validate()

	for host in hosts:
		hostConnections.append(Connection(
		    host=host,
		    user=user,
		    connect_kwargs={
		        "key_filename": pem,
		    },
		))
	return hostConnections

# --------------------------------------------------------
# Private method to validate
# --------------------------------------------------------
def _validate():

	if(len(hosts) == 0):
		print('Error : Please specify atleast one host')
		sys.exit(os.EX_SOFTWARE)

	if(user == ""):
		print('Error : Please specify user')
		sys.exit(os.EX_SOFTWARE)

	if(pem == ""):
		print('Error : Please specify path of pem file')
		sys.exit(os.EX_SOFTWARE)

	if not os.path.isfile(pem):
		print('Error : Pem file does not exist on specified path')
		sys.exit(os.EX_SOFTWARE)

	if(oct(os.stat(pem)[ST_MODE])[-3:] != '400'):
		print('Error : Please give 400 permissions to pem file')
		sys.exit(os.EX_SOFTWARE)

# --------------------------------------------------------
# Private method to print
# --------------------------------------------------------
def _print(host):

	print("\n")
	print('Running on : ' + host)
	print('------------------------------------------------')
	print("\n")


