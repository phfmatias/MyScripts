##   PYTHON FILE HEADER #
##
##   File:         [extractFrames.py]
##
##   Author(s):    ['Pedro H.F Matias']
##   Site(s):      ['https://github.com/phfmatias']
##   Email(s):     ['phfmatias@discente.ufg.br']
##   Credits:      ['Copyright © 2025 LEEDMOL. All rights reserved.']
##   Date:         ['05.11.2025']
##   Version:      ['0.0.1']
##   Status:       ['Development']
##   Language:     ['Python']
##   Description:  ['Extract frames from a molecular dynamics to be used in gaussian']
##   Usage:		   ['python extractFrames.py']

from os import system
from subprocess import check_output
from time import sleep

class ExtractFrames:
    def __init__(self):
        self.path = '/home/carolfelisberto/DOUTORADO/GROMACS/REMEDIO/CIP_IBU/GROMACS_BOX/CIP_1_IBU_1/Hbond/O4_CIP/O4_CIP_H33_IBU_HPC.xvg'
        self.target1 = 'O4'
        self.target2 = 'CIP'
        self.target3 = 'H33'
        self.target4 = 'IBU'

        self.get_info_from_user()
        self.find_max_hbond_frames(self.path)
        self.create_pdb_from_frame(self.best_frame)
        self.create_indices_file()
        self.get_residues()
        self.create_indices_hbond_file()
        self.create_pdbs()

    def get_info_from_user(self):
        self.path = input("Enter the path to the .xvg file: ")
        self.target1 = input("Enter with the first target group name (e.g., O2): ")
        self.target2 = input("Enter with the second target group name (e.g., the molecule name from target1 like CIP): ")
        self.target3 = input("Enter with the third target group name (e.g., H33): ")
        self.target4 = input("Enter with the fourth target group name (e.g., the molecule name from target3 like IBU): ")

        print('\n')
        print('So, we gonna analyze the H-bonds between {} from {} , and {} from {}.'.format(self.target1, self.target2, self.target3, self.target4))
        sleep(2)

    def find_max_hbond_frames(self, xvg_filename):
        max_hbond = -1
        best_frame = -1

        arq = open(xvg_filename, 'r')
        lines = arq.readlines()

        for line in lines:
            if line.startswith(('#', '@')):
                continue  
            parts = line.split()
            if len(parts) < 2:
                continue  
            frame = int(float(parts[0]))
            hbond_count = int(float(parts[1]))

            if hbond_count > max_hbond:
                max_hbond = hbond_count
                best_frame = frame

        arq.close()

        self.best_frame = best_frame
        self.max_hbond = max_hbond

        print(f"Maximum number of H-bonds: {max_hbond} at frame {best_frame}")
        sleep(2)

    def create_pdb_from_frame(self, frame_number):
        print(f"Creating PDB file for frame {frame_number}...")
        command = f"echo 0 | gmx_mpi trjconv -s ../md.tpr -f ../md.xtc -o frame_{frame_number}.pdb -dump {frame_number} -pbc mol -ur compact > /dev/null 2>&1"
        system(command)

    def create_indices_file(self):
        print("Creating index file for H-bond analysis...")

        command = f"echo 0 0 | gmx_mpi hbond-legacy -f frame_{self.best_frame}.pdb -s ../md.tpr -n ../index.ndx -hbn hbond_atoms.ndx > /dev/null 2>&1"
        arq = open('../index.ndx', 'r').readlines()
        groups = [line.split()[1] for line in arq if line.startswith('[')]

        ind1 = [x for x in range(len(groups)) if '{}'.format(self.target1) in groups[x] and '{}'.format(self.target2) in groups[x]][0]
        ind2 = [x for x in range(len(groups)) if '{}'.format(self.target3) in groups[x] and '{}'.format(self.target4) in groups[x]][0]

        command = f"echo {ind1} {ind2} | gmx_mpi hbond-legacy -f frame_{self.best_frame}.pdb -s ../md.tpr -n ../index.ndx -hbn hbond_atoms.ndx > /dev/null 2>&1"
        system(command)

    def get_residues(self):
        print("Getting residue information for H-bonded atoms...")

        dict_atoms = {}

        arq = open('hbond_atoms.ndx', 'r').readlines()
        start, end = -1, len(arq)
        for i in range(len(arq)):
            if arq[i].startswith('[ hbonds_'):
                start = i + 1
                break
        
        c = 1

        for j in range(start, len(arq)):
            dict_atoms['hbond_{}'.format(c)] = arq[j].strip().split()[0] + ' ' + arq[j].strip().split()[2]
            c += 1
        
        dict_residues = {} 

        for key, value in dict_atoms.items():
            atom1 = value.split()[0]
            atom2 = value.split()[1]

            command1 = f'grep "ATOM  {atom1:>5}" frame_{self.best_frame}.pdb'
            command2 = f'grep "ATOM  {atom2:>5}" frame_{self.best_frame}.pdb'

            atom1_info = check_output(command1, shell=True, text=True)[22:26].strip()
            atom2_info = check_output(command2, shell=True, text=True)[22:26].strip()

            dict_residues[key] = atom1_info + ' ' + atom2_info

        self.dict_residues = dict_residues

    def create_indices_hbond_file(self):
        print("Creating index file for H-bonded residues...")

        commands = []
        c = 7
        for key, value in self.dict_residues.items():
            commands.append('r {} & 3'.format(value.split()[0]))
            commands.append('r {} & 2'.format(value.split()[1]))
            commands.append('{} | {}'.format(c, c+1))   
            c += 3
        
        commands.append(' q')
        command = 'echo "{}" | gmx_mpi make_ndx -f frame_{}.pdb -o par1.ndx > /dev/null 2>&1'.format('\n'.join(commands), self.best_frame)
        system(command)

    def create_pdbs(self):
        print("Creating PDB files for each H-bonded residue pair...")

        pdb_lines = []
        arq = open('par1.ndx', 'r').readlines()

        for line in arq:
            if line.startswith('['):
                pdb_lines.append(line)

        indices = {}

        c = 1
        for i in range(len(pdb_lines)):
            if len(pdb_lines[i].split('_')) == 8:
                indices['hbond_{}'.format(c)] = i
                c += 1

        for key, value in indices.items(): 
            command = f"echo {value-1} {value} | gmx_mpi trjconv -s ../md.tpr -f frame_{self.best_frame}.pdb -o {key}.pdb -n par1.ndx -center -pbc mol -ur compact > /dev/null 2>&1"
            command2 = f"obabel {key}.pdb -O {key}.gjf > /dev/null 2>&1"
            system(command)      
            system(command2)

if __name__ == "__main__":
    extractor = ExtractFrames()



