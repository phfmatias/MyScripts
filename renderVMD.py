##   PYTHON FILE HEADER #
##
##   File:         [renderVMD.py]
##
##   Author(s):    ['Pedro H.F Matias']
##   Credits:      ['Copyright © 2024 LEEDMOL. All rights reserved.']
##   Date:         ['05.04.2024']
##   Version:      ['0.0.1']
##   Status:       ['Development']
##   Language:     ['Python']
##   Description:  ['Python Script to Render VMD images']
##   Usage:        ['python3 renderVMD.py wait=False <input_file>']

from sys import argv
try:
    from MoleKing import PeriodicTable, G16LOGfile, Molecule
except ImportError:
    print("MoleKing is not installed. Please, run: pip3 install MoleKing")
    exit()

import os

if len(argv) != 3:
    print("Usage: python3 renderVMD.py wait=False <input_file>")
    print("wait=False: Do not wait for the VMD window to close")
    print("wait=True: Wait for the VMD window to close, so you can rotate the molecule")
    exit()

class Render():
    def __init__(self, input_file):
        self.input_file = input_file
        self.elements = {}
        self.toRemove = ''
        self. colorsVMD = [x for x in range(32)]

        self.name = self.input_file.split('.')[0]
            
        self.checkWait()
        self.checkTachyon()
        self.check_file()
        self.doRender()

    def checkWait(self):
        if 'wait=False' in argv:
            self.wait = False
        else:
            self.wait = True
    
    def HEX2RGB(self, hex):
        rgb = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
        normalized_rgb = [val / 255 for val in rgb]
        normalized_rgb = [round(val, 6) for val in normalized_rgb]
        return normalized_rgb
        

    def checkTachyon(self):
        # Check if the Tachyon executable is present in the PATH
        if any(os.access(os.path.join(path, 'tachyon'), os.X_OK) for path in os.environ["PATH"].split(os.pathsep)):
            pass
        else:
            print("Tachyon is not installed. Please, run: sudo apt install tachyon -y")
            exit()

    def check_file(self):
        if self.input_file.split('.')[-1] not in ['gjf', 'xyz', 'log']:
            print("Invalid file format. Please provide a valid file format: gjf, xyz or log")
            exit()

        elif self.input_file.split('.')[-1] == 'xyz':
            self.doXYZ()

        if self.input_file.split('.')[-1] == 'gjf':
            self.doGJF()

        elif self.input_file.split('.')[-1] == 'log':
            self.doLOG()

    def doGJF(self):
        mol = Molecule()
        arq = open(self.input_file, 'r').readlines()

        for line in arq:
            try:
                element = line.split()[0]
                x = float(line.split()[1])
                y = float(line.split()[2])
                z = float(line.split()[3])
                mol.addAtom(element, x, y, z)
            except:
                pass
        
        if len(mol) == 0:
            print("No atoms found in the file.")
            exit()

        else:
            mol.toXYZ(fileName='temp.xyz')
            self.input_file = 'temp.xyz'
            self.doXYZ()

    def doLOG(self):
        x = G16LOGfile(self.input_file).getMolecule().toXYZ(fileName='temp.xyz')
        self.input_file = 'temp.xyz'
        self.doXYZ()

    def doXYZ(self):
        arq = open(self.input_file, 'r').readlines()[2:]

        el_list = []

        for line in arq:
            if line == '\n':
                break
            element = line.split()[0]
            if element not in el_list:
                el_list.append(element)
        
        for i in el_list:
            if i == 'Cl':
                print(i, PeriodicTable().getColor(i), self.HEX2RGB(PeriodicTable().getColor(i)))
            self.elements[i] = self.HEX2RGB(PeriodicTable().getColor(i))

    def doTCL(self):
        arq = open('render.tcl', 'w')
        arq.write('mol representation {CPK 1.0 0.3 50.0 30.0}\n')
        arq.write('mol addrep top\n')
        arq.write('mol modcolor 1 0 Element\n')
        c = 0
        for key, value in self.elements.items():
            arq.write('color Element {} {}\n'.format(key, self.colorsVMD[c]))
            arq.write('color change rgb {} {:.6f} {:.6f} {:.6f}\n'.format(c, value[0], value[1], value[2]))
            c+=1
        arq.write('material change mirror Opaque 0.15\n')
        arq.write('material change outline Opaque 4.000000\n')
        arq.write('material change outlinewidth Opaque 0.5\n')
        arq.write('material change ambient Glossy 0.1\n')
        arq.write('material change diffuse Glossy 0.600000\n')
        arq.write('material change opacity Glossy 0.75\n')
        arq.write('material change ambient Opaque 0.08\n')
        arq.write('material change mirror Opaque 0.0\n')
        arq.write('material change shininess Glossy 1.0\n')
        arq.write('display distance -7.0\n')
        arq.write('display height 10\n')
        arq.write('light 3 on\n')
        arq.write('display depthcue off\n')
        arq.write('color Display Background white\n')
        arq.write('axes location off\n')
        arq.write('display update\n')
        if not self.wait:
            arq.write('render Tachyon vmdscene.dat\n')
            arq.write('exit')
    
    def doRender(self):
        self.doTCL()
        
        if self.wait:
            print('Please, when you are done type this in the vmd terminal:')
            print('render Tachyon vmdscene.dat')
            print('exit')
            input('Press Enter to continue to open VMD')

        os.system('vmd {} -e render.tcl'.format(self.input_file))
        os.system('tachyon vmdscene.dat -format PNG -o {}.png -res 2000 1500 -aasamples 24'.format(self.name))

        self.toRemove = 'render.tcl vmdscene.dat'
        os.system('rm {}'.format(self.toRemove))
    
        if 'temp.xyz' in os.listdir():
            os.system('rm temp.xyz')


if __name__ == '__main__':
    Render(argv[-1])