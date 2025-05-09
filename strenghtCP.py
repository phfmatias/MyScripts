from os import getcwd
from sys import argv
from pandas import DataFrame

class QTAIM_Analysis:
    def __init__(self):
        self.cp = [int(i) for i in argv[1:]]
        self.get_data()
        print(self.df.to_markdown(index=False))

    def get_data(self):

        arq = open('CPprop.txt', 'r').readlines()

        temp = {}
        results = {}
        DF_TEMP = DataFrame()

        count = 0
        for i in range(len(arq)):
            if 'CP' in arq[i]:
                start = i
                end = i+54

                cp = int(arq[i].split()[2].split(',')[0])

                my_string = ''

                for j in range(start, end):
                    my_string += arq[j]

                temp[cp] = my_string

        for j in self.cp:
            for i in temp[j].split('\n'):
                if 'Density of all electrons:' in i:
                    rho = float(i.split()[-1])
                    #
                    #be_charged = ((-223.08*rho)+0.7423)*4.184  #neutral
                    be_charged = ((-333.24*rho)-1.0661)*4.184   #charged H-Bond

                    # −11.0 to −15.0 kcal/mo strenght = medium http://sobereva.com/attach/513/Tian_Lu_JCC_2019.pdf
                    # < −15.0 kcal/mol strenght = strong

                    if be_charged < -15.0:
                        strength = 'Strong'
                    elif be_charged >= -15.0 and be_charged <= -11.0:
                        strength = 'Medium'
                    else:
                        strength = 'Weak'
                    
                if 'Hamiltonian kinetic energy K(r):' in i:
                    kr = float(i.split()[-1])

                if 'Laplacian of electron density:' in i:
                    lap = float(i.split()[-1])
                    
                if 'Electron localization function (ELF):' in i:
                    elf = float(i.split()[-1])

                if 'Localized orbital locator (LOL)' in i:
                    lol = float(i.split()[-1])

                if 'Energy density E(r) or H(r):' in i:
                    er_hr = float(i.split()[-1])
                
                if 'Type' in i:
                    type = i.split()[4]

                if 'Connected atoms' in i:
                    A1 = i.split()[2].split('(')[1]+'_'+i.split()[2].split('(')[0]
                    A2 = i.split()[-2].split('(')[1]+'_'+i.split()[-2].split('(')[0]
                    
                    A = A1 + '-' + A2

            if lap > 0 and er_hr > 0:
                aim_strenght = 'Weak'
            elif lap > 0 and er_hr < 0:
                aim_strenght = 'Moderate'
            elif lap < 0 and er_hr < 0:
                aim_strenght = 'Strong'

            results = {'CP':j, 'A1-A2':A, 'Strength':strength, 'Type':type, 'K(r)':kr, 'Lap':lap, 'ELF':elf, 'LOL':lol, 'E(r)':er_hr, 'Strength (QTAIM)':aim_strenght}
            DF_TEMP = DF_TEMP._append(results, ignore_index=True)
        self.df = DF_TEMP


if __name__ == '__main__':
    qt = QTAIM_Analysis()