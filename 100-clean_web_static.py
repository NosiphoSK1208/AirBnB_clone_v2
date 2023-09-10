#!/usr/bin/python3
"""Fabric script to clean up old versions of web_static"""

from fabric.api import *
import os

env.hosts = ['100.25.215.46', '52.3.246.184']  # Replace with your server IPs
env.user = 'ubuntu'  # Replace with your username
env.key_filename = '~/.ssh/school'  # Replace with your SSH key path

def do_clean(number=0):
    """
    Deletes out-of-date archives and old versions of web_static
    """
    try:
        number = int(number)
    except ValueError:
        return

    if number < 2:
        number = 1

    with cd('/data/web_static/releases'):
        archives = sorted(run('ls -1t').split())
        for archive in archives[number:]:
            run('rm -rf {}'.format(archive))

    with cd('/data/web_static/releases'):
        archives = sorted(run('ls -1t').split())
        for archive in archives[number:]:
            run('rm -rf {}'.format(archive))

    with cd('/data/web_static/releases'):
        archives = sorted(run('ls -1t').split())
        for archive in archives[number:]:
            run('rm -rf {}'.format(archive))

    with cd('/data/web_static/releases'):
        archives = sorted(run('ls -1t').split())
        for archive in archives[number:]:
            run('rm -rf {}'.format(archive))

    with lcd('versions'):
        local('ls -1t | tail -n +{} | xargs rm -rf'.format(number + 1))
