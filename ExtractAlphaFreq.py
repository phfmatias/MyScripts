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
##   Description:  ['This script extracts the polarizability (alpha) for each frequency from the output file of a Gaussian calculation.']
##   Usage:        ['python3 ExtractAlphaFreq.py <outputname>']

from MoleKing import G16LOGfile
from os import listdir
from sys import argv
from pandas import DataFrame

files = [x for x in listdir() if x.endswith('.log')]

df = DataFrame()
results = {}

unit = 'esu'

for file in files:

    x = G16LOGfile(file, polarAsw=1)
    freqs = x.getFrequency()

    results_freq = []
    

    for i in freqs:
        results_freq.append(x.getAlpha(unit=unit, frequency=i)['iso'])
            
    results.update({'molecule': file, 'f_'+str(freqs[0])+' ({})'.format(unit): results_freq[0], 'f_'+str(freqs[1])+' ({})'.format(unit): results_freq[1], 'f_'+str(freqs[2])+' ({})'.format(unit): results_freq[2], 'f_'+str(freqs[3])+' ({})'.format(unit): results_freq[3]})
    results_freq.clear()
    df = df._append(results, ignore_index=True)

df = df.to_csv('AlphaFreq_{}.csv'.format(argv[-1]), index=False)


    
    
