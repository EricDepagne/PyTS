#!/usr/bin/env python
# -*- coding: utf-8 -*-

# sys imports

# numpy imports
import numpy as np

# python imports
import os
from sys import exit
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


def check_directories():
    if not os.path.realpath(os.getcwd()) == os.path.realpath(config['Path']['base_dir']):
        print('Running TurboSpectrum from elsewhere')
        if config['Global'].getboolean('create_dirs_and_links') is False:
            print('The program will not change the structure of your directories, and the program will not run properly.')
            print('If you want the proper structure, you need to change the parameter "create_dirs_and_links" in the configuration file {configfile} from "False" to "True"'.format(configfile='pyts.cfg'))
            print('The program will now exit')
            exit()
        else:
            print('Linking some directories so')
            sources_to_link = ['DATA', ]
            for s in sources_to_link:
                print(config['Path']['base_dir']+s, os.getcwd() + '/')
                try:
                    os.symlink(config['Path']['base_dir']+s, os.getcwd()+'/'+s)
                except FileExistsError:
                    print('Link already made. Continuing')
    else:
        print('same location')
    # If we don't run turbospectrum in the base directory, some files can't be read.
    # We'll make sure thos files are there.
    print('Script directory : {directory}'.format(directory=os.path.dirname(os.path.realpath(__file__))))
    print('Base directory : {directory}'.format(directory=os.path.realpath(config['Path']['base_dir'])))
    print('Running directory : {directory}'.format(directory=os.path.realpath(os.getcwd())))


def configuration(prg, abu=0):
    # Checking for the existence of directories to save files.

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
            section = 'Eqwidth'
            if abu == 1:
                section = 'Abundances'
        else:
            section = 'SyntheticSpectrum'

        print('section : {section}'.format(section=section))
        extended_parameters = {
            'intensity_or_flux': config['Global']['intensity_or_flux'],
            'abfind': config['Global']['abfind'],
            'out_file':os.path.realpath(os.getcwd())+'/'+config['Results']['out_file']+config[section]['extension'],
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
            'opacity_file': os.path.realpath(os.getcwd())+'/'+config['Results']['opacity_file'],
        }
    print('abu : {abu}'.format(abu=abu))
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
<<<<<<< HEAD
=======
    turbospectrum['babsma'] = {
            'input': babsma_input,
            'output': bab_output,
            'error': bab_errors}
>>>>>>> master
    prg = ['bsyn', 'eqwidth']
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
    check_directories()
    main()
