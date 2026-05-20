##   PYTHON FILE HEADER #
##
##   File:         [log2xyz.py]
##
##   Author(s):    ['Pedro H.F Matias']
##   Site(s):      ['https://github.com/phfmatias']
##   Email(s):     ['phfmatias@discente.ufg.br']
##   Credits:      ['Copyright © 2026 LEEDMOL. All rights reserved.']
##   Date:         ['12.05.2026']
##   Version:      ['0.0.1']
##   Status:       ['Development']
##   Language:     ['Python']
##   Description:  ['Python script that will generate a xyz from a log file']
##   Usage:		   ['python3 log2xyz <logfile>

from  sys import argv
from MoleKing import G16LOGfile

if __name__ == "__main__":

    if len(argv) != 2 and len(argv) != 3:
        print("Usage: python3 log2xyz <logfile> [xyzfile]")
        exit(1)

    if len(argv) == 2:
        log_file = argv[1]
        fileName = log_file.split(".")[0]+".xyz"

    if len(argv) == 3:
        fileName = argv[2]
        log_file = argv[1]

    print('XYZ name will be the same as the log file, but with .xyz extension. If want another name next time run:')
    print('python3 log2xyz <logfile> <xyzfile>')
    g16_log = G16LOGfile(log_file).getMolecule()
    g16_log.toXYZ(fileName=fileName)