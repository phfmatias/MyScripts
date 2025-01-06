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

if len(argv) != 2:
    print('################################################################')
    print('#      Alimente o codigo com os arquivos necessarios.          #')
    print('#               python3 MODB3LYP.py mol.gjf                    #')
    print('################################################################')
    exit(0)

class MODB3LYP():
    def __init__(self):
        self.menu()
        self.read_input()
        self.write_input()
        
    def menu(self):
        self.initial = int(input("Digite o valor inicial para %HF: "))
        self.final = int(input("Digite o valor final para %HF: "))
        self.step = int(input("Digite o valor de step para %HF: "))
    
    def read_input(self):
        arq = open(argv[1], 'r').readlines()
        
        for i in range(len(arq)):
            if '* xyz' in arq[i] or '* XYZ' in arq[i]:
                self.start = i

    def write_input(self):       
        for i in range(self.initial, self.final, self.step):
            arq = open(argv[1], 'r').readlines()           

            arq[self.start] = '%method\nScalHFX={}\nend\n'.format(i/100)+arq[self.start]

            out = open(argv[1].split('.')[0]+'_'+str(i)+'.inp', 'w')
            out.writelines(arq)

        print('Arquivos gerados com sucesso!')


if __name__ == '__main__':
    modb3lyp = MODB3LYP()
    
