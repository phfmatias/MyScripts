##   PYTHON FILE HEADER #
##
##   File:         [slurmking.py]
##
##   Author(s):    ['Pedro H.F Matias']
##   Site(s):      ['https://github.com/phfmatias']
##   Email(s):     ['phfmatias@discente.ufg.br']
##   Credits:      ['Copyright © 2023 LEEDMOL. All rights reserved.']
##   Date:         ['18.04.2023']
##   Version:      ['2.1.0']
##   Status:       ['Development']
##   Language:     ['Python']
##   Description:  ['Python package to create slurm files for HPC cluster.']

##   PYTHON FILE HEADER #

##   IMPORTS #

from re import sub, M, search
from os import listdir, path, getcwd
from sys import argv
import subprocess


try:
    import readline
except ImportError:
    import pyreadline as readline

class makeslurm():
    
    def __init__(self):
        self.version = "2.1.0"
        self.home_dir = path.expanduser('~')
        self.msInfo = 'Essa versão {} suporta: g09, g16, psi4, psi4_1.8.0, orca, omega, omegaOrder, cvKing, dice, lammps e cpmd.\n'.format(self.version)
        self.calcs = ["g09", "g16", "psi4", "psi4_1.8.0", "orca", "omega", "omegaOrder", "cvKing", "dice", "lammps", "cpmd"]
        self.filas = ['int_short', 'int_medium', 'int_large', 'amd_short', 'amd_medium', 'amd_large', 'gpu_int_k40', 'gpu_a100_92', 'gpu_a100_64']
        self.regexMemOrca = r"%maxcore\s\d*\s"
        self.regexMem = r"%[A-Za-z]+=\d+[A-Za-z]+\n"
        self.regexMemPSI4 = r"[A-Za-z]+\s*\d*\s*GB\n"
        self.regexMemPSI4_mb = r"[A-Za-z]+\s*\d*\s*mb\n"
        self.regexNproc = r"%[A-Za-z]+=\d+\n"
        self.regexCHK = r"%[A-Za-z]+=.+\.chk\n"
        self.filasInfo = {'int_short':'Pode-se alocar no máximo 80 tasks por usuário, submeter no máximo 10 jobs, e possui (8) nós disponiveis: -> [01-08]\n',
                          'int_medium':'Pode-se alocar no máximo 40 tasks por usuário, submeter no máximo 6 jobs, e possui (8) nós disponiveis: -> [01-08]\n',
                          'int_large':'Pode-se alocar no máximo 20 tasks por usuário, submeter no máximo 4 jobs, e possui (8) nós disponiveis: -> [01-08]\n',
                          'amd_short':'Pode-se alocar no máximo 256 tasks por usuário, submeter no máximo 10 jobs, e possui (9) nós disponiveis: -> [01-08]\n',
                          'amd_medium':'Pode-se alocar no máximo 128 tasks por usuário, submeter no máximo 6 jobs, e possui (9) nós disponiveis: -> [01-08]\n',
                          'amd_large':'Pode-se alocar no máximo 64 tasks por usuário, submeter no máximo 4 jobs, e possui (9) nós disponiveis: -> [01-08]\n',
                          'gpu_int_k40':'Pode-se alocar no máximo 20 tasks por usuário, submeter no máximo 2 jobs, e possui (1) nós disponiveis: -> [01]\n',
                          'gpu_a100_192':'Pode-se alocar no máximo 192 tasks por usuário, submeter no máximo 1 job, e possui (1) nós disponiveis: -> [01]\n',
                          'gpu_a100_64':'Pode-se alocar no máximo 64 tasks por usuário, submeter no máximo 3 job, e possui (1) nós disponiveis: -> [01]\n',
                        }
                          
        self.logWriter(header=True)
        self.create_cache()        

    def create_cache(self):
        if path.exists(self.home_dir+'/.cacheSlurm.txt'):
            pass
        else:
            arq = open(self.home_dir+'/.cacheSlurm.txt','w')
            arq.close()
    
    def check_cache(self,argument):
        arq = open(self.home_dir+'/.cacheSlurm.txt','r')
        rlines = arq.readlines()  

        for i in rlines:
            if argument in i:
                return i.split()[-1]
        return False

    
    def write_cache(self,argument):
        arq = open(self.home_dir+'/.cacheSlurm.txt','a')
        arq.write('\n'+argument)
        arq.close()                    

    def completer(self,text, state):
        options = [calc_opt for calc_opt in self.calcs if calc_opt.startswith(text)]
        if state < len(options):
            return options[state]
        else:
            return None

    def completer_fila(self, text, state):
        options = [calc_opt for calc_opt in self.filas if calc_opt.startswith(text)]
        if state < len(options):
            return options[state]
        else:
            return None

    def getInfos(self):

        self.logWriter(askCalc=True)        
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.completer)
        self.calculo = input()

        if self.calculo in ['g09','g16','psi4', 'psi4_1.8.0', 'orca'] and len(argv) == 1:
            self.logWriter(askInput=True)
            self.infoInput = input() 
            if self.infoInput == 'y':
                self.logWriter(askDivideSlurm=True)
                divideSlurm = input()
                if divideSlurm == 'y':
                    self.logWriter(askNumSlurms=True)
                    self.numSlurms = int(input())
                    if self.numSlurms == 1:
                        print('Por favor, coloque pelo menos 2 slurms.')
                        exit(0)
                else:
                    self.numSlurms = 1
            else:
                self.numSlurms = 1                
                
            if self.calculo == 'g16' or self.calculo == 'g09':
                self.logWriter(askCHK=True)
                self.chkAnsw = input()
        
        elif len(argv) > 1:
            self.infoInput = 'n'

        else:
            self.infoInput = 'n'

        if self.numSlurms == 1:
            if self.infoInput == 'y' or self.calculo in ['dice','cvKing','omega','omegaOrder']:
                self.logWriter(askName=True)
                self.name = input()
            else:
                self.name = ''

        elif self.numSlurms > 1:
            self.logWriter(askName=True)
            self.name = input()

        self.logWriter(askQueue=True)
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.completer_fila)
        self.fila = input()
        
        # self.logWriter(askTime=True)
        # self.time_info = input()

        # if self.time_info == 'y':
        #     self.logWriter(askTimeValue=True)
        #     time = input()
        #     if 'd' in time:
        #         actual_Time = int(time.split('d')[0])

        #         if 'short' in self.fila and actual_Time > 1:    
        #             print('O tempo máximo para a fila short é de 1 dia, estamos alterando para 1 dia.')
        #             actual_Time = 1

        #         elif 'medium' in self.fila and actual_Time > 7:
        #             print('O tempo máximo para a fila medium é de 7 dias, estamos alterando para 7 dias.')
        #             actual_Time = 7
                
        #         elif 'large' in self.fila and 'int' in self.fila and actual_Time > 30:
        #             print('O tempo máximo para a fila int_large é de 30 dias, estamos alterando para 30 dias.')
        #             actual_Time = 30
                
        #         elif self.fila in ['amd_large','gpu_int_k40'] and actual_Time > 15:
        #             print('O tempo máximo para a fila {} é de 15 dias, estamos alterando para 15 dias.'.format(self.fila))
        #             actual_Time = 15
        #         elif 'gpu_a100_192' in self.fila and actual_Time > 14:
        #             print('O tempo máximo para a fila {} é de 14 dias, estamos alterando para 14 dias.'.format(self.fila))
        #         elif 'gpu_a100_64' in self.fila and actual_Time > 5:
        #             print('O tempo máximo para a fila {} é de 5 dias, estamos alterando para 5 dias.'.format(self.fila))
        #             actual_Time = 5
        #         self.time = '{}-00:00:00'.format(actual_Time)
            
        #     elif 'h' in time:
        #         actual_Time = int(time.split('h')[0])
                
        #         if 'short' in self.fila and actual_Time > 24:
        #             print('O tempo máximo para a fila short é de 24 horas, estamos alterando para 24 horas.')
        #             actual_time = 24

        #         if actual_Time > 24:
        #             print('Por favor, se quer mais de 24 horas, coloque em dias.')
        #             exit(0)
        #         self.time = '00-{}:00:00'.format(actual_Time)
        # else:
        #     pass

        self.logWriter(askTask=True)
        self.task = int(input())

        self.logWriter(askNodes=True)
        self.nodes = int(input())

        self.logWriter(askExtension=True)
        self.extension = input()

        # self.logWriter(askEmail=True)
        # self.email = input()

        # if self.email.lower() == 'y':
        #     self.email = True
        #     self.logWriter(askAdress=True)
        #     self.adress = input()
        # else:
        #     self.email = False

        if 'amd' in self.fila or 'amd_':
            self.mem = float(self.task*3.8)
            self.memOrca = 3875 
            self.gaussian = 'gaussian/16b01'        
        elif 'int' in self.fila:
            self.mem = float(self.task*2.2)
            self.memOrca = 2200
            self.gaussian = 'gaussian/16b01'

        self.time_info = 'n'

        if self.time_info == 'n':
            if 'short' in self.fila:
                self.time = '1-00:00:00'
            elif 'medium' in self.fila:
                self.time = '7-00:00:00'
            elif 'large' in self.fila and 'int' in self.fila:
                self.time = '30-00:00:00'
            elif 'amd_large' in self.fila or 'gpu_int_k40' in self.fila:
                self.time = '15-00:00:00'
            elif 'gpu_a100_192' in self.fila:
                self.time = '14-00:00:00'
            elif 'gpu_a100_64' in self.fila:
                self.time = '5-00:00:00'
            else:
                self.time = '15-00:00:00'

        if len(argv) > 1:
            self.arquivos = [argv[1]] 
            self.name = argv[1].split('.')[0]  
        else:
            self.arquivos = [x for x in listdir() if self.extension in x]
                       
    def checkGaussian(self):
        temp = []
        for arqs in self.arquivos:
            if arqs.replace('{}'.format(self.extension), '.out') in listdir() :
                y = open(arqs.replace('{}'.format(self.extension), '.out'),'r').read()
                if 'Normal termination' in y:
                    print('Arquivo {} já foi rodado e deu certo! Não entrará no SLURM!'.format(arqs))
                else:
                    temp.append(arqs)

            elif arqs.replace('{}'.format(self.extension), '.log') in listdir() :
                y = open(arqs.replace('{}'.format(self.extension), '.log'),'r').read()
                if 'Normal termination' in y:
                    print('Arquivo {} já foi rodado e deu certo! Não entrará no SLURM!'.format(arqs))
                else:
                    temp.append(arqs)
            else:
                    temp.append(arqs)
        
        self.arquivos = temp

    def checkOrca(self):
        temp = []
        for arqs in self.arquivos:
            if arqs.replace('{}'.format(self.extension), '.log') in listdir():
                y = open(arqs.replace('{}'.format(self.extension), '.log'),'r').read()
                if 'ORCA TERMINATED NORMALLY' in y:
                    print('Arquivo {} já foi rodado e deu certo! Não entrará no SLURM!'.format(arqs))
                else:
                    print('Estou aqui, e apendei o {}'.format(arqs))
                    temp.append(arqs)
            else:
                temp.append(arqs)               

        self.arquivos = temp

    def checkPsi4(self):
        temp = []
        for arqs in self.arquivos:
            if arqs.replace('{}'.format(self.extension), '.out') in listdir():
                y = open(arqs.replace('{}'.format(self.extension), '.out'),'r').read()
                if 'Buy a developer a beer!' in y:
                    print('Arquivo {} já foi rodado e deu certo! Não entrará no SLURM!'.format(arqs))
                else:
                    temp.append(arqs)
            else:
                temp.append(arqs)

        self.arquivos = temp        

    def changeInput(self):

        self.logWriter(changeInput=True)

        if self.calculo == 'g16' or self.calculo == 'g09':            
            for arq in self.arquivos: 
                if self.chkAnsw == 'y':
                    self.chk = arq.split('.')[0]

                rlines = open(arq,'r').read()
                if search(self.regexMem, rlines, M):
                    rlines = sub('%[A-Za-z]+=\d+[A-Za-z]+\n','%mem={:.0f}GB\n'.format(self.mem),rlines)
                else:
                    rlines = '%mem={:.0f}GB\n'.format(self.mem)+rlines
                if search(self.regexNproc,rlines, M):
                    rlines = sub('%[A-Za-z]+=\d+\n','%nprocshared={}\n'.format(self.task),rlines)
                else:
                    rlines = '%nprocshared={}\n'.format(self.task)+rlines
                if search(self.regexCHK,rlines, M):
                    if self.chkAnsw == 'y':
                        rlines = sub('%[A-Za-z]+=\w+\.chk\n','%chk={}.chk\n'.format(self.chk),rlines)
                else:
                    if self.chkAnsw == 'y':
                        rlines = '%chk={}.chk\n'.format(self.chk)+rlines

                toWrite = open(arq,'w')
                toWrite.write(rlines)

        elif self.calculo == 'orca':
            for arq in self.arquivos:
                rlines = open(arq,'r').read()
                if search(self.regexMemOrca, rlines, M):
                    rlines = sub('%maxcore\s\d*\s','%maxcore {}\n'.format(self.memOrca),rlines)
                    rlines = sub('nprocs\s\d*\s','nprocs {}\n'.format(self.task),rlines)
                else:
                    rlines = '%maxcore {} %pal nprocs {} end\n'.format(self.memOrca, self.task)+rlines
                
                toWrite = open(arq,'w')
                toWrite.write(rlines)
                

        elif self.calculo == 'psi4' or self.calculo == 'psi4_1.8.0':
            for arq in self.arquivos:
                rlines = open(arq,'r').read()
                if search(self.regexMemPSI4_mb, rlines, M):
                    rlines = sub('[A-Za-z]+\s*\d*\s*mb\n','memory {:.0f}GB\n'.format(self.mem),rlines)
                elif search(self.regexMemPSI4, rlines, M):
                    rlines = sub('[A-Za-z]+\s*\d*\s*GB\n','memory {:.0f}GB\n'.format(self.mem),rlines)
                else:
                    rlines = 'memory {:.0f}GB\n'.format(self.mem)+rlines
                
                toWrite = open(arq,'w')
                toWrite.write(rlines)
        
        elif self.calculo == 'dice':
            for arq in self.arquivos:
                rlines = open(arq,'r').read()
                if 'nprocs = ' in rlines:
                    rlines = sub('nprocs = \d+', 'nprocs = {}'.format(self.task), rlines)
                else:
                    rlines = rlines.replace('# diceplayer\n','# diceplayer\nnprocs = {}\n'.format(self.task))
                if 'mem = ' in rlines:
                    rlines = sub('mem = \d+\.*\w*\w\w', 'mem = {:.0f}GB'.format(self.mem), rlines)
                else:
                    rlines = rlines.replace('# Gaussian\n','# Gaussian\nmem = {:.0f}GB\n'.format(self.mem))
                toWrite = open(arq,'w')
                toWrite.write(rlines)

        elif self.calculo == 'cvKing':
            arqs = [x for x in listdir() if '.in' in x]
            for arq in arqs:
                rlines = open(arq,'r').read()
                if 'mem =' in rlines:
                    rlines = sub('mem = \d+\.*\w*\w\w', 'mem = {:.0f}GB'.format(self.mem), rlines)
                else:
                    rlines = rlines + 'mem = {}GB\n'.format(self.mem)
                if 'cpu =' in rlines:
                    rlines = sub('cpu = \d+', 'cpu = {}'.format(self.task), rlines)
                else:
                    rlines = rlines + 'cpu = {}\n'.format(self.task)
                toWrite = open(arq,'w')
                toWrite.write(rlines)

        elif self.calculo == 'omega':
            arqs = [x for x in listdir() if '.in' in x]
            for arq in arqs:
                rlines = open(arq,'r').read()
                if 'mem =' in rlines:
                    rlines = sub('mem = \d+', 'mem = {:.0f}'.format(self.mem), rlines)
                else:
                    rlines = rlines + 'mem = {}\n'.format(self.mem)
                if 'ncores =' in rlines:
                    rlines = sub('ncores = \d+', 'ncores = {}'.format(self.task), rlines)
                else:
                    rlines = rlines + 'ncores = {}\n'.format(self.task)
                toWrite = open(arq,'w')
                toWrite.write(rlines)
        
        elif self.calculo == 'omegaOrder':
            arqs = [x for x in listdir() if '.in' in x]
            for arq in arqs:
                rlines = open(arq,'r').read()
                if 'mem =' in rlines:
                    rlines = sub('mem = \d+', 'mem = {:.0f}'.format(self.mem), rlines)
                else:
                    rlines = rlines + 'mem = {}\n'.format(self.mem)
                if 'ncores =' in rlines:
                    rlines = sub('ncores = \d+', 'ncores = {}'.format(self.task), rlines)
                else:
                    rlines = rlines + 'ncores = {}\n'.format(self.task)
                toWrite = open(arq,'w')
                toWrite.write(rlines)
        
        else:
            pass
        
    def logWriter(self, header=False, askName=False, askInput=False, askCalc=False, askQueue=False, askTask=False, askNodes=False, askExtension=False, askEmail=False, finalMessage=False, askAdress=False, changeInput=False, askCHK=False,askTime=False, askTimeValue=False, askDivideSlurm=False, askNumSlurms=False):

        if header:
            print("")
            print("\t\t\t         _.+._    ")
            print("\t\t\t       (^\/^\/^)  ")
            print("\t\t\t        \@*@*@/   ")
            print("\t\t\t        [_____]   ")
            print("  .d8888b.  888     888     888 8888888b.  888b     d888      ")
            print(" d88P  Y88b 888     888     888 888   Y88b 8888b   d8888      ")
            print(" Y88b.      888     888     888 888    888 88888b.d88888      ")
            print("  'Y888b.   888     888     888 888   d88P 888Y88888P888      ")
            print("     'Y88b. 888     888     888 8888888P'  888 Y888P 888      ")
            print("       '888 888     888     888 888 T88b   888  Y8P  888      ")
            print(" Y88b  d88P 888     Y88b. .d88P 888  T88b  888   '   888      ")
            print("  'Y8888P'  88888888 'Y88888P'  888   T88b 888       888      ")
            print("       888    d8P  8888888 888b    888  .d8888b.              ")
            print("       888   d8P     888   8888b   888 d88P  Y88b             ")
            print("       888  d8P      888   88888b  888 888    888             ")
            print("       888d88K       888   888Y88b 888 888                    ")
            print("       8888888b      888   888 Y88b888 888  88888             ")
            print("       888  Y88b     888   888  Y88888 888    888             ")
            print("       888   Y88b    888   888   Y8888 Y88b  d88P             ")
            print("       888    Y88b 8888888 888    Y888  'Y8888P88             ")                                                                  
            print('\n\n\tDesenvolvido por: Pedro HF e Mateus RB. \t')
            print('\tTodos os direitos reservados ao LEEDMOL. \t \n')
            print("-"*len(self.msInfo))
            print(self.msInfo)
            print("-"*len(self.msInfo))

        elif askCalc:
            print('\nDeseja criar slurm para g09, g16, psi4, psi4_1.8.0, orca, omega, omegaOrder, cvKing, dice, lammps ou cpmd? \n')

        elif askName:
            print('\nQual o nome do seu JOB? Este nome, aparecera na lista de trabalhos (squeue), além de ser o nome do arquivo slurm: \n')

        elif askDivideSlurm:
            print('\nDeseja dividir os cálculos em slurms separados? y ou n: \n')

        elif askNumSlurms:
            print('\nQuantos slurms serão criados? \n')

        elif askInput:
            print('\nDeseja colocar todos inputs no mesmo slurm? y ou n: \n')
        
        elif askQueue:
            print('\nQual fila a ser submetida? int_short, int_medium, int_large, amd_short, amd_medium, amd_large, gpu_int_k40, gpu_a100_192 ou gpu_a100_64: \n')

        elif askTime:
            print('\nVocê tem alguma estimativa de quando acabará seu cálculo? Isto pode adiantar seu cálculo na fila (y ou n): \n')

        elif askTimeValue:
            print('\nQual a estimativa de tempo? Informe apenas, dias ou horas\nExemplo: 1d ou 5h \n')

        elif askCHK:
            print('\nPor padrão, o slurmKing irá adicionar a keyword %chk=NOME_DO_ARQUIVO.chk, deseja continuar? y ou n. (Caso não queira, não será alterado o CHK do arquivo.)\n')

        elif askTask:
            print("\nQuantas tasks serão utilizados? ")
            print(self.filasInfo[self.fila])

        elif askNodes:
            print('\nInforme o numero de nós: \n')

        elif askExtension:
            print('\nQual a extensão do input: \n')

        elif askEmail:
            print('\nDeseja receber notificação via e-mail? (y ou n): \n')   

        elif askAdress:
            print('\nDigite seu endereço de e-mail: \n')

        elif finalMessage:
            print('\nMake slurm criado para {} para o(s) arquivo(s) {} com máxima duração de {} dias na fila {}, utilizando {} nó(s) e {} tasks.\n'.format(self.calculo,self.arquivos, self.time, self.fila, self.nodes,self.task))         
        
        elif changeInput:
            change = ['g16', 'omega', 'omegaOrder', 'cvKing', 'dice']
            if self.calculo in change:
                print('\nAlterando a memória e número de processadores do input para {:.0f} GB e {} respectivamente.\n'.format(self.mem, self.task))
            if self.calculo == 'psi4' or self.calculo == 'psi4_1.8.0':
                print('\nAlterando a memória do input para {:.0f} GB.\n'.format(self.mem))
            else:
                print('\nSlurm para {} criado com sucesso!'.format(self.calculo))
                

        else:
            pass

    def slurmHeader(self):
        self.slurm = "#!/bin/bash\n"
        self.slurm += "#SBATCH --job-name={}\n".format(self.name)
        self.slurm += "#SBATCH --partition={}\n".format(self.fila)
        self.slurm += "#SBATCH --time={}\n".format(self.time)
        self.slurm += "#SBATCH --nodes={}\n".format(self.nodes)
        self.slurm += "#SBATCH --ntasks={}\n".format(self.task)
        self.slurm += "#SBATCH --mem={:.0f}G\n".format(int(self.mem))

        if 'gpu' in self.fila:
            self.slurm += "#SBATCH --gres=gpu:1\n"

        # if self.email:
        #     self.slurm += "#SBATCH --mail-type=ALL\n"
        #     self.slurm += "#SBATCH --mail-user={}\n".format(self.adress)
        
    def slurmFooter(self, arq):
        if self.calculo == 'dice':            

            path = self.check_cache('dice')   

            if path == False:
                result = subprocess.run(['find', self.home_dir, '-type', 'f', '-name', 'diceplayer.py'], stdout=subprocess.PIPE)
                path = result.stdout.decode().strip()
                self.write_cache('dice = {}'.format(path))
            
            self.slurm += 'module load {}\n\n'.format(self.gaussian)
            self.slurm += 'python3 {}\n'.format(path)
            self.slurm += '\necho -e "\\n## Job finalizado em $(date +"%d-%m-%Y as %T")"'
       
        elif self.calculo == 'cvKing':
            
            path = self.check_cache('cvKing')

            if path == False:
                result = subprocess.run(['find', self.home_dir, '-type', 'f', '-name', 'ConvergKing.py'], stdout=subprocess.PIPE)
                path = result.stdout.decode().strip()
                self.write_cache('cvKing = {}'.format(path))            
            
            self.slurm += 'module load {}\n\n'.format(self.gaussian)
            self.slurm += 'python3 {}\n'.format(path)
            self.slurm += '\necho -e "\\n## Job finalizado em $(date +"%d-%m-%Y as %T")"'

        elif self.calculo == 'omega':
            
            path = self.check_cache('omega1')

            if path == False:
                result = subprocess.run(['find', self.home_dir, '-type', 'd', '-name', 'musical_fiesta'], stdout=subprocess.PIPE)
                path = result.stdout.decode().strip()+'/main.py'
                self.write_cache('omega1 = {}'.format(path))
            
            self.slurm += 'module load {}\n\n'.format(self.gaussian)
            self.slurm += 'export GAUSS_SCRDIR=/scratch/global\n\n'
            self.slurm += 'python3 {}\n'.format(path)
            self.slurm += '\necho -e "\\n## Job finalizado em $(date +"%d-%m-%Y as %T")"'
        
        elif self.calculo == 'omegaOrder':

            path = self.check_cache('omega2')

            if path == False:
                result = subprocess.run(['find', self.home_dir, '-type', 'd', '-name', 'musical_order'], stdout=subprocess.PIPE)
                path = result.stdout.decode().strip()+'/main.py'
                self.write_cache('omega2 = {}'.format(path))

            self.slurm += 'module load {}\n\n'.format(self.gaussian)
            self.slurm += 'export GAUSS_SCRDIR=/scratch/global\n\n'
            self.slurm += 'python3 {}\n'.format(path)
            self.slurm += '\necho -e "\\n## Job finalizado em $(date +"%d-%m-%Y as %T")"'

        elif self.calculo == 'cpmd':
            self.slurm += '\nmodule load openmpi/5.0.3-gcc-9.2.0-cci73za\n'
            self.slurm += 'module load cpmd/4.3-gcc-9.2.0-u2fwv5u\n\n'
            self.slurm += 'cd $SLURM_SUBMIT_DIR\n'
            self.slurm += 'PP=$SLURM_SUBMIT_DIR\n'
            self.slurm += '\nmpirun -np $SLURM_NTASKS cpmd.x {} $PP > {}\n'.format(arq, arq.replace('{}'.format(self.extension),'.log'))
            self.slurm += '\necho -e "\\n## Job finalizado em $(date +"%d-%m-%Y as %T")"'
    
        elif self.calculo == 'g16' or self.calculo == 'g09':
            if self.calculo == 'g16':
                self.slurm += '\nmodule load {}\n\n'.format(self.gaussian)
            else:
                self.slurm += '\nmodule load gaussian/09\n'
            self.slurm += 'export GAUSS_SCRDIR=/scratch/global\n\n'
            if self.infoInput == 'y':
                for i in arq:
                    self.slurm += '{} {}\n'.format(self.calculo.lower(),i)
            
            else:
                self.slurm += '{} {}\n'.format(self.calculo.lower(),arq)

            self.slurm += '\necho -e "\\n## Job finalizado em $(date +"%d-%m-%Y as %T")"'
            
        elif self.calculo == 'orca':
            self.checkOrca()
            pathOrca = self.check_cache('orca')

            if pathOrca == False:
                result = subprocess.run(['find', self.home_dir, '-type', 'f', '-name', 'orca'], stdout=subprocess.PIPE)
                pathOrca = result.stdout.decode().strip()
                self.write_cache('orca = {}'.format(pathOrca))
            
            self.slurm += '\nsource /home/phfmatias/miniconda3/bin/activate leedmol310\n'
            self.slurm += 'export PATH=/home/phfmatias/.conda/envs/leedmol310/bin:$PATH\n'
            self.slurm += 'export LD_LIBRARY_PATH=/home/phfmatias/.conda/envs/leedmol310/lib:$LD_LIBRARY_PATH\n'
            
            self.slurm += 'cd $SLURM_SUBMIT_DIR\n\n'

            if len(self.arquivos) >= 1:
                if self.infoInput == 'y':
                    for i in self.arquivos:                 
                        self.slurm += '{} {} > {}\n'.format(pathOrca,i, i.replace('{}'.format(self.extension),'.log'))
                else:
                    self.slurm += '{} {} > {}\n'.format(pathOrca,self.arquivos[0], self.arquivos[0].replace('{}'.format(self.extension),'.log'))
                
                self.slurm += '\necho -e "\\n## Job finalizado em $(date +"%d-%m-%Y as %T")"'
            
        elif self.calculo == 'lammps':
            self.slurm += 'cd $SLURM_SUBMIT_DIR\n'
            self.slurm += 'module load openmpi-4.1.5-gcc-9.2.0-vzqsive\n'
            self.slurm += 'module load lammps-20220623.3-gcc-12.2.0-2xuxyoo\n'          
            self.slurm += 'mpirun -n {} lmp -in {} -l {}.out'.format(self.task,arq,arq.split(self.extension)[0])
        
        elif self.calculo == 'psi4':
            self.checkPsi4()
            self.slurm += 'PATH=$PATH:/home/public/psi4/psi4conda/bin ; export PATH\n'
            self.slurm += 'source /home/public/psi4/psi4conda/etc/profile.d/conda.sh\n'
            self.slurm += 'conda activate\n'
            self.slurm += 'SCRATCH=/scratch/global\n'
            self.slurm += '        WRKDIR=$SCRATCH/$SLURM_JOB_ID\n'
            self.slurm += '        mkdir -p $WRKDIR\n'
            self.slurm += '        APAGA_SCRATCH=Y\n'
            self.slurm += '        cd $SLURM_SUBMIT_DIR\n'

            if self.infoInput == 'y':
                for i in arq:
                    irep = i.replace('{}'.format(self.extension),'.out')
                    self.slurm += 'psi4 -n $SLURM_TASKS_PER_NODE {} -o {}\n'.format(i, irep)
            else:                
                arqRep = arq.replace('{}'.format(self.extension),'.out')
                self.slurm += 'psi4 -n {} -o {}\n'.format(arq, arqRep)

            
            self.slurm += 'if [ x"$APAGA_SCRATCH" = x"Y" ]; then\n'
            self.slurm += '       rm -rf $WRKDIR\n'
        
        elif self.calculo == 'psi4_1.8.0':
            self.checkPsi4()
            self.slurm +="cd $SLURM_SUBMIT_DIR\n\n"
            self.slurm +="PATH=$PATH:$HOME/psi4-1.8.0/bin ; export PATH\n"
            self.slurm +="source $HOME/psi4-1.8.0/etc/profile.d/conda.sh\n"
            self.slurm +="conda activate\n"

            self.slurm += 'SCRATCH=/scratch/global\n'
            self.slurm += '        WRKDIR=$SCRATCH/$SLURM_JOB_ID\n'
            self.slurm += '        mkdir -p $WRKDIR\n'
            self.slurm += '        APAGA_SCRATCH=Y\n\n\n'

            if self.infoInput == 'y':
                for i in arq:
                    irep = i.replace('{}'.format(self.extension),'.out')
                    self.slurm += 'psi4 -i {} -o {} -n $SLURM_TASKS_PER_NODE\n'.format(i, irep)
            else:
                arqRep = arq.replace('{}'.format(self.extension),'.out')
                self.slurm += 'psi4 -i {} -o {} -n $SLURM_TASKS_PER_NODE\n'.format(arq, arqRep)
            
            self.slurm += '\n\nif [ x"$APAGA_SCRATCH" = x"Y" ]; then\n'
            self.slurm += '       rm -rf $WRKDIR\n'
    
    def divideSlurms(self, num_arq, num_slurms):

        if num_slurms <= 0:
            raise ValueError("O número de slurms deve ser maior que zero.")
        if num_arq <= 0:
            raise ValueError("O número de arquivos deve ser maior que zero.")

        arquivos_por_slurm = num_arq // num_slurms
        restante = num_arq % num_slurms

        if arquivos_por_slurm < 1:
            raise ValueError("O número de arquivos por slurm deve ser maior que zero. Diminua o número de slurms ou aumente o número de arquivos.")

        distribuicao = []

        for i in range(num_slurms):
            slurm_list = []
            
            if i == num_slurms - 1:
                arquivos_por_slurm += restante
                for j in range(arquivos_por_slurm):
                    slurm_list.append(self.arquivos.pop(0))
                distribuicao.append(slurm_list)
        
            else:
                for j in range(arquivos_por_slurm):
                    slurm_list.append(self.arquivos.pop(0))
                distribuicao.append(slurm_list)
        
        return distribuicao


    def slurmWriter(self): 

        if self.calculo == 'g16' or self.calculo == 'g09':
            self.checkGaussian() 

        if self.infoInput == 'y':
            if self.numSlurms > 1:
                list_files = self.divideSlurms(len(self.arquivos), self.numSlurms)

                for i in range(self.numSlurms):
                    self.slurmHeader()
                    self.slurmFooter(list_files[i])
                    name = self.name+str(i+1)
                    self.slurm = self.slurm.replace('#SBATCH --job-name={}\n'.format(self.name), '#SBATCH --job-name={}\n'.format(name))
                    slurmArq = open(name+'.slurm','w')
                    slurmArq.write(self.slurm)
                    slurmArq.close()
                    self.slurm = ''

            else:
                self.slurmHeader()
                self.slurmFooter(self.arquivos)
                self.slurm = self.slurm.replace('#SBATCH --job-name=\n', '#SBATCH --job-name={}\n'.format(self.name))
                slurmArq = open(self.name+'.slurm','w')
                slurmArq.write(self.slurm)
                slurmArq.close()

        elif self.infoInput == 'n':   
            if len(self.arquivos) > 1:
                for input in self.arquivos:
                    self.slurmHeader()
                    self.slurmFooter(input)
                    self.name = input.replace('{}'.format(self.extension),'')
                    self.slurm = self.slurm.replace('#SBATCH --job-name=\n', '#SBATCH --job-name={}\n'.format(self.name))
                    slurmArq = open(self.name+'.slurm','w')
                    slurmArq.write(self.slurm)
                    slurmArq.close()
                    self.slurm = ''
                    self.name = ''
            
            else:
                input = self.arquivos[0]
                self.slurmHeader()
                self.slurmFooter(input)
                self.name = input.replace('{}'.format(self.extension),'')   
                self.slurm = self.slurm.replace('#SBATCH --job-name=\n', '#SBATCH --job-name={}\n'.format(self.name))
                slurmArq = open(self.name+'.slurm','w')
                slurmArq.write(self.slurm)
                slurmArq.close()
                self.slurm = ''    

if __name__ == "__main__":
    ms = makeslurm()
    ms.getInfos()
    ms.slurmWriter()
    ms.changeInput()
