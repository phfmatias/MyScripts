from os import listdir

ref_file = [x for x in listdir() if '.chk' in x][0]


name = ref_file.split('_')[-1]
newName = ref_file.replace(name, 'NFB3LYPSTO.gjf')

arq = open(newName, 'w')

mystr = ('''%oldchk={}
%chk={}
%mem=16GB
%nprocshared=8
# opt=(calcfc,ts,noeigentest,maxcycle=100000) freq=noraman b3lyp/STO-6g scf=(qc,novaracc,maxcycle=10000,noincfock) test geom=AllCheck Guess=Read

Refinação TS B3LYP

0 2    


'''.format(ref_file, newName.replace('.gjf','.chk')))

print(mystr)

arq.write(mystr)
arq.close()