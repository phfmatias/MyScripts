##   PYTHON FILE HEADER #
##
##   File:         [ExtractAlphaFreq.py]
##
##   Author(s):    ['Pedro H.F Matias', 'Rafael Ferreira Verissimo']
##   Credits:      ['Copyright © 2024 LEEDMOL. All rights reserved.']
##   Date:         ['22.03.2024']
##   Version:      ['1.0']
##   Status:       ['Development']
##   Language:     ['Python']
##   Description:  ['This script is used to change charges in a .data file to the ones calculated by Gaussian.']
##   Usage:        ['python3 pacKing.py <packing.inp>']

from sys import argv
from MoleKing import G16LOGfile

if len(argv) < 2:
    print("Usage: python pacKing.py <packing.inp>")
    arq = open('pacKing_dummy.inp', 'w')
    arq.write('# This is the input file for pacKing.py\n')
    arq.write('# Please, fill the information below IN THE SAME ORDER of the .data file\n')
    arq.write('solvent1: solvent1.log number of molecules\n')
    arq.write('solvent2: solvent2.log number of molecules\n')
    arq.write('solute1: solute1.log number of molecules\n')
    arq.write('solute2: solute2.log number of molecules\n')
    arq.write('data: data.data\n')
    print('An example of the .inp file was created in the current directory.')
    exit(1)

class pacKing:
    def __init__(self):
        self.charges = []
        self.charges_dict = {}
        self.atom_dict = {}
        self.control()
        self.preparing_data()
        self.read_box()
        self.modify=self.change_charges()
        self.calculateDensity()
        self.print_file()
        
    def control(self):
        arq = open(argv[1], 'r').readlines()
        self.solves = []
        self.solutes = []
        self.numbers = []
        self.molarMass = []
        self.atomnumbers = []

        for i in range(len(arq)):
            if 'solvent' in arq[i]:
                self.solves.append(arq[i].split()[2])
                self.numbers.append(int(arq[i].split()[3]))
            if 'solute' in arq[i]:
                self.solutes.append(arq[i].split()[2])
                self.numbers.append(int(arq[i].split()[3]))
            if 'data' in arq[i]:
                self.data = arq[i].split()[2]
            if 'box_size' in arq[i]:
                self.box_size = arq[i].split()[2]

        if len(self.solves) == 0:
            print('No solvent was found in the input file.')
            exit(1) 
        
        if len(self.solutes) == 0:
            print('No solute was found in the input file.')
            

        try:
            self.data
        except:
            print('No data file was found in the input file.')
            exit(1)

        try:
            self.box_size
        except:
            print('No box_size was found in the input file.')
            exit(1)            
        
        for i in range(len(self.solves)):
            print('Solvent {}: Number of Molecules {}'.format(self.solves[i].split('.')[0], self.numbers[i]))
        for i in range(len(self.solutes)):
            print('Solute {}: Number of Molecules {}'.format(self.solutes[i].split('.')[0], self.numbers[i+len(self.solves)]))

    def calculateDensity(self):
        mol_voly = 0

        for i in range(len(self.solves)):
            mol_voly += 1.6605577881 * sum(self.molarMass[i] * self.numbers[i] for i in range(len(self.solves)))
        for i in range(len(self.solutes)):
            mol_voly += 1.6605577881 * sum(self.molarMass[i] * self.numbers[i] for i in range(len(self.solutes)))
        
        print('Box Size: {} Angstrom'.format(self.box_size))
        print('Molecular Volume: {} cm³'.format(mol_voly))
        print('Density: {} g/cm³'.format(mol_voly/(float(self.box_size)**3)))
        
        
                
    def preparing_data(self):
        for i in range(len(self.solves)):
            self.gaussian_log = open(self.solves[i], 'r').readlines()
            self.atomnumbers.append(len(G16LOGfile(self.solves[i]).getMolecule()))
            self.molarMass.append(G16LOGfile(self.solves[i]).getMolecule().getMM())
            self.charges.append(self.get_charges())
            self.charges_dict = {}

        for i in range(len(self.solutes)):
            self.gaussian_log = open(self.solutes[i], 'r').readlines()
            self.atomnumbers.append(len(G16LOGfile(self.solutes[i]).getMolecule()))
            self.molarMass.append(G16LOGfile(self.solutes[i]).getMolecule().getMM())
            self.charges.append(self.get_charges())
            self.charges_dict = {}


    def read_box(self):
        s = ''
        rlines = open(self.data, 'r').readlines()
        for i in range(len(rlines)):
            if ' Atoms #' in rlines[i]:
                start = i + 2
                self.start = start
                
            if ' Bonds' in rlines[i]:
                end = i - 2 
                self.end = end
                break
        self.box = rlines[start:end+1]


    def change_charges(self):
        start = 0
        test = ''
        list_of_molecules = self.solves + self.solutes
        count = 1
        for i in range(len(list_of_molecules)):            
            for j in range(start, start + self.numbers[i] * self.atomnumbers[i]):
                c = list(self.charges[i].keys())[count-1]
                test += self.box[j].replace(self.box[j].split()[3], self.charges[i][c])
                count += 1
                if count > self.atomnumbers[i]:
                    count = 1
           
            start = j + 1
        return test


    def get_charges(self):
        start_list = []
        end_list = []
        for i in range(len(self.gaussian_log)):
            if 'ESP charges:' in self.gaussian_log[i]:
                #take the last account of ESP charges
                start_list.append(i + 2)
            if 'Sum of ESP charges' in self.gaussian_log[i]:
                end_list.append(i)
        for i in range(start_list[-1], end_list[-1]):
            self.charges_dict[self.gaussian_log[i].split()[1]+'_'+self.gaussian_log[i].split()[0]] = self.gaussian_log[i].split()[2]
        print(self.charges_dict)  
        return self.charges_dict
    
    
    def print_file(self):          

        arq = open('new_'+self.data, 'w')
        arqv = open(self.data, 'r').readlines()
        for i in arqv[0:self.start]:
            if 'xlo' in i.split():
                arq.write('{} {} xlo xhi\n'.format(-float(self.box_size)/2, float(self.box_size)/2))
            elif 'ylo' in i.split():
                arq.write('{} {} ylo yhi\n'.format(-float(self.box_size)/2, float(self.box_size)/2))
            elif 'zlo' in i.split():
                arq.write('{} {} zlo zhi\n'.format(-float(self.box_size)/2, float(self.box_size)/2))
            else:
                arq.write(i)
        arq.write(self.modify)
        for i in arqv[self.end + 1:]:
            arq.write(i)
        arq.close()
        print('File new_{} was created'.format(self.data))

if __name__ == '__main__':
    pacKing()
