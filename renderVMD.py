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
from pyperclip import copy
try:
    from MoleKing import PeriodicTable, G16LOGfile, Molecule
except ImportError:
    print("MoleKing is not installed. Please, run: pip3 install MoleKing")
    exit()

import os


if len(argv) < 3:
    print("Usage: python3 renderVMD.py wait=False <input_file>")
    print("                       OR                          ")
    print("wait=False: Do not wait for the VMD window to close")

if '.cub' in argv[2] and len(argv) < 4:
    print("Usage: python3 renderVMD.py wait=False <cube_file> <isovalue> fukui/orb")
    print("wait=True: Wait for the VMD window to close, so you can rotate the molecule")
    exit()

class Render():
    def __init__(self, input_file):
        self.input_file = input_file
        self.elements = {}
        self.toRemove = ''
        self.colorsVMD = [x for x in range(32)]

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
        if self.input_file.split('.')[-1] not in ['gjf', 'xyz', 'log', 'cub']:
            print("Invalid file format. Please provide a valid file format: gjf, xyz or log")
            exit()

        if self.input_file.split('.')[-1] == 'xyz':
            self.doXYZ()
            self.ipt = 'xyz'

        if self.input_file.split('.')[-1] == 'gjf':
            self.doGJF()
            self.ipt = 'gjf'

        if self.input_file.split('.')[-1] == 'log':
            self.doLOG()
            self.ipt = 'log'

        if self.input_file.split('.')[-1] == 'cub':
            self.doCUB()
            self.ipt = 'cub'

        
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

    
    def doCUB(self):
        self.AtomsCub = []
        arq = open(self.input_file, 'r').readlines()
        for i in range(len(arq)):
            if len(arq[i].split()) == 5:
                try:

                    if int(arq[i].split()[0]) < 0:
                        pass

                    else:
                        print(arq[i])
                        int(arq[i].split()[0])
                        float(arq[i].split()[1])
                        float(arq[i].split()[2])
                        float(arq[i].split()[3])
                        float(arq[i].split()[4])
                        self.AtomsCub.append(arq[i].split()[0])
                except:
                    pass

        self.AtomsCub = list(set(self.AtomsCub))
        
        for i in self.AtomsCub:
            atomCub = PeriodicTable().getSymbol(int(i))
            if atomCub == 'I':
                self.elements[atomCub] = self.HEX2RGB(PeriodicTable().getColor('Pd'))
            elif atomCub == 'Y':
                self.elements[atomCub] = self.HEX2RGB(PeriodicTable().getColor('Br'))
            elif atomCub == 'F':
                self.elements[atomCub] = [0.576, 1, 0.925]
            else:
                self.elements[atomCub] = self.HEX2RGB(PeriodicTable().getColor(atomCub))

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
            if i == 'I':
                self.elements[i] = self.HEX2RGB(PeriodicTable().getColor('Pd'))
            elif i == 'Y':
                print(PeriodicTable().getColor('Br'))
                self.elements[i] = self.HEX2RGB(PeriodicTable().getColor('Br'))
            elif i == 'F':
                self.elements[i] = [0.576, 1, 0.925]
            else:
                print(i)
                self.elements[i] = self.HEX2RGB(PeriodicTable().getColor(i))

    def doTCL(self, ipt):

        if ipt in ['gjf', 'log', 'xyz']:
            arq = open('render.tcl', 'w')
            arq.write('mol representation {CPK 1.0 0.3 50.0 30.0}\n')
            arq.write('mol addrep top\n')
            arq.write('mol modcolor 1 0 Element\n')
            c = 0
            for key, value in self.elements.items():
                if c == 8:
                    c+=1
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
            arq.write('axes location off\n')
            arq.write('display update\n')
            arq.write('color Display Background white\n')
            if argv[-1] == 'qtaim':
                arq.write('color Display Background white\n')
                arq.write('axes location Off\n')
                arq.write('display depthcue off\n')
                arq.write('display rendermode GLSL\n')
                arq.write('set CPsize 0.07\n')
                arq.write('set pathsize 0.02\n')
                arq.write('mol new CPs.pdb\n')
                arq.write('mol modselect 0 1 name C\n')
                arq.write('mol modstyle 0 1 VDW $CPsize 22.0\n')
                arq.write('mol modcolor 0 1 ColorID 11\n')
                arq.write('mol addrep 1\n')
                arq.write('mol modselect 1 1 name N\n')
                arq.write('mol modstyle 1 1 VDW $CPsize 22.0\n')
                arq.write('mol modcolor 1 1 ColorID 3\n')
                arq.write('mol addrep 1\n')
                arq.write('mol modselect 2 1 name O\n')
                arq.write('mol modstyle 2 1 VDW $CPsize 22.0\n')
                arq.write('mol modcolor 2 1 ColorID 4\n')
                arq.write('mol addrep 1\n')
                arq.write('mol modselect 3 1 name F\n')
                arq.write('mol modstyle 3 1 VDW $CPsize 22.0\n')
                arq.write('mol modcolor 3 1 ColorID 7\n')
                arq.write('mol new paths.pdb\n')
                arq.write('mol modstyle 0 2 VDW $pathsize 22.0\n')
                arq.write('mol modcolor 0 2 ColorID 32\n')
                arq.write('color change rgb 17 1.000000 1.000000 0.000000\n')
                arq.write('color Display Background white\n')
                arq.write('proc labcp {cptype {labsize 1.8} {offsetx -0.1} {offsety 0.0}} {\n')
                arq.write('label delete Atoms all\n')
                arq.write('if {$cptype=="no"} {return}\n')
                arq.write('color Labels Atoms blue\n')
                arq.write('label textthickness 2.000000\n')
                arq.write('label textsize $labsize\n')
                arq.write('set atmsel all\n')
                arq.write('if {$cptype=="3n3"} {set atmsel "name C"}\n')
                arq.write('if {$cptype=="3n1"} {set atmsel "name N"}\n')
                arq.write('if {$cptype=="3p1"} {set atmsel "name O"}\n')
                arq.write('if {$cptype=="3p3"} {set atmsel "name F"}\n')
                arq.write('set sel [atomselect 0 $atmsel]\n')
                arq.write('set k 0\n')
                arq.write('foreach i [$sel list] {\n')
                arq.write('label add Atoms 0/$i\n')
                arq.write('label textformat Atoms $k { %1i }\n')
                arq.write('label textoffset Atoms $k "$offsetx $offsety"\n')
                arq.write('incr k\n')
                arq.write('}\n')
                arq.write('$sel delete\n')
                arq.write('}\n')
                arq.write('\n')
                arq.write('proc labcpidx {cpidx {labsize 1.8} {offsetx -0.1} {offsety 0.0}} {\n')
                arq.write('label delete Atoms all\n')
                arq.write('color Labels Atoms blue\n')
                arq.write('label textthickness 2.000000\n')
                arq.write('label textsize $labsize\n')
                arq.write('set sel [atomselect 0 "serial $cpidx"]\n')
                arq.write('set k 0\n')
                arq.write('foreach i [$sel list] {\n')
                arq.write('label add Atoms 0/$i\n')
                arq.write('label textformat Atoms $k { %1i }\n')
                arq.write('label textoffset Atoms $k "$offsetx $offsety"\n')
                arq.write('incr k\n')
                arq.write('}\n')
                arq.write('$sel delete\n')
                arq.write('}\n')
            if not self.wait:
                arq.write('render Tachyon vmdscene.dat\n')
                arq.write('exit')

        if ipt == 'cub':
            arq = open('showcub.vmd','w')
            arq.write('proc cub {filename {isoval 0.05}} {\n')
            arq.write('set mater Glossy\n')
            arq.write('color Display Background {}\n'.format(self.colorsVMD[-2]))
            arq.write('color change rgb {} 1.000000 1.000000 1.000000\n'.format(len(self.colorsVMD) -2))
            arq.write('display depthcue off\n')
            arq.write('display rendermode GLSL\n')
            arq.write('axes location Off\n')
            c = 0
            for key, value in self.elements.items():
                if len(key) == 2:
                    if key == 'Cl':
                        pass
                    else:
                        arq.write('color Name {} {}\n'.format(key[0], self.colorsVMD[c]))
                else:
                    arq.write('color Name {} {}\n'.format(key, self.colorsVMD[c]))
                arq.write('color change rgb {} {:.6f} {:.6f} {:.6f}\n'.format(c, value[0], value[1], value[2]))
                c+=1
            arq.write('material change mirror Opaque 0.15\n')
            arq.write('material change outline Opaque 4.000000\n')
            arq.write('material change outlinewidth Opaque 0.5\n')
            arq.write('material change ambient Glossy 0.1\n')
            arq.write('material change diffuse Glossy 0.600000\n')
            arq.write('material change opacity Glossy 0.75\n')
            arq.write('material change shininess Glossy 1.0\n')
            arq.write('light 3 on\n')
            arq.write('foreach i [molinfo list] {\n')
            arq.write('mol delete $i\n')
            arq.write('}\n')
            arq.write('mol new $filename.cub\n')
            arq.write('mol modstyle 0 top CPK 0.800000 0.300000 600.000000 600.000000\n') #LIGAÇÃO
            arq.write('mol addrep top\n')
            arq.write('mol modstyle 1 top Isosurface $isoval 0 0 0 1 1\n')
            if argv[-1].lower() == 'fukui':
                arq.write('color change rgb {} 0.000000 0.000000 1.00000 \n'.format(len(self.colorsVMD))) #AZUL POSITIVO
                arq.write('color change rgb {} 1.000000 1.000000 0.000000 \n'.format(len(self.colorsVMD) -1))  #AMARELO NEGATIVO
            if argv[-1].lower() == 'orb':
                arq.write('color change rgb {} 0.000000 0.000000 1.00000 \n'.format(len(self.colorsVMD))) #AZUL POSITIVO
                arq.write('color change rgb {} 1.000000 0.000000 0.000000 \n'.format(len(self.colorsVMD) -1))  #AMARELO NEGATIVO       
            if argv[-1].lower() == 'spin':
                arq.write('color change rgb {} 0.000000 0.000000 1.00000 \n'.format(len(self.colorsVMD))) #AZUL
                arq.write('color change rgb {} 0.000000 0.000000 1.000000 \n'.format(len(self.colorsVMD) -1)) #AZUL    
            arq.write('mol modcolor 1 top ColorID {}\n'.format(len(self.colorsVMD)))         
            arq.write('mol modmaterial 1 top $mater\n')
            arq.write('mol addrep top\n')
            arq.write('mol modstyle 2 top Isosurface -$isoval 0 0 0 1 1\n')
            arq.write('mol modcolor 2 top ColorID {}\n'.format(len(self.colorsVMD) -1))   
            arq.write('mol modmaterial 2 top $mater\n')
            arq.write('display distance -8.0\n')
            arq.write('display height 10\n')
            arq.write('}\n')
            arq.write('proc cubiso {isoval} {\n')
            arq.write('mol modstyle 1 top Isosurface $isoval 0 0 0 1 1\n')
            arq.write('mol modstyle 2 top Isosurface -$isoval 0 0 0 1 1\n')
            arq.write('}\n')
            arq.write('proc cub2 {filename1 filename2 {isoval 0.05}} {\n')
            arq.write('set mater Glossy\n')
            arq.write('display depthcue off\n')
            arq.write('display rendermode GLSL\n')
            arq.write('axes location Off\n')
            c = 0
            for key, value in self.elements.items():
                arq.write('color Name {} {}\n'.format(key, self.colorsVMD[c]))
                arq.write('color change rgb {} {:.6f} {:.6f} {:.6f}\n'.format(c, value[0], value[1], value[2]))
                c+=1
            arq.write('material change mirror Opaque 0.15\n')
            arq.write('material change outline Opaque 4.000000\n')
            arq.write('material change outlinewidth Opaque 0.5\n')
            arq.write('material change ambient Glossy 0.1\n')
            arq.write('material change diffuse Glossy 0.600000\n')
            arq.write('material change opacity Glossy 0.75\n')
            arq.write('material change shininess Glossy 1.0\n')
            arq.write('light 3 on\n')
            arq.write('foreach i [molinfo list] {\n')
            arq.write('mol delete $i\n')
            arq.write('}\n')
            arq.write('mol new $filename1.cub\n')
            arq.write('mol modstyle 0 top CPK 0.800000 0.300000 22.000000 22.000000\n')
            arq.write('mol addrep top\n')
            arq.write('mol modstyle 1 top Isosurface $isoval 0 0 0 1 1\n')
            arq.write('mol modcolor 1 top ColorID 12\n')
            arq.write('mol modmaterial 1 top $mater\n')
            arq.write('mol new $filename2.cub\n')
            arq.write('mol modstyle 0 top CPK 0.800000 0.300000 22.000000 22.000000\n')
            arq.write('mol addrep top\n')
            arq.write('mol modstyle 1 top Isosurface $isoval 0 0 0 1 1\n')
            arq.write('mol modcolor 1 top ColorID 22\n')
            arq.write('mol modmaterial 1 top $mater\n')
            arq.write('display distance -8.0\n')
            arq.write('display height 10\n')
            arq.write('}\n')
            arq.write('proc cub2iso {isoval} {\n')
            arq.write('foreach i [molinfo list] {\n')
            arq.write('mol modstyle 1 $i Isosurface $isoval 0 0 0 1 1\n')
            arq.write('}\n')
            arq.write('}\n')
            arq.write('cub {} {}\n'.format(self.input_file.split('.')[0], argv[3]))
            if not self.wait:
                arq.write('render Tachyon vmdscene.dat\n')
                arq.write('exit')
    
    def doRender(self):
        self.doTCL(self.ipt)
        
        if self.ipt in ['gjf', 'log', 'xyz']:
            if self.wait:
                print('Please, when you are done, just paste in the VMD terminal. The code was already copied to the clipboard.')
                print('exit')
                input('Press Enter to continue to open VMD')
                x = copy('render Tachyon vmdscene.dat')
                os.system('vmd {} -e render.tcl'.format(self.input_file))
                os.system('tachyon vmdscene.dat -format PNG -o {}.png -res 2000 1500 -aasamples 24'.format(self.name))
                #os.system('rm render.tcl')

            else:
                print('Rendering...')
                os.system('vmd {} -e render.tcl'.format(self.input_file))
                os.system('tachyon vmdscene.dat -format PNG -o {}.png -res 2000 1500 -aasamples 24'.format(self.name))
                self.toRemove = 'render.tcl vmdscene.dat'
                #os.system('rm {}'.format(self.toRemove))
        
            if 'temp.xyz' in os.listdir():
                pass
                #os.system('rm temp.xyz')

        else:
            if self.wait:
                print('Please, when you are done, just paste in the VMD terminal. The code was already copied to the clipboard.')
                print('exit')
                input('Press Enter to continue to open VMD')
                x = copy('render Tachyon vmdscene.dat')
                os.system('vmd {} -e showcub.vmd'.format(self.input_file))
                os.system('tachyon vmdscene.dat -format PNG -o {}.png -res 2000 1500 -aasamples 24'.format(self.name))
                #os.system('rm vmdscene.dat')
                #os.system('rm showcub.vmd')
            else:
                print('Rendering...')
                os.system('vmd {} -e showcub.vmd'.format(self.input_file.split('.')[0]))
                os.system('tachyon vmdscene.dat -format PNG -o {}.png -res 2000 1500 -aasamples 24'.format(self.name))
                
                #self.toRemove = 'showcub.vmd vmdscene.dat'
                #os.system('rm {}'.format(self.toRemove))
            
            if 'temp.xyz' in os.listdir():
                pass
                #os.system('rm temp.xyz')


if __name__ == '__main__':
    Render(argv[2])