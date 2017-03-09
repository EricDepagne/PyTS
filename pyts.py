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
    config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
    config.read('pyts.cfg')
    print('Configuration : {config}'.format(config=config.sections()))
    tpl = open('Babsma.tpl')
    src = Template(tpl.read())
    d = {
            'delta_lambda': 0.001,
            'turbulence_velocity': 0,
            'lambda_min': config['Global']['lambda_min'],
            'lambda_max': config['Global']['lambda_max'],
            'metallicity': config['Global']['metallicity'],
            'xifix': config['Global']['xifix'],
            'marcsfile': config['Global']['marcsfile'],
            'input_model': config['Path']['model_dir'] + config['Global']['model_file'],
            'opacity_file': config['Models']['opacity_file'],
            'alpha_over_iron': config['Models']['alpha_over_iron'],
            'helium_fraction': config['Models']['helium_fraction'],
            'r_process_fraction': config['Models']['r_process_fraction'],
            's_process_fraction': config['Models']['s_process_fraction']
        }
    r = src.substitute(d)
    print(r)
    return config, r


def main():
    print('Starting Turbospectrum version {version}\n'.format(version=tbversion))
    (config, r) = configuration()
    p = subprocess.Popen([config['Program']['babsma_exec']], stdin=subprocess.PIPE, stdout=subprocess.PIPE, cwd=config['Path']['base_dir'], universal_newlines=True)
    outs, errs = p.communicate(input=r)
    print(outs)


if __name__ == "__main__":
    main()
