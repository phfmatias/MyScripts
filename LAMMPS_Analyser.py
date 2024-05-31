##   PYTHON FILE HEADER #
##
##   File:         [LAMMPS_Analyser.py]
##
##   Author(s):    ['Pedro H.F Matias']
##   Credits:      ['Copyright © 2024 LEEDMOL. All rights reserved.']
##   Date:         ['31.05.2024']
##   Version:      ['0.0.1']
##   Status:       ['Development']
##   Language:     ['Python']
##   Description:  ['This script reads a LAMMPS log file and plots the percentage variation of each species over time.']
##   Usage:        ['python LAMMPS_Analyser.py <file_to_analyze>']



import matplotlib.pyplot as plt
from sys import argv

file = argv[-1]

arq = open(file, 'r').readlines()

species_set = set() 
species_dict = {}
quant_dict = {}
mole_dict = {}
nspecies_dict = {}

for i in range(len(arq)):
    if '# Timestep' in arq[i]:
        step = int(arq[i+1].split()[0])
        species = arq[i].split()[4:]
        quantities = arq[i+1].split()[3:]
        nmoles = int(arq[i+1].split()[1])
        nspecies = int(arq[i+1].split()[2])

        species_dict[step] = species
        quant_dict[step] = [int(q) for q in quantities]
        mole_dict[step] = nmoles
        nspecies_dict[step] = nspecies
        
        species_set.update(species)


percentage_dict = {species: [] for species in species_set}


steps_to_analyze = range(157, 8152, 5)

# Calcular as porcentagens
for step in steps_to_analyze:
    if step in quant_dict:
        total_moles = mole_dict[step]
        quantities = quant_dict[step]
        species = species_dict[step]
        
        # Inicializar porcentagens para todas as espécies como 0
        step_percentages = {species: 0 for species in species_set}
        
        # Calcular as porcentagens para as espécies presentes
        for i, specie in enumerate(species):
            percentage = (quantities[i] / total_moles) * 100
            step_percentages[specie] = percentage
        
        # Adicionar os valores calculados ao dicionário de porcentagens
        for specie in species_set:
            percentage_dict[specie].append(step_percentages[specie])
    else:
        # Se não houver dados para um step, adiciona zero às porcentagens
        for specie in percentage_dict:
            percentage_dict[specie].append(0)

def plot_species(selected_species):
    plt.figure(figsize=(12, 8))
    for specie in selected_species:
        if specie in percentage_dict:
            plt.plot(steps_to_analyze, percentage_dict[specie], label=specie)
        else:
            print(f"Espécie '{specie}' não encontrada nos dados.")
    
    plt.xlabel('Timestep')
    plt.ylabel('Percentage of each species (%)')
    plt.title('Percentage variation of each species over time')
    plt.legend(loc='best', frameon=False)
    plt.show()


def select_species(option, specific_species=None):
    if option == 'all':
        selected_species = species_set
    elif option == 'specific':
        if specific_species:
            selected_species = specific_species
        else:
            selected_species = []
    elif option == 'single':
        if specific_species and len(specific_species) == 1:
            selected_species = specific_species
        else:
            selected_species = []
    else:
        selected_species = []

    return selected_species




# # Plotar todas as espécies
# selected_species = select_species('all')
# plot_species(selected_species)

# # Plotar algumas espécies específicas
# selected_species = select_species('specific', ['NO', 'H2O', 'O3Na6'])
# plot_species(selected_species)

# # Plotar uma única espécie
# selected_species = select_species('single', ['H2O'])
# plot_species(selected_species)
