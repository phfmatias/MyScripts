##   PYTHON FILE HEADER #
##
##   File:         [MOD_B3LYP.py]
##
##   Author(s):    ['Pedro H.F Matias']
##   Site(s):      ['https://github.com/phfmatias']
##   Email(s):     ['phfmatias@discente.ufg.br']
##   Credits:      ['Copyright © 2024 LEEDMOL. All rights reserved.']
##   Date:         ['07.08.2024']
##   Version:      ['0.0.1']
##   Status:       ['Development']
##   Language:     ['Python']
##   Description:  ['Script to perform a HF titration in B3LYP']
##   Usage:		   ['python3 MOD_B3LYP <mol.gjf>']


from sys import argv
from MoleKing import G16LOGfile

if len(argv) != 2:
    print('################################################################')
    print('#      Alimente o codigo com os arquivos necessarios.          #')
    print('#               python3 MODB3LYP.py mol.gjf                    #')
    print('################################################################')
    exit(0)

class MODB3LYP():
    def __init__(self):
        self.menu()
        self.get_mol()
        self.write_input()
        
    def menu(self):
        # self.initial = int(input("Digite o valor inicial para %HF: "))
        # self.final = int(input("Digite o valor final para %HF: "))
        # self.step = int(input("Digite o valor de step para %HF: "))

        self.initial = 15
        self.final = 26
        self.step = 1

    def get_mol(self):
        self.mol = G16LOGfile(argv[1], cpAsw=True).getMolecule()

    def write_input(self):
        for i in range(self.initial, self.final, self.step):

            p2 = i
            p1 = 100 - p2

            name = argv[1].split('.')[0]+'_'+str(i)+'.gjf'
            method = 'B3LYP'
            self.base = '6-31+g(d)'

            if p2 == 0:
                keyword = str('NoSymm density=current polar=gamma IOP(3/76=0'+str(p1)+'000'+str(p2)+'00) IOP(3/77=0900010000)')
                self.mol.toGJF(fileName=name, method=method, basis=self.base, addKeywords=keyword, midKeywords=' 0.000 0.04282')
                #arq.write('#p B3LYP/{} {} IOP(3/76=0'.format(self.base,self.additionalKeywords)+str(p1)+'000'+str(p2)+'00) IOP(3/77=0900010000)\n')

            elif p2 > 0 and p2 < 10:
                keyword = str('NoSymm density=current polar=gamma IOP(3/76=00'+str(p2)+'000'+str(p1)+'00) IOP(3/77=0900010000)')
                self.mol.toGJF(fileName=name, method=method, basis=self.base, addKeywords=keyword, midKeywords=' 0.000 0.04282')
                #arq.write('#p B3LYP/{} {} IOP(3/76=00'.format(self.base, self.additionalKeywords)+str(p2)+'000'+str(p1)+'00) IOP(3/77=0900010000)\n')
            elif p2 >= 10 and p2 < 100:
                keyword=str('NoSymm density=current polar=gamma IOP(3/76=0'+str(p1)+'000'+str(p2)+'00) IOP(3/77=0900010000)')
                self.mol.toGJF(fileName=name, method=method, basis=self.base, addKeywords=keyword, midKeywords=' 0.000 0.04282')
                #arq.write('#p B3LYP/{} {} IOP(3/76=0'.format(self.base, self.additionalKeywords)+str(p1)+'000'+str(p2)+'00) IOP(3/77=0900010000)\n')
            else:
                keyword=str('NoSymm density=current polar=gamma IOP(3/76='+str(p2)+'000'+str(p1)+'00) IOP(3/77=0900010000)')
                self.mol.toGJF(fileName=name, method=method, basis=self.base, addKeywords=keyword, midKeywords=' 0.000 0.04282')
                #arq.write('#p B3LYP/{} {} IOP(3/76='.format(self.base,self.additionalKeywords)+str(p2)+'000'+str(p1)+'00) IOP(3/77=0900010000)\n')

        print('Arquivos gerados com sucesso!')


if __name__ == '__main__':
    modb3lyp = MODB3LYP()
    
