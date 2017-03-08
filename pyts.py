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
    c = configparser.ConfigParser()
    c.read('pyts.ini')
    print('Configuration : {config}'.format(config=c.sections()))

if __name__ == "__main__":
    main()
