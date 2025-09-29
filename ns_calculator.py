##   PYTHON FILE HEADER #
##
##   File:         [ns_calculator.py]
##
##   Author(s):    ['Pedro H.F Matias']
##   Site(s):      ['https://github.com/phfmatias']
##   Email(s):     ['phfmatias@discente.ufg.br']
##   Credits:      ['Copyright © 2025 LEEDMOL. All rights reserved.']
##   Date:         ['03.09.2025']
##   Version:      ['0.0.1']
##   Status:       ['Development']
##   Language:     ['Python']
##   Description:  ['Script to calculate the nsteps from dt and target']
##   Usage:		   ['python3 ns_calculator.py <dt> <target>']


from sys import argv

dt = argv[1]
target = argv[2]

#target always be in nanoseconds

nsteps = int((float(target) * 1000) / float(dt))

print('To achieve {} ns with {} dt, nsteps should be: {}'.format(target, dt, nsteps))