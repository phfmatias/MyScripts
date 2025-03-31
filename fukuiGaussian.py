##   PYTHON FILE HEADER #
##
##   File:         [fukuiOrca.py]
##
##   Author(s):    ['Pedro H.F Matias']
##   Credits:      ['Copyright © 2024 LEEDMOL. All rights reserved.']
##   Date:         ['17.06.2024']
##   Version:      ['0.0.1']
##   Status:       ['Development']
##   Language:     ['Python']
##   Description:  ['Python script that automates the calculation of Fukui functions using Gaussian software.']
##   Usage:        ['python fukuiGaussian.py <input_file>']

from MoleKing import G16LOGfile
from os import chdir, system, getcwd
import matplotlib.pyplot as plt
from sys import argv

class Fukui():
    def __init__(self):

        if len(argv) == 1:
            self.control()
            self.extractXYZ()
            self.createGaussianInput()
            self.runGaussian()
            self.detectNormal()
            self.runMWFN(self.doMWFN)
        
        if argv[-1] == 'external':
            self.control()
            self.runMWFN(True, True)
        
        if argv[-1] == 'plot':
            self.systemName = argv[-2]
            self.plotFukui()

    def control(self):
        self.input = 0
        self.method = 0
        self.basis = 0
        self.orcaPath = 0
        self.MWFNPath = 0
        self.systemName = 'System Default'
        self.doMWFN = False

        arq = open('fukuiGaussian.inp', 'r').readlines()
        for i in range(len(arq)):
            if 'input' in arq[i]:
                self.input = arq[i].split()[2]
            if 'method' in arq[i]:
                self.method = arq[i].split()[2]
            if 'basis' in arq[i]:
                self.basis = arq[i].split()[2]
            if 'gaussPath' in arq[i]:
                self.gausPath = arq[i].split()[2]
            if 'MWFNPath' in arq[i]:
                self.MWFNPath = arq[i].split()[2]
            if 'nproc' in arq[i]:
                self.nproc = arq[i].split()[2]
            if 'mem' in arq[i]:
                self.maxcore = arq[i].split()[2]
            if 'SystemName' in arq[i]:
                self.systemName = arq[i].split()[2]
            if 'doMWFN' in arq[i]:
                self.doMWFN = arq[i].split()[2]

    def extractXYZ(self):
        if self.input.split('.')[-1] == 'log':
            self.geom = G16LOGfile(self.input).getMolecule()

        else:
            pass

    def createGaussianInput(self):
        N = self.geom.toGJF(fileName='N', method=self.method, basis=self.basis, charge=0, multiplicity=1)
        Nm1 = self.geom.toGJF(fileName='N-1', method=self.method, basis=self.basis, charge=1, multiplicity=2)
        Np1 = self.geom.toGJF(fileName='N+1', method=self.method, basis=self.basis, charge=-1, multiplicity=2)

        system('rm -rf N N-1 N+1')
        system('mkdir N N-1 N+1')
        chdir('N')
        system('mv ../N.gjf .')
        chdir('..')
        chdir('N-1')
        system('mv ../N-1.gjf .')
        chdir('..')
        chdir('N+1')
        system('mv ../N+1.gjf .')
        chdir('..')

    def runGaussian(self):
        chdir('N')
        print('Running N at {}'.format(getcwd()))
        system(f'g16 N.gjf')
        print('Formchk N')
        system('formchk N.chk N.fchk')
        chdir('..')

        chdir('N-1')
        print('Running N-1 at {}'.format(getcwd()))
        system(f'g16 N-1.gjf')
        print('Formchk N-1')
        system('formchk N-1.chk N-1.fchk')
        chdir('..')

        chdir('N+1')
        print('Running N+1 at {}'.format(getcwd()))
        system(f'g16 N+1.gjf')
        print('Formchk N+1')
        system('formchk N+1.chk N+1.fchk')
        chdir('..')

    def detectNormal(self):
        try:
            chdir('N')
            N_nroaml = G16LOGfile('N.log')
            chdir('..')
        except:
            print('Error: Calculation for N failed.')
            exit()

        try:
            chdir('N-1')
            Nm1_normal = G16LOGfile('N-1.log')
            chdir('..')
        
        except:
            print('Error: Calculation for N-1 failed.')
            exit()

        try:
            chdir('N+1')
            Np1_normal = G16LOGfile('N+1.log')
            chdir('..')

        except:
            print('Error: Calculation for N+1 failed.')      
            exit() 

    def runMWFN(self,doMWFN, external=False):

        if not external:

            system('rm -rf MFWN')
            system('mkdir MFWN')
            
            chdir('MFWN')

            system('cp ../N/*.fchk .')
            system('cp ../N+1/*.fchk .')
            system('cp ../N-1/*.fchk .')

            print('Creating MWFN.sh at {}'.format(getcwd()))
            arq = open('MWFN.sh', 'w')
            arq.write('''{} N.fchk > FUKUI.log << !
22
2
N.fchk
N+1.fchk
N-1.fchk
3
N.fchk
N+1.fchk
N-1.fchk                 
2
5
6
7
0
0
q
!'''.format(self.MWFNPath))
            arq.close()

            if self.doMWFN == True:
                print('\n Running MWFN at {}'.format(getcwd()))
                system('bash MWFN.sh')
                self.plotFukui()
            else:
                pass
            chdir('../')
        
        if external:
            
            chdir('MFWN')
            print('Running MWFN at {}'.format(getcwd()))
            system('bash MWFN.sh')
            self.plotFukui()
            chdir('../')

    def plotFukui(self):
            file = open('CDFT.txt', 'r').readlines()

            for i in range(len(file)):
                file[i] = file[i].split()
                if 'Atom' in file[i]:
                    start = i + 1
                if 'Condensed' in file[i]:
                    end = i - 1
                    break

            dict_f0 = {}
            dict_fp = {}
            dict_fm = {}

            for i in range(start, end):
                name = file[i][0].split('(')[1]+file[i][0].split('(')[0]
                dict_f0.update({name: float(file[i][7])})
                dict_fp.update({name: float(file[i][6])})
                dict_fm.update({name: float(file[i][5])})

            dict_f0 = {k: v for k, v in sorted(dict_f0.items(), key=lambda x: x[1], reverse=True)}
            dict_fp = {k: v for k, v in sorted(dict_fp.items(), key=lambda x: x[1], reverse=True)}
            dict_fm = {k: v for k, v in sorted(dict_fm.items(), key=lambda x: x[1], reverse=True)} 

            if len(dict_f0.keys()) < 5:
                sizePlots = len(dict_f0.keys())
            else:
                sizePlots = 5

            for i in range(3):
                if i == 0:
                    dictUse = dict_f0
                    label1 = 'f0'
                    label2 = r'Fukui Parameter ($\mathbf{f_{0}}$)'
                if i == 1:
                    dictUse = dict_fm
                    label1 = 'f-'
                    label2 = r'Fukui Parameter ($\mathbf{f_{-}}$)'
                if i == 2:
                    dictUse = dict_fp
                    label1 = 'f+'
                    label2 = r'Fukui Parameter ($\mathbf{f_{+}}$)'           
            
                fig = plt.figure(figsize=(20, 10))
                ax = fig.add_subplot(111)
                bar = []
                for i in range(sizePlots):
                    bar += ax.bar(list(dictUse.keys())[i], float(list(dictUse.values())[i]), color='b', label=label1, width=0.5)
                for i in range(len(bar)):
                    if bar[i].get_height() < 0:
                        ax.text(bar[i].get_x() + bar[i].get_width()/2, bar[i].get_height(), '{:.3f}'.format(bar[i].get_height()), ha='center', va='top', fontsize=12)
                    else:
                        ax.text(bar[i].get_x() + bar[i].get_width()/2, bar[i].get_height()+0.0005, '{:.3f}'.format(bar[i].get_height()), ha='center', va='bottom', fontsize=12)

                plt.yticks(fontweight='bold', fontsize=12)
                plt.xticks(fontweight='bold', fontsize=12)
                ax.set_ylabel(label2, fontsize=20, fontweight='bold', labelpad=15)
                ax.set_xlabel('Atoms in {}'.format(self.systemName), fontsize=20, fontweight='bold', labelpad=15)
                plt.savefig('{}_{}.png'.format(self.systemName, label1))

        
if __name__ == '__main__':
    x = Fukui()

    if argv[-1] == 'plot':
        x.plotFukui()

'''
INPUT EXAMPLE

input = water.log
method = B3LYP  
basis = STO-3G
gaussPath = g16
MWFNPath = Multiwfn_3.8
nproc = 6
mem = 16
SystemName = Water.log
doMWFN = True
'''