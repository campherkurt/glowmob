from fabric.api import *
#from fabric.contrib.console import confirm
import os.path

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

env.local_deploy = '/home/rohan/deploy/thescoop'
#env.working_copy = '/home/rohan/src/py/mtn-ism'
env.working_copy = PROJECT_ROOT
env.project = 'yoza'


def gateway():
    "Set the variables for the local qa on gateway server"
    env.hosts = ['gateway']
    env.remote_dir = "/home/user/src"
    env.environ = 'pinax'
    env.virtualenv = '/home/user/pyenv/pinax-mtn/bin/activate'


def qa():
    "Set the variables for the qa server"
    env.hosts = ['byteorbit.co.za']
    env.user = 'byte'
    env.password = 'SpltBXGyH50'
    env.remote_dir = "/home/byte/src"
    env.environ = 'qa'
    env.virtualenv = '/home/byte/pyenv/pinax-dev/bin/activate'



def _set_permissions():
    sudo("chmod -R 777 %(remote_dir)s/%(project)s/site_media/media/" % env)
    #sudo("chmod -R 777 %(remote_dir)s/%(project)s/djapian_spaces/" % env)


def deploy():
    require("host")
    require("remote_dir")
    require('environ')
    print local("cd %(working_copy)s && find -name '*.pyc' -exec rm {} \;" % env) # remove cache files
    print local("cd %(working_copy)s && rsync -czrPC --stats --delete --exclude-from=ignore.rsync ./ %(user)s@%(host)s:%(remote_dir)s/%(project)s/" % env)
    #_set_permissions()
    # link correct settings file
    #run("cd %(remote_dir)s/%(project)s/ && rm settings.py && ln -s settings_%(environ)s.py settings.py" % env)
    #run("cd %(remote_dir)s/%(project)s/ && source %(virtualenv)s && ./manage.py migrate --no-initial-data" % env)
    run("touch %(remote_dir)s/%(project)s/deploy/%(environ)s.wsgi" % env)

def migrate():
    run("cd %(remote_dir)s/%(project)s/ && source %(virtualenv)s && ./manage.py migrate" % env)


def deploy_simulation():
    require("host")
    require("remote_dir")
    require('environ')
    print local("cd %(working_copy)s && find -name '*.pyc' -exec rm {} \;" % env) # remove cache files
    print local("cd %(working_copy)s && rsync -nczrPC --stats --delete --exclude-from=ignore.rsync ./ %(user)s@%(host)s:%(remote_dir)s/%(project)s/" % env)


