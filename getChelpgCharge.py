##   PYTHON FILE HEADER #
##
##   File:         [getChelpgCharge.py]
##
##   Author(s):    ['Pedro H.F Matias']
##   Credits:      ['Copyright © 2024 LEEDMOL. All rights reserved.']
##   Date:         ['03.04.2024']
##   Version:      ['0.0.1']
##   Status:       ['Development']
##   Language:     ['Python']
##   Description:  ['Python script to get chelpg charges to Lammps']
##   Usage:        ['python3 getChelpgCharge.py <inputfile>']

from sys import argv

if len(argv) < 2:
    print("Usage: python3 getChelpgCharge.py <inputfile>")
    exit()

def getChelpgCharge(inputfile):
    arq = open(inputfile, 'r').readlines()
    arq2 = open(inputfile.split('.')[0] + '_chelpg.dat', 'w')

    for i in range(len(arq)):
        if " ESP charges:" in arq[i]:
            start = i + 2

        if "Sum of ESP charges =" in arq[i]:
            end = i - 1

    for i in arq[start:end]:
        arq2.write(i)
        
    

getChelpgCharge(argv[-1])