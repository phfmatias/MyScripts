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
        self.base = input("Digite a base: ")
        self.additionalKeywords = input("Digite as palavras chaves adicionais: ")
    
    def read_input(self):
        arq = open(argv[1], 'r').readlines()
        self.mol = ''

        for i in range(len(arq)):
            if '0 1' in arq[i]:
                start = i+1

        for i in range(start, len(arq)):
            if '\n' == arq[i]:
                break
            else:
                self.mol += arq[i]

    def write_input(self):
        for i in range(self.initial, self.final, self.step):
            arq = open(argv[1].split('.')[0]+'_'+str(i)+'.gjf', 'w')
            arq.write('%chk='+argv[1].split('.')[0]+'_'+str(i)+'.chk\n')

            p2 = i
            p1 = 100 - p2

            if p2 == 0:
                arq.write('#p B3LYP/{} {} IOP(3/76=0'.format(self.base,self.additionalKeywords)+str(p1)+'000'+str(p2)+'00) IOP(3/77=0900010000)\n')
            elif p2 > 0 and p2 < 10:
                arq.write('#p B3LYP/{} {} IOP(3/76=00'.format(self.base, self.additionalKeywords)+str(p2)+'000'+str(p1)+'00) IOP(3/77=0900010000)\n')
            elif p2 >= 10 and p2 < 100:
                arq.write('#p B3LYP/{} {} IOP(3/76=0'.format(self.base, self.additionalKeywords)+str(p1)+'000'+str(p2)+'00) IOP(3/77=0900010000)\n')
            else:
                arq.write('#p B3LYP/{} {} IOP(3/76='.format(self.base,self.additionalKeywords)+str(p2)+'000'+str(p1)+'00) IOP(3/77=0900010000)\n')

            arq.write('\n {}_{} \n\n'.format(argv[1].split('.')[0], i))
            arq.write('0 1\n')
            arq.write(self.mol)
            arq.write('\n\n')

        print('Arquivos gerados com sucesso!')


if __name__ == '__main__':
    modb3lyp = MODB3LYP()
    
