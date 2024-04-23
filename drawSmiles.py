from rdkit import Chem
from rdkit.Chem import (
    AllChem,
    rdCoordGen,
)
from rdkit.Chem import Draw
from rdkit.Chem.Draw import IPythonConsole
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from IPython.display import SVG

plt.style.use("seaborn-notebook")
IPythonConsole.ipython_useSVG = True  

COLOR_TUPLES = [
    (230, 159, 0),
    (86, 180, 233),
    (0, 158, 115),
    (240, 228, 66),
    (0, 114, 178),
    (213, 94, 0),
    (204, 121, 167),
    (204, 204, 204),  # Gray, added by me
]
COLOR_FRAC = [tuple(x / 255 for x in color) for color in COLOR_TUPLES]
COLOR_MAP = {
    "Center atom": COLOR_FRAC[1],
    "Atom in a ring": COLOR_FRAC[6],
    "Aromatic atom": COLOR_FRAC[3],
    "Other atoms": COLOR_FRAC[7],
    "Bonds": COLOR_FRAC[7],
}


def get_atom_colors(molecule, atoms, centers=None):
    """Define some colors for different atoms."""
    colors = {}
    for atom in atoms:
        if centers is not None and atom in centers:
            colors[atom] = COLOR_MAP["Center atom"]
        else:
            if molecule.GetAtomWithIdx(atom).GetIsAromatic():
                colors[atom] = COLOR_MAP["Aromatic atom"]
            elif molecule.GetAtomWithIdx(atom).IsInRing():
                colors[atom] = COLOR_MAP["Atom in a ring"]
            else:
                colors[atom] = COLOR_MAP["Other atoms"]
    return colors


def get_bond_colors(bonds):
    """Define colors for bonds."""
    return {bond: COLOR_MAP["Bonds"] for bond in bonds}

def get_environment(molecule, center, radius):
    """Get the environment of a certain radius around a center atom."""
    if not molecule.GetNumConformers():
        rdDepictor.Compute2DCoords(mol)
    env = Chem.FindAtomEnvironmentOfRadiusN(molecule, radius, center)
    atoms = set([center])
    bonds = set([])
    for bond in env:
        atoms.add(molecule.GetBondWithIdx(bond).GetBeginAtomIdx())
        atoms.add(molecule.GetBondWithIdx(bond).GetEndAtomIdx())
        bonds.add(bond)
    atoms = list(atoms)
    bonds = list(bonds)

    atom_colors = get_atom_colors(molecule, atoms, centers=set([center]))
    bond_colors = get_bond_colors(bonds)

    return atoms, bonds, atom_colors, bond_colors

def draw_molecule_and_bit_info_grid(molecule, info, bit, size, max_examples=None, mols_per_row=3
):
    """Highlight a bit in a given molecule."""
    atoms_to_highlight = []
    bonds_to_highlight = []
    atoms_to_highlight_colors = []
    bonds_to_highlight_colors = []
    molecules_to_draw = []
    for i, example in enumerate(info[bit]):
        if max_examples is not None and i + 1 > max_examples:
            break
        center, radius = example
        atoms, bonds, atom_colors, bond_colors = get_environment(
            molecule, center, radius
        )
        atoms_to_highlight.append(atoms)
        bonds_to_highlight.append(bonds)
        atoms_to_highlight_colors.append(atom_colors)
        bonds_to_highlight_colors.append(bond_colors)
        molecules_to_draw.append(molecule)

    options = Draw.rdMolDraw2D.MolDrawOptions()
    options.prepareMolsForDrawing = True
    options.fillHighlights = True
    
    return Draw.MolsToGridImage(
        molecules_to_draw,
        molsPerRow=min(mols_per_row, len(molecules_to_draw)),
        subImgSize=(size, size),
        highlightAtomLists=atoms_to_highlight,
        highlightBondLists=bonds_to_highlight,
        highlightAtomColors=atoms_to_highlight_colors,
        highlightBondColors=bonds_to_highlight_colors,
        drawOptions=options,
    )
def show_all_on_bits(molecule, info, size):
    """Draw all on bits"""
    atoms_to_highlight = []
    bonds_to_highlight = []
    atoms_to_highlight_colors = []
    bonds_to_highlight_colors = []
    molecules_to_draw = []
    legends = []
    for key in sorted(info.keys()):
        center, radius = info[key][0]
        legends.append(f"Bit {key}")
        atoms, bonds, atom_colors, bond_colors = get_environment(
            molecule, center, radius
        )
        atoms_to_highlight.append(atoms)
        bonds_to_highlight.append(bonds)
        atoms_to_highlight_colors.append(atom_colors)
        bonds_to_highlight_colors.append(bond_colors)
        molecules_to_draw.append(molecule)

    options = Draw.rdMolDraw2D.MolDrawOptions()
    options.prepareMolsForDrawing = True
    options.fillHighlights = True
    return Draw.MolsToGridImage(
        molecules_to_draw,
        molsPerRow=min(5, len(molecules_to_draw)),
        subImgSize=(size, size),
        legends=legends,
        highlightAtomLists=atoms_to_highlight,
        highlightBondLists=bonds_to_highlight,
        highlightAtomColors=atoms_to_highlight_colors,
        highlightBondColors=bonds_to_highlight_colors,
        drawOptions=options,
    )

