##   PYTHON FILE HEADER #
##
##   File:         [CD.py]
##
##   Author(s):    ['Pedro H.F Matias']
##   Site(s):      ['https://github.com/phfmatias']
##   Email(s):     ['phfmatias@discente.ufg.br']
##   Credits:      ['Copyright © 2025 LEEDMOL. All rights reserved.']
##   Date:         ['06.01.2025']
##   Version:      ['0.0.1']
##   Status:       ['Development']
##   Language:     ['Python']
##   Description:  ['This script is used to calculate and plot ECD and VCD spectra using Multiwfn software.']
##   Usage:		   ['python3 CD.py <arq>' or 'python3 CD.py <arq> <initial_x> <final_x> <step_x>']

from pandas import DataFrame
import matplotlib.pyplot as plt
from sys import argv
from os import system, path

arq = argv[-1]
initial_x = None
final_x = None
step = 25

if len(argv) == 5:
    arq = argv[1]
    initial_x = float(argv[2])
    final_x = float(argv[3])
    step_x = float(argv[4])

class CD:
    def __init__(self, arq):
        self.name = arq
        self.arq = open(arq, 'r').readlines()
        
        asw = self.detect_cd(self.arq)

        if asw == 'ECD':
            self.run_elCD()
            self.getData('ECD')
            self.plot_ECD()

        elif asw == 'VCD':
            self.run_vibCD()
            self.getData('VCD')
            self.plot_VCD()

        else:
            print('Error: CD calculation failed.')
            exit()

    def detect_cd(self, file):
        for i in range(len(file)):
            if 'td' in file[i]:
                return 'ECD'
            elif 'freq=VCD' in file[i]:
                return 'VCD' 

    def run_elCD(self):
        arq = open('temp.txt', 'w')

        if len(argv) == 5:
            arq.write('11\n4\n2\n3\n{},{},{}\n2\n-3\nq'.format(initial_x, final_x, step_x))
        else:
            arq.write('11\n4\n2\n2\n-3\nq')
        arq.close()
        system('Multiwfn_3.8 {} < temp.txt'.format(self.name))
        
        if path.exists('spectrum_curve.txt') and path.exists('spectrum_line.txt'):
            system('mv spectrum_curve.txt spectrum_curve_ecd.txt')
            system('mv spectrum_line.txt spectrum_line_ecd.txt')
            system('rm temp.txt')

        else:
            print('Error: ECD calculation failed.')
            exit()

    def run_vibCD(self):
        arq = open('temp.txt', 'w')
        arq.write('11\n5\n14\n\n\n\n2\n-3\nq')
        arq.close()

        system('Multiwfn_3.8 {} < temp.txt'.format(self.name))

        if path.exists('spectrum_curve.txt') and path.exists('spectrum_line.txt'):
            system('mv spectrum_curve.txt spectrum_curve_vcd.txt')
            system('mv spectrum_line.txt spectrum_line_vcd.txt')
            system('rm temp.txt')
        
        else:
            print('Error: VCD calculation failed.')
            exit()

    def getData(self,asw):
        self.sc = DataFrame(columns=['x','y'])
        self.sl = DataFrame(columns=['x','y'])

        if asw == 'ECD':
            arq = open('spectrum_curve_ecd.txt', 'r').readlines()
            arq2 = open('spectrum_line_ecd.txt', 'r').readlines()
        else:
            arq = open('spectrum_curve_vcd.txt', 'r').readlines()
            arq2 = open('spectrum_line_vcd.txt', 'r').readlines()

        for i in range(len(arq)):
            x = float(arq[i].split()[0])
            y = float(arq[i].split()[1])

            self.sc = self.sc._append({'x': x, 'y': y}, ignore_index=True)

        for j in range(len(arq2)-1):
            x = float(arq2[j].split()[0])
            y = float(arq2[j].split()[1])

            self.sl = self.sl._append({'x': x, 'y': y}, ignore_index=True)

    def plot_ECD(self):
        
        fig = plt.figure(figsize=(8,8))
        ax = fig.add_subplot(111)
        ax.plot(self.sc['x'].values, self.sc['y'].values, color='#0005FF')
        ax.fill_between(self.sc['x'].values, self.sc['y'].values, color='#0005FF', alpha=0.3)

        print('---------------------------------------')
        print('The minimum value of the X-axis is: {}'.format(min(self.sc['x'])))
        print('The maximum value of the X-axis is: {}'.format(max(self.sc['x'])))
        print('---------------------------------------')

        ax.set_ylabel(r'$\mathbf{\Delta \epsilon}$' +' (arb.)', fontsize=14, fontweight='bold')
        ax.set_xlim(min(self.sc['x']), max(self.sc['x']))
        ax.set_xlabel('Comprimento de Onda (nm)', fontsize=14, fontweight='bold')

        ax.hlines(0, min(self.sc['x'].values), max(self.sc['x'].values), color='black')
        
        ax.grid(linestyle='--', color='black', alpha=0.3)
        plt.savefig('{}_ECD.png'.format(self.name), dpi=300)
        plt.close()

    def plot_VCD(self):
        fig = plt.figure(figsize=(8,8))
        ax = fig.add_subplot(111)

        ax.plot(self.sc['x'].values, self.sc['y'].values, color='#0005FF')
        ax.fill_between(self.sc['x'].values, self.sc['y'].values, color='#0005FF', alpha=0.3)
        ax.set_ylabel(r'$\mathbf{\Delta \epsilon}$' +' (arb.)', fontsize=14, fontweight='bold')
        ax.set_xlabel('Número de Onda ($\mathbf{cm^{-1}}$)', fontsize=14, fontweight='bold')
        ax.set_xlim(min(self.sc['x']), max(self.sc['x']))

        ax.hlines(0, min(self.sc['x']), max(self.sc['x']), color='black', linestyle='--', alpha=0.5)

        ax.set_xlim(0,3500)
            
        ax.invert_xaxis()
        ax.grid(linestyle='--', color='black', alpha=0.3)
        plt.savefig('VCD.png', dpi=300)        
        

    def run_VCD(self):
        pass


if __name__ == '__main__':  
    cd = CD(arq)