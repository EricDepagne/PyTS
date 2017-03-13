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
turbospectrum = {
        'version':  config['Global']['version'],

                }


def configuration(prg, abu=None):
    print(prg)
    # Loading configuration
    if 'babsma' in prg:
        tpl_file = 'Babsma.tpl'
        extended_parameters = {
            'input_model': config['Path']['model_dir'] + config['Global']['model_file'],
            'chifix': config['Global']['chifix'],
            'turbulence_velocity': 0,
            'marcsfile': config['Global']['marcsfile']
                }
    else:
        tpl_file = 'Bsyn_or_Eqwidth.tpl'
        if abu is not None:
            if 'eqw' in prg:
                section = 'Abundances'
            section = 'Eqwidth'
        else:
            section = 'SyntheticSpectrum'
        print('Section : {section}'.format(section=section))

        extended_parameters = {
            'intensity_or_flux': config['Global']['intensity_or_flux'],
            'abfind': config['Global']['abfind'],
            'out_file': config['Results']['out_file']+config[section]['extension'],
            'number_of_files': len(config[section]['files'].split(",")),
            'list_of_lines_files': '\n'.join(config[section]['files'].split(",")),
            'number_of_elements': len(config['Models']['individual_abundances'].split(",")),
            'list_of_elements': '\n'.join(config['Models']['individual_abundances'].split(",")),
            'spherical': config['Global']['spherical']
                }
    common_parameters = {
            'lambda_min': config['Global']['lambda_min'],
            'lambda_max': config['Global']['lambda_max'],
            'delta_lambda': config['Global']['delta_lambda'],
            'opacity_file': config['Results']['opacity_file'],
            'metallicity': config['Global']['metallicity'],
            'alpha_over_iron': config['Models']['alpha_over_iron'],
            'helium_fraction': config['Models']['helium_fraction'],
            'r_process_fraction': config['Models']['r_process_fraction'],
            's_process_fraction': config['Models']['s_process_fraction'],
        }
    template = open(tpl_file)
    source = Template(template.read())
    # bsyn_tpl = open('TurboSpectrum.tpl')
    # bsyn_src = Template(bsyn_tpl.read())
    d = {**common_parameters, **extended_parameters}
    print(list(d))

    stdin = source.substitute(d)
    # bsyn = bsyn_src.substitute(d)
    print(stdin)

    return config, stdin


def main():
    print('Starting Turbospectrum version {version}\n'.format(version=turbospectrum['version']))
    (config, prg_input) = configuration('babsma')
    (a, b) = configuration('bsyn', abu=True)
    prg = ['babsma', 'eqwidth', 'bsyn']
    p = subprocess.Popen(
            [config['Program'][prg[0]]],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            cwd=config['Path']['base_dir'],
            universal_newlines=True)
    bab_output, bab_errors = p.communicate(input=prg_input)
    if bab_errors is None:
        print('Success. Continuous opacity file \n{file}\n generated.\n'.format(file=config['Results']['opacity_file']))
    p = subprocess.Popen(
            [config['Program']['bsyn_exec']],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            cwd=config['Path']['base_dir'],
            universal_newlines=True)
    # bsyn_output, bsyn_errors = p.communicate(input=bsyn)

if __name__ == "__main__":
    main()
