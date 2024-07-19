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
##   Description:  ['Python script that automates the calculation of Fukui functions using ORCA software.']
##   Usage:        ['python fukuiOrca.py <input_file>']

from sys import argv
from os import chdir, system, getcwd, popen
import matplotlib.pyplot as plt

class Fukui():
    def __init__(self):
        self.control()
        self.extractXYZ()
        self.createN()
        self.extractLOG()
        self.createNp1()
        self.createNm1()
        self.runMFWN()

    def control(self):
        self.input = 0
        self.method = 0
        self.basis = 0
        self.orcaPath = 0
        self.MWFNPath = 0
        self.systemName = 'System Default'

        arq = open('fukuiOrca.inp', 'r').readlines()
        for i in range(len(arq)):
            if 'input' in arq[i]:
                self.input = arq[i].split()[2]
            if 'method' in arq[i]:
                self.method = arq[i].split()[2]
            if 'basis' in arq[i]:
                self.basis = arq[i].split()[2]
            if 'orcaPath' in arq[i]:
                self.orcaPath = arq[i].split()[2]
            if 'MWFNPath' in arq[i]:
                self.MWFNPath = arq[i].split()[2]
            if 'nproc' in arq[i]:
                self.nproc = arq[i].split()[2]
            if 'mem' in arq[i]:
                self.maxcore = arq[i].split()[2]
            if 'SystemName' in arq[i]:
                self.systemName = arq[i].split()[2]

        if self.input == 0 or self.method == 0 or self.basis == 0 or self.orcaPath == 0:
            print('Error: Check the input file.')
            exit()

        if self.nproc == 0:
            self.nproc = 1
        if self.maxcore == 0:
            self.maxcore = 1000

        if self.MWFNPath == 0:
            print('Error: MWFNPath not defined.')
            exit()
        
        if self.orcaPath == 0:
            print('Error: ORCAPath not defined.')
            exit()
            
    def extractXYZ(self):
        arq = open(self.input, 'r').readlines()
        self.Geom = ''.join(arq[2:])
    
    def extractLOG(self):
        chdir('N')
        arq = open('N.xyz', 'r').readlines()
        self.NGeom = ''.join(arq[2:])
        chdir('../')

    def createN(self):
        self.extractXYZ()
        
        system('rm -rf N')
        system('mkdir N')
        chdir('N/')

        arq = open('N.inp', 'w')    
        arq.write('%maxcore ' + self.maxcore + '\n')
        arq.write('%pal nprocs ' + self.nproc + '\nend\n')
        arq.write('!' + self.method + ' ' + self.basis + ' OPT KEEPDENS\n')
        arq.write('* XYZ 0 1 \n')
        arq.write(self.Geom)
        arq.write('*')
        arq.close()

        print('\nRunning N at: ', getcwd())
        process = popen(self.orcaPath + ' N.inp > N.log')
        process.read()
        process.close()

        chdir('../')

        self.detectNormal('neutral')
        system('orca_2aim N/N')

    def createNp1(self):
        system('rm -rf N+1/')
        system('mkdir N+1')
        chdir('N+1')

        arq = open('N+1.inp', 'w')
        arq.write('%maxcore ' + self.maxcore + '\n')
        arq.write('%pal nprocs ' + self.nproc + '\nend\n')
        arq.write('!' + self.method + ' ' + self.basis + ' KEEPDENS\n')
        arq.write('* XYZ -1 2 \n')
        arq.write(self.NGeom)
        arq.write('*')
        arq.close()

        print('\nRunning N+1 at: ', getcwd())
        process = popen(self.orcaPath + ' N+1.inp > N+1.log')
        process.read()
        process.close()

        chdir('../')

        self.detectNormal('anion')
        system('orca_2aim N+1/N+1')

    def createNm1(self):
        system('rm -rf N-1/')
        system('mkdir N-1')
        chdir('N-1')

        arq = open('N-1.inp', 'w')
        arq.write('%maxcore ' + self.maxcore + '\n')
        arq.write('%pal nprocs ' + self.nproc + '\nend\n')
        arq.write('!' + self.method + ' ' + self.basis + ' KEEPDENS\n')
        arq.write('* XYZ 1 2 \n')
        arq.write(self.NGeom)
        arq.write('*')
        arq.close()

        print('\nRunning N-1 at: ', getcwd())
        process = popen(self.orcaPath + ' N-1.inp > N-1.log')
        process.read()
        process.close()

        chdir('../')

        self.detectNormal('cation')
        system('orca_2aim N-1/N-1')

    def detectNormal(self, System):
        normal = False

        if System == 'neutral':
            chdir('N')
            log2open = 'N.log'

        elif System == 'cation':
            chdir('N-1')
            log2open = 'N-1.log'
        
        elif System == 'anion':
            chdir('N+1')
            log2open = 'N+1.log'
    
        log = open(log2open, 'r').readlines()[::-1]
        for i in range(len(log)):
            if '****ORCA TERMINATED NORMALLY****' in log[i]:
                normal = True
                break
        chdir('../')
                
        if not normal:
            print('Error: ORCA did not terminate normally in the {} system.'.format(System))
            exit()


    def runMFWN(self):
        system('rm -rf MFWN')
        system('mkdir MFWN')
        
        chdir('MFWN')

        system('cp ../N/*.wfn .')
        system('cp ../N+1/*.wfn .')
        system('cp ../N-1/*.wfn .')

        arq = open('MFWN.sh', 'w')
        arq.write('''{} N.wfn > FUKUI.log << !
22
2
3
2
5
6
7
0
0
q
!'''.format(self.MWFNPath))
        arq.close()

        print('\nRunning MWFN at: ', getcwd())
        system('bash MFWN.sh')


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

'''
INPUT EXAMPLE

input = etano.xyz
method = M062X
basis = 6-31+G(d,p)
orcaPath = orca
MWFNPath = Multiwfn_3.8
nproc = 1
mem = 6000
SystemName = Etano
'''