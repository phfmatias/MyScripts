##   PYTHON FILE HEADER #
##
##   File:         [gjf2xyz.py]
##
##   Author(s):    ['Pedro H.F Matias']
##   Credits:      ['Copyright © 2024 LEEDMOL. All rights reserved.']
##   Date:         ['16.04.2024']
##   Version:      ['0.0.1']
##   Status:       ['Development']
##   Language:     ['Python']
##   Description:  ['Python script to convert Gaussian input files to XYZ files.']
##   Usage:        ['python3 xyz2gjf']


from os import listdir

xyz =  [i for i in listdir() if i.endswith('.xyz')]

for i in xyz:
    arq = open(i, 'r').readlines()
    arq = [i.replace(',', ' ') for i in arq]
    out = open(i.split('.')[0]+'.gjf', 'w')
    out.write('%nprocshared=4\n')
    out.write('%mem=4GB\n')
    out.write('#p CAM-B3LYP/6-311G(d) opt\n\n')
    out.write('Title Card Required\n\n')
    out.write('0 1\n')
    for j in range(2, len(arq)):
        out.write(arq[j])
    out.write('\n\n')    
    out.close()
    print('Conversion completed!')