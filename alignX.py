##   PYTHON FILE HEADER #
##
##   File:         [alignX.py]
##
##   Author(s):    ['Pedro H.F Matias']
##   Credits:      ['Copyright © 2024 LEEDMOL. All rights reserved.']
##   Date:         ['02.07.2024']
##   Version:      ['0.0.1']
##   Status:       ['Development']
##   Language:     ['Python']
##   Description:  ['This scripts uses PCA to align a molecule in a given input file.']
##   Usage:        ['python3 alignX.py All/<input>'']

##  IMPORTS 

from sys import argv
import numpy as np
from sklearn.decomposition import PCA
from MoleKing import G16LOGfile, Molecule
from os import listdir

if len(argv) != 2:
    print('Plese, provide a input file, or type "All" to align all files in the directory.')

## CODE

class Align():
    def __init__(self):
        if argv[-1].lower() == 'all':
            self.align_all = True
        else:
            self.align_all = False

        self.detect_input(argv[-1])

        if self.align_all:
            files = [i for i in listdir() if i.endswith('.xyz') or i.endswith('.log') or i.endswith('.gjf')]

            for i in files:
                self.arq = i
                self.detect_input(i)
                self.align_molecule()
                self.write_gjf()

        else:
            self.arq = argv[-1]
            self.detect_input(argv[-1])
            self.align_molecule()
            self.write_gjf()

    def detect_input(self, arq):
        if arq.endswith('.xyz'):
            self.molecule = []
            file = open(arq, 'r')
            temp = file.readlines()[2:]
            file.close()
            for i in temp:
                self.molecule.append((i.split()[0], np.array([float(i.split()[1]), float(i.split()[2]), float(i.split()[3])])))
        
        elif arq.endswith('.log'):
            self.molecule = []
            file = G16LOGfile(arq).getMolecule()
            for i in file:
                self.molecule.append((i.getAtomicSymbol(), np.array([float(i.getX()), float(i.getY()), float(i.getZ())])))

        elif arq.endswith('.gjf'):
            self.molecule = []
            file = open(arq, 'r').readlines()
            for i in range(len(file)):
                if '0 1' in file[i]:
                    temp = i+1
                    break

            for i in file[temp:]:
                if i == '\n':
                    break
                else:
                    self.molecule.append((i.split()[0], np.array([float(i.split()[1]), float(i.split()[2]), float(i.split()[3])])))

    def align_molecule(self):
        coords = np.array([coord for atom, coord in self.molecule])

        pca = PCA(n_components=3)
        pca.fit(coords)

        principal_axis = pca.components_[0]
        rotation_matrix = self.get_rotation_matrix(principal_axis)
        
        aligned_coords = np.dot(coords, rotation_matrix.T)  # Transpose the rotation matrix for correct alignment

        self.aligned_atom_data = [(atom, coord) for (atom, _), coord in zip(self.molecule, aligned_coords)]

    def get_rotation_matrix(self, pAxis):
        axis = pAxis / np.linalg.norm(pAxis)
        z_axis = np.array([1, 0, 0])

        if np.allclose(axis, z_axis):
            return np.eye(3)
    
        v = np.cross(axis, z_axis)
        s = np.linalg.norm(v)
        c = np.dot(axis, z_axis)

        vx = np.array([[0, -v[2], v[1]],
                    [v[2], 0, -v[0]],
                    [-v[1], v[0], 0]])
        
        rotation_matrix = np.eye(3) + vx + np.dot(vx, vx) * ((1 - c) / (s ** 2))

        return rotation_matrix

    def write_gjf(self):
        name = self.arq.split('.')[0]
        # arq = open('{}_aligned.gjf'.format(name), 'w')
        # arq.write("#P HF/6-31G(d)\n\n")
        # arq.write("{} Aligned molecule\n\n".format(name))
        # arq.write("0 1\n")

        molecule = Molecule()
        
        for atom, coord in self.aligned_atom_data:
            if name == 'PBT_6':
                print(atom, coord[0], coord[1], coord[2])
            molecule.addAtom(atom.upper(), float(coord[0]), float(coord[1]), float(coord[2]))
            #arq.write(f"{atom} {coord[0]:.6f} {coord[1]:.6f} {coord[2]:.6f}\n")

        molecule.moveMassCenter(0,0,0)

        molecule.toGJF(fileName = name+'_aligned.gjf')
        
        # arq.write("\n\n")
        # arq.close()

if __name__ == '__main__':
    Align()