##   PYTHON FILE HEADER #
##
##   File:         [modHF_Picloram.py]
##
##   Author(s):    ['Pedro H.F Matias']
##   Site(s):      ['https://github.com/phfmatias']
##   Email(s):     ['phfmatias@discente.ufg.br']
##   Credits:      ['Copyright © 2025 LEEDMOL. All rights reserved.']
##   Date:         ['27.05.2025']
##   Version:      ['0.0.1']
##   Status:       ['Development']
##   Language:     ['Python']
##   Description:  ['']
##   Usage:		   ['']

from sys import argv
from os import listdir
from MoleKing import G16LOGfile

class modHF_Picloram:
    def __init__(self):
        self.initial = 0
        self.final = 105
        self.step = 5

        files = [x for x in listdir('.') if '.log' in x]

        for i in files:
            self.createInput(i)

    def handle_Keywords(self, arqName):
        atom, r_p, TS = False, False, False
        if 'Cl' in arqName:
            atom = True
        if 'TS' in arqName:
            TS = True
        else:
            r_p = True

        if atom:
            return 'freq=noraman empiricaldispersion=pfd int=ultrafine scf=(novaracc,xqc,maxcycle=10000)'
        
        if r_p:
            return 'opt=calcfc freq=noraman empiricaldispersion=pfd int=ultrafine scf=(novaracc,xqc,maxcycle=10000)'
        if TS:
            return 'opt=(calcfc,ts,maxcycle=100000,noeigentest) freq=noraman scrf=smd empiricaldispersion(pfd) int=ultrafine scf=(novaracc,xqc,maxcycle=10000) volume'
        
    def createInput(self, arq):
        
        mol = G16LOGfile(arq).getMolecule()
        
        for i in range(self.initial, self.final, self.step):

            if 'Cl' in arq or 'TS' in arq:
                mol.setCharge(0)
                mol.setMultiplicity(2)
                mol.toGJF(fileName=arq.replace('.log', '_{}_HF.gjf'.format(i)), method='B3LYP', basis='6-31+g(d)', addKeywords=self.handle_Keywords(arq), modHF=i)

            else:            
                mol.toGJF(fileName=arq.replace('.log', '_{}_HF.gjf'.format(i)), method='B3LYP', basis='6-31+g(d)', addKeywords=self.handle_Keywords(arq), modHF=i)




if __name__ == '__main__':
    modHF_Picloram()