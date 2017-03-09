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
# p = subprocess.Popen(["/home/eric/Science/Projets/TurboSpectrum/V15.1/exec-gf-v15.1/babsma_lu"], stdin=PIPE, stdout=PIPE)
# p.communicate(input=b"'LAMBDA_MIN:'  '6500'\n'LAMBDA_MAX:'  '6600'\n'LAMBDA_STEP:' '0.01'")[0]

if __name__ == "__main__":
    main()
