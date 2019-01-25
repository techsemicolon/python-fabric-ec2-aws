# Laravel Python Fabric

Run commands on multiple EC2 servers. This is a basic scaffolding for you. It is a Fabric tasks runnner to execute commands from local machine(or bashin host) to all remote EC2 Servers specified. 

## Pre-requisites : 

You need to have python 2.X.X install. Also you will need `fabric` and `dotenv` packages.

You can install it using : 

~~~bash
pip install fabric dotenv
~~~

## Settings : 

Yu need to create an `.env` file in the same folder where you have saved the `fabfile.py`, with following variables :

~~~env
hosts="host_1_ip,host_2_dns,host_3_domain"
user="common_user_for_all_servers"
pem="absolute_path_to_private_key_file.pem"
webroot="/var/www/your_web_root"
~~~

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

## Extending : 

Feel free to add new commands to `fabfile.py` as it is very straight forward. 