##   PYTHON FILE HEADER #
##
##   File:         [getCPS.py]
##
##   Author(s):    ['Pedro H.F Matias']
##   Site(s):      ['https://github.com/phfmatias']
##   Email(s):     ['phfmatias@discente.ufg.br']
##   Credits:      ['Copyright © 2025 LEEDMOL. All rights reserved.']
##   Date:         ['31.03.2025']
##   Version:      ['0.0.1']
##   Status:       ['Development']
##   Language:     ['Python']
##   Description:  ['This script extracts the charge of the CPs from the CPprop.txt file for VMD plot.']
##   Usage:		   ['python getCPS.py']


# This should be the same label as in GaussView
# atoms_to_get = ['O_167 H_44', 'H_30 O_184', 'H_3 O_185', 'H_14 O_107', 'O_152 H_63', 'O_140 H_52', 'O_139 H_79', 'H_93 O_122']
atoms_to_get = ['N_11 N_1','N_1 H_10', 'H_10 O_13']


cp_dict = {}
cp_list = []
cp_positions = []
cp_paths = []

def getCPS(atoms_to_get, file):
    arq = open(file,'r').readlines()

    for i in range(len(arq)):
        for j in atoms_to_get:
            atom1 = j.split()[0].split('_')[1]+'('+j.split()[0].split('_')[0]+' )'
            atom2 = j.split()[1].split('_')[1]+'('+j.split()[1].split('_')[0]+' )'
            
            if ' '+atom1 in arq[i] and ' '+atom2 in arq[i] and 'Type (3,-1)' in arq[i-1]:
                
                cp = int(arq[i-1].split()[2].split(',')[0])
                cp_dict.update({j: cp})
                cp_list.append(cp)
                cp_positions.append([arq[i+2].split()[2], arq[i+2].split()[3], arq[i+2].split()[4]])

                if cp == 18:
                    print(arq[i])
                    print(atom1, atom2)

                print('Found CP: ', cp, ' of Atoms ', atom1, ' and ', atom2)

getCPS(atoms_to_get, 'CPprop.txt')

def getPaths(positions):
    arq = open('paths.pdb','r').readlines()
    for i in range(len(arq)):
        for j in range(len(positions)):
            x = round(float(positions[j][0]), 3)
            y = round(float(positions[j][1]), 3)
            z = round(float(positions[j][2]), 3)

            if str(x) in arq[i] and str(y) in arq[i] and str(z) in arq[i]:
                if len(arq[i].split()) == 12:
                    cp_paths.append(arq[i].split()[5])
                elif len(arq[i].split()) == 11:
                    cp_paths.append(arq[i].split()[4])
getPaths(cp_positions)

toPrint = 'name N and serial '
toPrintPath = 'resid '

for i in cp_list:
    toPrint += str(i) + ' '

print(toPrint)

for i in cp_paths:
    toPrintPath += str(i) + ' '

print(toPrintPath)