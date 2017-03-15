#!/usr/bin/env python
# -*- coding: utf-8 -*-

# sys imports

# numpy imports
import numpy as np

# python imports
from string import Template
import configparser
import subprocess
from itertools import product

# Parameters
config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
config.read('pyts.cfg')
turbospectrum = {
        'version':  config['Global']['version'],
                }


def configuration(prg, abu=None):
    print('Executing program {prg}'.format(prg=prg))
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
        if 'eqw'in prg:
            if abu is not None:
                section = 'Abundances'
            section = 'Eqwidth'
        else:
            section = 'SyntheticSpectrum'

        print('section : {section}'.format(section=section))
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
            'metallicity': config['Global']['metallicity'],
            'alpha_over_iron': config['Models']['alpha_over_iron'],
            'helium_fraction': config['Models']['helium_fraction'],
            'r_process_fraction': config['Models']['r_process_fraction'],
            's_process_fraction': config['Models']['s_process_fraction'],
            'opacity_file': config['Results']['opacity_file'],
        }
    template = open(tpl_file)
    source = Template(template.read())
    d = {**common_parameters, **extended_parameters}

    stdin = source.substitute(d)
    print('Input : {stdin}'.format(stdin=stdin))

    return stdin


def main():
    print('Starting Turbospectrum version {version}\n'.format(version=turbospectrum['version']))
    # Babsma is run everytime.
    babsma_input = configuration('babsma')
    p = subprocess.Popen(
            [config['Program']['babsma']],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            cwd=config['Path']['base_dir'],
            universal_newlines=True)
    bab_output, bab_errors = p.communicate(input=babsma_input)
    prg = ['bsyn','eqwidth']
    with_abu = [0, 1]
    results = {}
    for combination in product(prg, with_abu):
        if combination[1] == 1 and combination[0] is 'bsyn':
            continue
        print('À exécuter : {prg} avec {abu}'.format(prg=combination[0], abu=combination[1]))
        prg_input = configuration(combination[0], combination[1])
        process = subprocess.Popen(
            [config['Program'][combination[0]]],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            cwd=config['Path']['base_dir'],
            universal_newlines=True
                                    )
        o, e = process.communicate(input=prg_input)
        results.update({'error': e, 'output': o})
        try:
            turbospectrum[combination[0]].update({combination[1]: results})
        except KeyError:
            turbospectrum.update({combination[0]: {combination[1]: results}})

if __name__ == "__main__":
    main()
