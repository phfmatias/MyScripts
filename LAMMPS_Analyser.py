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

if len(argv) < 2:
    print("Usage: python LAMMPS_Analyser.py <file_to_analyze>")
    exit()

class LammpsAnalyser:
    def __init__(self):
        self.file = argv[1]
        self.species_set = set() 
        self.species_dict = {}
        self.quant_dict = {}
        self.mole_dict = {}
        self.nspecies_dict = {}
        self.option_menu = None

        if argv[-1] == 'DEBUG':
            self.option_menu = 1
            self.extract_infos()
            self.runner()

        else:
            self.extract_infos()
            self.Menu()
            self.runner()

    def extract_infos(self):
        with open(self.file, 'r') as f:
            arq = f.readlines()

        for i in range(len(arq)):
            if '# Timestep' in arq[i]:
                step = int(arq[i+1].split()[0])
                species = arq[i].split()[4:]
                quantities = arq[i+1].split()[3:]
                nmoles = int(arq[i+1].split()[1])
                nspecies = int(arq[i+1].split()[2])

                self.species_dict[step] = species
                self.quant_dict[step] = [int(q) for q in quantities]
                self.mole_dict[step] = nmoles
                self.nspecies_dict[step] = nspecies

                self.species_set.update(species)

        self.percentage_dict = {species: [] for species in self.species_set}

        steps = sorted(self.nspecies_dict.keys())
        self.steps_to_analyze = steps

        # Calcular as porcentagens
        for step in self.steps_to_analyze:
            if step in self.quant_dict:
                total_moles = self.mole_dict[step]
                quantities = self.quant_dict[step]
                species = self.species_dict[step]

                # Inicializar porcentagens para todas as espécies como 0
                step_percentages = {species: 0 for species in self.species_set}

                # Calcular as porcentagens para as espécies presentes
                for i, specie in enumerate(species):
                    percentage = (quantities[i] / total_moles) * 100
                    step_percentages[specie] = percentage

                # Adicionar os valores calculados ao dicionário de porcentagens
                for specie in self.species_set:
                    self.percentage_dict[specie].append(step_percentages[specie])
            else:
                # Se não houver dados para um step, adiciona zero às porcentagens
                for specie in self.percentage_dict:
                    self.percentage_dict[specie].append(0)

    def plot_species(self, selected_species, name, menu_option):
        plt.figure(figsize=(12, 8))


        first_10_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        
        c = 0

        #sorte species by max percentage

        selected_species = sorted(selected_species, key=lambda x: max(self.percentage_dict[x]), reverse=True)

        for specie in selected_species:
            if specie in self.percentage_dict:
                plt.plot(self.steps_to_analyze, self.percentage_dict[specie], label=specie, color=first_10_colors[c])
                c+=1
            else:
                print(f"Espécie '{specie}' não encontrada nos dados.")

        plt.xlabel('Timestep')
        plt.ylabel('Percentage of each species (%)')
        plt.title('Percentage variation of each species over time')
        if menu_option == 1:
            sorted_species = sorted(self.species_set, key=lambda x: max(self.percentage_dict[x]), reverse=True)
            selected_species = sorted_species[:10]
            plt.legend(selected_species, loc='best', ncol=2)
            plt.subplots_adjust(right=0.8)
        else:
            plt.legend(loc='best', frameon=False)
        plt.savefig(f'{name}.png')

    def select_species(self, option, specific_species=None):

        if option == 'all':
            selected_species = list(self.species_set)
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

    def Menu(self):
        print("Select an option:")
        print("1 - Plot all species")
        print("2 - Plot specific species")
        print("3 - Plot a single species")
        print("4 - PLot specific species without Hydrogen")
        print("5 - Exit")
        self.option_menu = int(input("Option: "))
        print('\n')

    def runner(self):

        self.species_set = sorted(self.species_set)

        if self.option_menu == 1:
            selected_species = self.select_species('all')
            name_saver = 'all_species_{}'.format(self.file.split('.')[0])
            self.plot_species(selected_species, name_saver, self.option_menu)
            print("Plot saved as {}.png".format(name_saver))

        elif self.option_menu == 2:
            print("Available species:")
            print(", ".join(self.species_set))
            print('\n')
            species = input("Enter the species separated by commas: ")
            selected_species = self.select_species('specific', [s.strip() for s in species.split(',')])
            name_saver = 'specific_species_{}'.format(self.file.split('.')[0])
            self.plot_species(selected_species, name_saver, self.option_menu)
            print("Plot saved as {}.png".format(name_saver))

        elif self.option_menu == 3:
            print("Available species:")
            print(", ".join(self.species_set))
            print('\n')
            species = input("Enter the species: ")
            selected_species = self.select_species('single', [species.strip()])
            name_saver = 'single_species_{}'.format(self.file.split('.')[0])
            self.plot_species(selected_species, name_saver, self.option_menu)
            print("Plot saved as {}.png".format(name_saver))

        elif self.option_menu == 4:
            print("Available species:")
            wit_hyd = [specie for specie in self.species_set if 'H' not in specie]
            print(", ".join(wit_hyd))
            print('\n')
            species = input("Enter the species separated by commas: ")
            selected_species = self.select_species('specific', [s.strip() for s in species.split(',')])
            name_saver = 'specific_species_without_Hydrogen_{}'.format(self.file.split('.')[0])
            self.plot_species(selected_species, name_saver, self.option_menu)
            print("Plot saved as {}.png".format(name_saver))


        elif self.option_menu == 5:
            exit()

        else:
            print("Invalid option. Try again.")
            self.Menu()
            self.runner()

if __name__ == "__main__":
    LammpsAnalyser()
