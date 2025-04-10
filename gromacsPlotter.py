##   PYTHON FILE HEADER #
##
##   File:         [gromacsPlotter.py]
##
##   Author(s):    ['Pedro H.F Matias']
##   Credits:      ['Copyright © 2024 LEEDMOL. All rights reserved.']
##   Date:         ['03.04.2024']
##   Version:      ['0.0.1']
##   Status:       ['Development']
##   Language:     ['Python']
##   Description:  ['Python script to automatically plot XVG files from gromacs']
##   Usage:        ['python3 gromacsPlotter.py <file.xvg>']

from sys import argv
import matplotlib.pyplot as plt 

from mpl_toolkits.axes_grid1.inset_locator import inset_axes

if len(argv) < 2:
    print("Usage: python3 gromacsPlotter.py <file.xvg>")
    exit()

def plotXVG(file):
    arq = open(file, 'r').readlines()

    x = []
    y = []   

    for i in range(len(arq)):
        if arq[i].startswith("#") or arq[i].startswith("@"):
            if 'xaxis' in arq[i]:
                xaxis = arq[i].split()[3:]
                xaxis = ' '.join(xaxis).replace('"', '')
            if 'yaxis' in arq[i]:
                yaxis = arq[i].split()[3:]
                yaxis = ' '.join(yaxis).replace('"', '')
        else:
            x.append(float(arq[i].split()[0]))
            y.append(float(arq[i].split()[1]))

    figure = plt.figure(figsize=(10, 6))
    # Reduz um pouco o espaço vertical do gráfico principal
    figure.subplots_adjust(bottom=0.25)
    ax = figure.add_subplot(111)
    ax.plot(x, y, color="#cf6df2")
    ax.set_xlabel(xaxis)
    ax.set_ylabel(yaxis)

    meany = sum(y) / len(y)
    ax.axhline(y=meany, color='#000000', linestyle='--', label='Mean = {:.3f}'.format(meany))
    ax.legend(loc='best', fontsize=10, frameon=True).get_frame().set_edgecolor('black')

    # Posição automática do boxplot abaixo do gráfico
    main_pos = ax.get_position()
    box_height = 0.15
    ax2 = figure.add_axes([
        main_pos.x0,       # mesmo alinhamento à esquerda
        main_pos.y0 - box_height - 0.05,  # abaixo do gráfico com margem
        main_pos.width,    # mesma largura
        box_height         # altura do boxplot
    ])
    ax2.boxplot(y, vert=False)
    ax2.set_yticks([])
    ax2.set_xlabel(xaxis)
    ax2.patch.set_alpha(0)
    ax2.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.5)

    plt.savefig(file.replace('.xvg', '.png'), dpi=300)
    plt.show()

    # figure = plt.figure(figsize=(10, 6))
    # ax = figure.add_subplot(111)
    # ax.plot(x, y, color="#cf6df2")
    # ax.set_xlabel(xaxis)
    # ax.set_ylabel(yaxis)
    # meany = sum(y) / len(y)
    # ax.axhline(y=meany, color='#000000', linestyle='--', label='Mean = {:.3f}'.format(meany))
    # ax.legend(loc='best', fontsize=10, frameon=True).get_frame().set_edgecolor('black')
    # ax2 = figure.add_axes([0.583, 0.531, 0.317, 0.349])
    # ax2.boxplot(y, vert=False)
    # ax2.set_xlabel(xaxis)
    # ax2.set_ylabel(yaxis)
    # ax2.patch.set_alpha(0)
    # ax.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.5)
    # plt.savefig(file.replace('.xvg', '.png'), dpi=300)
    # plt.show()


plotXVG(argv[1])