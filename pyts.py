#!/usr/bin/env python
# -*- coding: utf-8 -*-

# sys imports

# numpy imports
import numpy as np

# python imports
from string import Template
import configparser 

# Parameters
tbversion = '15.1'


def main():
    print('Starting Turbospectrum version {version}\n'.format(version=tbversion))
# Loading configuration
    with open('pyts.ini') as cf:
        config = configparser.ConfigParser()
        config.read(cf)
    print('Configuration : {config}'.format(config=config))

if __name__ == "__main__":
    main()
