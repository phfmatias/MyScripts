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
##   Usage:        ['python3 gjf2xyz.py <inputfile.gjf>']

from sys import argv

if len(argv) != 2:
    print("Usage: python3 gjf2xyz.py <inputfile.gjf>")
    exit()

inputfile = argv[1]
arq = open(inputfile, 'r').readlines()

out = open(inputfile.split('.')[0]+'.xyz', 'w')

charges_multi = ['0 1', '0 2', '0 3', '-1 1', '-1 2', '-1 3', '1 1', '1 2', '1 3']

for i in range(len(arq)):
    if len(arq[i].split()) == 2:
        if '{} {}'.format(arq[i].split()[0], arq[i].split()[1]) in charges_multi:
            start = i+1
            break


for i in range(start, len(arq)):
    if arq[i] == '\n':
        end = i
        break

atoms = len(arq[start:end])

out.write(str(atoms)+'\n{}\n'.format(inputfile.split('.')[0]))

for i in range(start, end):
    out.write(arq[i])

out.close()
print('Conversion completed!')

    
    