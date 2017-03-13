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
config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
config.read('pyts.cfg')
tbversion = config['Global']['version']


def configuration():
    # Loading configuration
    babsma_tpl = open('Babsma.tpl')
    babsma_src = Template(babsma_tpl.read())
    bsyn_tpl = open('Bsyn.tpl')
    bsyn_src = Template(bsyn_tpl.read())
    d = {
            'turbulence_velocity': 0,
            'chifix': config['Global']['chifix'],
            'marcsfile': config['Global']['marcsfile'],
            'input_model': config['Path']['model_dir'] + config['Global']['model_file'],
            'lambda_min': config['Global']['lambda_min'],
            'lambda_max': config['Global']['lambda_max'],
            'delta_lambda': config['Global']['delta_lambda'],
            'intensity_or_flux': config['Global']['intensity_or_flux'],
            'abfind': config['Global']['abfind'],
            'opacity_file': config['Results']['opacity_file'],
            'synthetic_spectrum': config['Results']['synthetic_spectrum'],
            'metallicity': config['Global']['metallicity'],
            'alpha_over_iron': config['Models']['alpha_over_iron'],
            'helium_fraction': config['Models']['helium_fraction'],
            'r_process_fraction': config['Models']['r_process_fraction'],
            's_process_fraction': config['Models']['s_process_fraction'],
            'spherical': config['Global']['spherical'],
            'number_of_elements': len(config['Models']['individual_abundances'].split(",")),
            'list_of_elements': '\n'.join(config['Models']['individual_abundances'].split(",")),
            'number_of_files': len(config['Files']['linedata_files'].split(",")),
            'list_of_lines_files': '\n'.join(config['Files']['linedata_files'].split(","))

        }
    babsma = babsma_src.substitute(d)
    bsyn = bsyn_src.substitute(d)
    print(babsma, bsyn)

    return config, babsma, bsyn


def main():
    print('Starting Turbospectrum version {version}\n'.format(version=tbversion))
    (config, babsma, bsyn) = configuration()
    p = subprocess.Popen(
            [config['Program']['babsma_exec']],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            cwd=config['Path']['base_dir'],
            universal_newlines=True)
    bab_output, bab_errors = p.communicate(input=babsma)
    if bab_errors is None:
        print('Success. Continuous opacity file \n{file}\n generated.\n'.format(file=config['Results']['opacity_file']))
    p = subprocess.Popen(
            [config['Program']['bsyn_exec']],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            cwd=config['Path']['base_dir'],
            universal_newlines=True)
    bsyn_output, bsyn_errors = p.communicate(input=bsyn)

if __name__ == "__main__":
    main()
