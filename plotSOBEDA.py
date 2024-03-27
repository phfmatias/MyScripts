##   PYTHON FILE HEADER #
##
##   File:         [PlotSOBEDA.py]
##
##   Author(s):    ['Pedro H.F Matias']
##   Credits:      ['Copyright © 2024 LEEDMOL. All rights reserved.']
##   Date:         ['27.03.2024']
##   Version:      ['0.0.1']
##   Status:       ['Development']
##   Language:     ['Python']
##   Description:  ['Python script to plot the SOBEDA results from the .log']
##   Usage:        ['python3 PlotSOBEDA.py [file] [name]']

import matplotlib.pyplot as plt
from sys import argv

class Plotter ():
    def __init__(self, file, name) -> None:
        self.file = file
        self.name = name
        self.load()
        self.plot_SAPTLike()
        self.plot_SOBEDA()

    def load(self):
        rlines = open(self.file, 'r').readlines()

        start = 0

        for i in range(len(rlines)):
            if rlines[i].startswith("***** Final results *****:"):
                start = i
                break
        
        for i in range(start, len(rlines)):
            if 'Electrostatic (E_els):' in rlines[i]:
                self.E_elst = float(rlines[i].split()[2])
            
            if 'Exchange (E_x):' in rlines[i]:
                self.E_x = float(rlines[i].split()[2])
            
            if 'Pauli repulsion (E_rep):' in rlines[i]:
                self.E_pauli = float(rlines[i].split()[3])
            
            if 'Exchange-repulsion (E_xrep = E_x + E_rep):' in rlines[i]:
                self.E_xrep = float(rlines[i].split()[6])
            
            if 'Orbital (E_orb):' in rlines[i]:
                self.E_orb = float(rlines[i].split()[2])
            
            if 'DFT correlation (E_DFTc):' in rlines[i]:
                self.E_DFTc = float(rlines[i].split()[3])

            if 'Dispersion correction (E_dc):' in rlines[i]:
                self.E_dc = float(rlines[i].split()[3])

            if 'Exchange-repulsion (including scaled DFT correlation):' in rlines[i]:
                self.Exrep = float(rlines[i].split()[5])

            if 'Dispersion (E_disp):' in rlines[i]:
                self.disp = float(rlines[i].split()[2])

        self.corr = self.E_DFTc + self.E_dc
    
    def checkAttr(self):
        try:
            self.E_elst
            self.Exrep
            self.E_orb
            self.disp
        except AttributeError:
            print("Missing variables for SAPT-like plot, we'll skip it.")

    def plot_SOBEDA(self):
        E_total = self.E_elst + self.E_x + self.E_pauli + self.E_orb + self.E_DFTc + self.disp

        figure2 = plt.figure()
        ax2 = figure2.add_subplot(111)
        ax2.set_ylabel('Energy (kcal/mol)')
        x =  ax2.bar(0, self.E_elst,  color='#ff0004')
        x += ax2.bar(1, self.E_x,     color='#00ff00')
        x += ax2.bar(2, self.E_pauli, color='#0000ff')
        x += ax2.bar(3, self.E_orb,   color='#104800')
        x += ax2.bar(4, self.E_DFTc,  color='#f261ff')
        x += ax2.bar(5, self.disp,    color='#ffaa00')
        x += ax2.bar(6, E_total,      color='#000000')
 
        for bar in x:
            if bar.get_height() < 0:
                ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height()*1.02, '{}'.format(bar.get_height()), ha='center', va='top',fontsize=6,fontweight='bold')
            else:
                ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height()*1.015, '{}'.format(bar.get_height()), ha='center', va='bottom',fontsize=6,fontweight='bold')
        ax2.hlines(0, -1, 6.5, colors='k', linestyles='solid')
        ax2.set_xlim(-0.5, 6.5)
        ax2.set_xticks([0,1,2,3,4,5,6])
        ax2.set_xticklabels(['Electrostatic', 'Exchange', 'Pauli Repulsion', 'Orbital', 'DFTc', 'Dispersion', 'Total Energy'], fontweight='bold', fontsize=6)
        plt.savefig('SOBEDA_Plot_{}.png'.format(self.name), dpi=300, bbox_inches='tight')
       

    def plot_SAPTLike(self):
        self.checkAttr()      

        E_Total = self.E_elst + self.Exrep + self.E_orb + self.disp
        figure = plt.figure('SAPT_LIKE')
        ax = figure.add_subplot(111)
        x = ax.bar(0, self.E_elst, color='#ff0004', label='Electrostatic')
        x += ax.bar(1, self.Exrep, color='#00ff00', label='Exchange-Repulsion')
        x += ax.bar(2, self.E_orb, color='#104800', label='Orbital')
        x += ax.bar(3, self.disp,  color='#ffaa00', label='Dispersion')
        x += ax.bar(4, E_Total,    color='#000000', label='Total Energy')
        for bar in x:
            if bar.get_height() < 0:
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()*1.02, '{}'.format(bar.get_height()), ha='center', va='top',fontsize=6,fontweight='bold')
            else:
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()*1.015, '{}'.format(bar.get_height()), ha='center', va='bottom',fontsize=6,fontweight='bold')
        ax.hlines(0, -1, 4.5, colors='k', linestyles='solid')
        ax.set_xlim(-0.5, 4.5)
        ax.set_xticks([0,1,2,3,4])
        ax.set_xticklabels(['Electrostatic', 'Exchange', 'Orbital', 'Dispersion', 'Total Energy'], fontweight='bold', fontsize=10, rotation=0)
        ax.set_ylabel(r'Energy (kcal $\mathbf{mol^{-1}}$)', fontweight='bold', fontsize=10)
        plt.savefig('SAPT_Like_{}.png'.format(self.name), dpi=300)

if __name__ == "__main__":
    if len(argv) != 3:
        print("Usage: python3 PlotSOBEDA.py [file] [name]")
        exit(1)
    else:
        
        x = Plotter(argv[-2],argv[-1])


