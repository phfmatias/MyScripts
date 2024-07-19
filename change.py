##   PYTHON FILE HEADER #
##
##   File:         [change.py]
##
##   Author(s):    ['Pedro H.F Matias']
##   Site(s):      ['https://github.com/phfmatias']
##   Email(s):     ['phfmatias@discente.ufg.br']
##   Credits:      ['Copyright © 2024 LEEDMOL. All rights reserved.']
##   Date:         ['15.07.2024']
##   Version:      ['0.0.1']
##   Status:       ['Development']
##   Language:     ['Python']
##   Description:  ['A python script that will change specific words in a text file.']
##   Usage:		   ['python3 change.py <input_file>']

from sys import argv

if len(argv) != 2:
    print("Usage: python3 change.py <input_file>")
    exit(1)

class Change():
    def __init__(self):
        self.arq = argv[-1]
        self.menu()
        self.change()

    def menu(self):
        self.word_to_replace = input("Coloque a palavra que deseja substituir: ")
        self.new_word = input("Coloque a palavra nova: ")
    
    def change(self):
        arq = open(self.arq, "r").read()
        arq = arq.replace(self.word_to_replace, self.new_word)
        open(self.arq, "w").write(arq)

if __name__ == "__main__":
    x = Change()
    x.change()
    print("Palavra substituída com sucesso!")
