from setuptools import setup

setup(
    name='rpi-security',
    version='0.6',
    author=u'Sergy F',
    author_email='sergfa@gmail.com',
    url='https://github.com/sergfa/raspberry-monitor',
    license='GPLv2',
    description='A Raspberry Pi presense monitoring system written in python to run on a Raspberry Pi with email notifications',
    long_description=open('README.md').read(),
    scripts = [ 'presense/presense-monitor.py' ],
    data_files=[
    ],
    install_requires=[
        'netaddr',
        'netifaces',
        'python-telegram-bot'
    ],
    classifiers=[
    'Environment :: Console',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.4'
    ],