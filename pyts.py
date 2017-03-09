#!/usr/bin/env python
# -*- coding: utf-8 -*-

# sys imports

# numpy imports
import numpy as np

# python imports
from string import Template
import configparser
import subprocess

# Parameters
tbversion = '15.1'


def configuration():
# Loading configuration
    c = configparser.ConfigParser()
    c.read('pyts.cfg')
    print('Configuration : {config}'.format(config=c.sections()))
    return c


def parameters(config):
    # input_model = config['Path']['turbospectrum_dir'] + config['Path']['models_path'] + config['Global']['model_file']
    tpl = open('Babsma.tpl')
    src = Template(tpl.read())
    d = {
            'lambda_min': config['Global']['lambda_min'],
            'lambda_max': config['Global']['lambda_max'],
            'delta_lambda': 0.001,
            'input_model': config['Path']['turbospectrum_dir'] + config['Path']['models_path'] + config['Global']['model_file'],
            'turbulence_velocity': 0
        }
    r = src.substitute(d)
    print(r)
    babslu = config['Path']['turbospectrum_dir'] + config['Path']['exec_dir'] + config['Program']['babsma_exec']
    p = subprocess.Popen([babslu], stdin=subprocess.PIPE, stdout=subprocess.PIPE, cwd=config['Path']['turbospectrum_dir'])
    p.communicate(input=r.encode())[0]


def main():
    print('Starting Turbospectrum version {version}\n'.format(version=tbversion))
    config = configuration()
    parameters(config)


if __name__ == "__main__":
    main()
