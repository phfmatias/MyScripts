##   PYTHON FILE HEADER #
##
##   File:         [checkGaussian.py]
##
##   Author(s):    ['Pedro H.F Matias']
##   Site(s):      ['https://github.com/phfmatias']
##   Email(s):     ['phfmatias@discente.ufg.br']
##   Credits:      ['Copyright © 2025 LEEDMOL. All rights reserved.']
##   Date:         ['10.02.2025']
##   Version:      ['0.0.1']
##   Status:       ['Development']
##   Language:     ['Python']
##   Description:  ['Check the status of Gaussian jobs']
##   Usage:		   ['python checkGaussian.py']


from os import listdir, system, mkdir, chdir


files = [x for x in listdir() if '.gjf' in x]

nt = []
et = []
running = []
nt = []

if 'Error' not in listdir():
    mkdir('Error')
if 'NotRunned' not in listdir():
    mkdir('NotRunned')
if 'Running' not in listdir():
    mkdir('Running')

for file in files:
    if file.replace('.gjf', '.log') in listdir():
        #read reversed

        arq = open(file.replace('.gjf', '.log'), 'r')
        arq = arq.readlines()

        if 'Normal termination' in arq[-1]:
            nt.append(file)

        else:
            if 'Error termination' in arq[-4] or 'Error termination' in arq[-5]:
                system('mv {}.* Error/'.format(file.split('.')[0]))
                et.append(file)
            else:
                pid = int(arq[5].split()[-1].split('.')[0])
                if system(f'ps -p {pid} > /dev/null') == 0: # running
                    system(f'cp {file.rsplit(".", 1)[0]}* Running/')
                    running.append(file)
                else:
                    system(f'cp {file.rsplit(".", 1)[0]}* NotRunned/')
                    nt.append(file)
                
    else:
        system(f'cp {file} NotRunned/')
        nt.append(file)

arq = open('status.txt', 'w')

arq.write('Normal Termination:\n')
for i in nt:
    arq.write(i+'\n')

arq.write('\nError Termination:\n')
for i in et:
    arq.write(i+'\n')

arq.write('\nRunning:\n')
for i in running:
    arq.write(i+'\n')

arq.write('\nQueue or you forgot to submit:\n')
for i in files:
    if i not in nt and i not in et and i not in running:
        arq.write(i+'\n')
        