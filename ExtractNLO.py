##   PYTHON FILE HEADER #
##
##   File:         [ExtractAlphaFreq.py]
##
##   Author(s):    ['Pedro H.F Matias']
##   Credits:      ['Copyright © 2024 LEEDMOL. All rights reserved.']
##   Date:         ['22.03.2024']
##   Version:      ['0.0.1']
##   Status:       ['Development']
##   Language:     ['Python']
##   Description:  ['This script extracts the NLO (alpha, beta and gamma) for each frequency from the output file of a Gaussian calculation.']
##   Usage:        ['python3 ExtractAlphaFreq.py <outputname>']

from MoleKing import G16LOGfile
from os import listdir
from sys import argv
from pandas import DataFrame
files = [x for x in listdir() if x.endswith('.log')]

df_alpha = DataFrame()
alpha_R = {}

df_beta = DataFrame()
beta_R = {}

df_gamma = DataFrame()
gamma_R = {}

unit = 'esu'

for file in files:
    name = file.split('_')[0]

    x = G16LOGfile(file, polarAsw=1)
    freqs = x.getFrequency()

    alpha = []
    beta = []
    gamma = []

    for i in freqs:
        alpha.append(x.getAlpha(unit=unit, frequency=i))
        beta.append(x.getBeta(unit=unit, frequency=i))
        gamma.append(x.getGamma(unit=unit, frequency=i))
    
    #create two columns, alpha[0] and alpha[1], the row will be the values of the alpha

    for j in range(len(freqs)):
        for i in range(len(alpha[j].keys())):
            alpha_R.update({list(alpha[j].keys())[i]: list(alpha[j].values())[i]})
    
        df_alpha = df_alpha._append(alpha_R, ignore_index=True)

        for i in range(len(beta[j].keys())):
            beta_R.update({list(beta[j].keys())[i]: list(beta[j].values())[i]})
        
        df_beta = df_beta._append(beta_R, ignore_index=True)

        for i in range(len(gamma[j].keys())):
            gamma_R.update({list(gamma[j].keys())[i]: list(gamma[j].values())[i]})
        
        df_gamma = df_gamma._append(gamma_R, ignore_index=True)


df_alpha = df_alpha.T
df_beta = df_beta.T
df_gamma = df_gamma.T

df_alpha.rename(columns={i: f'freq_{freqs[i]}' for i in range(len(freqs))}, inplace=True)
df_beta.rename(columns={i: f'freq_{freqs[i]}' for i in range(len(freqs))}, inplace=True)
df_gamma.rename(columns={i: f'freq_{freqs[i]}' for i in range(len(freqs))}, inplace=True)

df_alpha.fillna(0, inplace=True)
df_beta.fillna(0, inplace=True)
df_gamma.fillna(0, inplace=True)


df_alpha.index.name = 'Axis'
df_beta.index.name = 'Axis'
df_gamma.index.name = 'Axis'

df_alpha.to_csv('alpha_{}.csv'.format(name))
df_beta.to_csv('beta_{}.csv'.format(name))
df_gamma.to_csv('gamma_{}.csv'.format(name))