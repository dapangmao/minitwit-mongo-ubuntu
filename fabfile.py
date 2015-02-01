# -*- coding: utf-8 -*-

from fabric.api import cd, env, puts, sudo
from fabric.contrib.files import exists

env.hosts = ['YOUR IP ADDRESS']
env.user = 'root'
env.password = 'YOUR PASSWORD'

project_name = "minitwit-mongo-ubuntu"
python_requirements = ['flask', 'pymongo', 'Flask-PyMongo', 'pytz']
supervisor_conf = """
[program: %s]
command = gunicorn minitwit:app -b 127.0.0.1:5000
directory = /home/flask/%s
""" % (project_name, project_name)

nginx_conf = """
server {
    location /static {
        alias /home/flask/%s/static;
    }

    location / {
        proxy_pass http://127.0.0.1:5000;
    }
}
""" % (project_name)

def install_basics():
    sudo('apt-get update')
    sudo('apt-get install -y python-pip')
    sudo('apt-get install -y git')
    sudo('apt-get install -y nginx')
    sudo('apt-get install -y gunicorn')
    sudo('apt-get install -y supervisor')
    sudo('pip install {}'.format(' '.join(python_requirements)))

def install_mongo():
    sudo('apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10')
    sudo("echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' \
        | tee /etc/apt/sources.list.d/mongodb.list")
    sudo('apt-get update')
    sudo('apt-get install -y mongodb-org')

def copy_file():
    if not exists('/home/flask'):
        sudo('mkdir /home/flask')
    with cd('/home/flask'):
        sudo('git clone https://github.com/dapangmao/minitwit-mongo-ubuntu.git')
    with cd('/home/flask/{}'.format(project_name)):
        sudo('python minitwit_tests.py')

def adjust_nginx():
    sudo('/etc/init.d/nginx start')
    default_file = '/etc/nginx/sites-enabled/default'
    if exists(default_file):
        sudo('rm ' + default_file)
    with cd('/etc/nginx/sites-available'):
        sudo("echo '{}' ".format(nginx_conf) + '> {}'.format(project_name))
    sudo('ln -s /etc/nginx/sites-available/minitwit-mongo-ubuntu' + \
        ' /etc/nginx/sites-enabled/minitwit-mongo-ubuntu')
    sudo('/etc/init.d/nginx restart')

def adjust_supervisor():
    if not exists('/etc/supervisor/conf.d/{}.conf'.format(project_name)):
        sudo("echo '{}' ".format(supervisor_conf) + \
            '> /etc/supervisor/conf.d/{}.conf'.format(project_name))
    sudo('supervisorctl reread')
    sudo('supervisorctl update')

def run_flask():
    sudo('supervisorctl start {}'.format(project_name))
    sudo('supervisorctl status')
    puts('Now go to http://{} to view the app'.format(env.hosts[0]))

def deploy_minitwit():
    install_basics()
    install_mongo()
    copy_file()
    adjust_nginx()
    adjust_supervisor()
    run_flask()
