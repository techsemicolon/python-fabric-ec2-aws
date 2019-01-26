# Python Fabric EC2 AWS

Run commands on multiple EC2 servers from your local machine. This is a basic scaffolding containing Fabric tasks runnner to execute commands from local machine(or bashin host) to all remote EC2 Servers specified. 

It is a safe tunnel to send your commands from one machine to multiple EC2 servers. It eliminates : 

- Manual Login and running the command to each server.
- If you have autoscaling enabled, then you will need to first find the dns or IPs of the active servers, this does that for you automaticaly based on EC2 tags.
- If you have run a command which needs password, it will simply  prompt you on your local just as it would on the remote server.
- The `fabfile.py` is very simple to extend and add your own tasks in it as a function running the commands you would like. This scaffolding will help you to understand the possibilities.

## Pre-requisites : 

You need to have python 2.X.X installed. Also you will need `fabric`, `dotenv` and `boto` packages.

You can install those packages using : 

~~~bash
pip install fabric
pip install dotenv
pip install boto
~~~

## Installtion : 

~~~bash
git clone https://github.com/techsemicolon/python-fabric-ec2-aws.git fabric
cd fabric
touch .env
~~~

## Settings : 

You need to create an `.env` file in the cloned `fabric` folder with following variables :

~~~bash

# Type can be ec2bytag or manual
type="ec2bytag"

# hosts is only applicable when ypu set type as manual
hosts="host_1_ip,host_2_dns,host_3_domain"
user="common_user_for_all_servers"
pem="absolute_path_to_private_key_file.pem"
webroot="/var/www/your_web_root"

# Below only applicable if you set type as ec2bytag

aws_ec2_region="your_aws_region"
aws_access_key_id="your_access_key_id"
aws_secret_access_key="your_secret_access_key"
ec2_tag="your_ec2_tag_key:your_ec2_tag_value"
~~~

You can either specify the hosts manually or let the script search for instances automatically for you using a specific ec2 tag.

If you set type as `manual`, you need to specify hosts in `hosts` env variable.

Alternatively, if you set type as `ec2bytag` then you need to specify `aws_ec2_region`,
`aws_access_key_id`,  `aws_secret_access_key` and an `ec2_tag` in your env file.


- hosts is a comma separated collection of al ec2 servers(hosts). You can add dns name, ip address, domain name etc based on your settings. noly applicable when type is set to `manual`

- user is the username common to all users. This is specifically imagined as an EC2 servers from autoscaling group which are clones of a main AMI.

- pem is the path of your private key file for all EC2 servers.

- webroot is where you want to run all commands from

- `ec2_tag` is a key value pair of an ec2 tag separated by colon(:). For example : `Name:LiveServer` where `Name` is the key and `LiveServer` is the value.

## Usage :

You can ho use the  fabric tasks :

1. List all available tasks : 

~~~bash
fab --list
~~~

It will give you all tasks like : 

~~~bash
Available tasks:

  composer-install
  git-pull
  git-status
  npm-install
  refresh-artisan
  tinker
  cpu
~~~

2. Now you can run task on all servers : 

~~~bash
fab git-status
~~~

3. Run miltiple tasks together : 

~~~bash
fab git-pull refresh-artisan
~~~


## Task Details : 

1. composer-install : Installs new composer dependencies
1. npm-install : Installs new npm dependencies
1. git-pull : Pulls from master branch
1. git-status : Check current git status
1. refresh-artisan : Runs artisan:migrate, artisan config:clear and artisan view:clear
1. tinker : Runs tinker on one of the server hosts specified
1. cpu : Check current free memory and top 10 memory consuming processes

## Extending : 

Feel free to add new commands to `fabfile.py` as per your preference.