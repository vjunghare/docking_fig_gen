# Docking figure generation

PyMOL scripts that turn docked ligand–receptor complexes into interaction figures. For each complex, the polar contacts listed in an interaction table are drawn as dashed distance lines between the ligand and the receptor residues, and a high-resolution image is rendered.

The interaction table is built with the in-house `pdb_std` program from the Macromolecular Analysis Toolkit (MAT, <http://mat.iitr.ac.in>). You can also supply your own table in the same format (see [Interaction table format](#interaction-table-format)).

## Contents

| File | Purpose |
|------|---------|
| `interaction_table.sh` | Runs `pdb_std` on every complex PDB and saves a raw interaction table for each one. |
| `table_mod.py` | Filters the raw tables and writes the `mod_<name>.csv` files used for drawing, plus a combined `table_all.csv`. |
| `complex_nw2.py` | Reads each complex and its `mod_<name>.csv`, draws the figure with the PyMOL API, and saves a PNG and a PyMOL session. |

## Requirements

- Linux or another Bash-compatible environment.
- PyMOL with Python 2 support. The scripts use Python 2 syntax (`print` statements).
- Only for building tables automatically: the `pdb_std` executable from MAT, placed in the working folder. It is not included in this repository.

## Workflow

Put the complex PDB files and the three scripts in one folder, then run the steps in order.

1. **Build the interaction tables** (skip this and step 2 if you supply your own tables):

   ```bash
   bash interaction_table.sh
   ```

   For every `*.pdb`, this runs `./pdb_std -i <name>.pdb -E` and saves the ligand–receptor atom pairs with their distances as `<name>.csv`.

2. **Filter the tables:**

   ```bash
   python2 table_mod.py
   ```

   This keeps the polar contacts: pairs where either atom name contains `C` are removed. It writes `mod_<name>.csv` for each complex and a combined `table_all.csv`.

3. **Draw the figures:**

   ```bash
   pymol -cq complex_nw2.py
   ```

   Each complex is drawn as follows:
   - The cartoon is shown with 0.4 transparency, and the contacting residues are shown as sticks.
   - Ligand and other non-protein atoms are shown as sticks and spheres.
   - Contacts are drawn as dashed lines, and distance and residue labels are hidden.
   - Every complex is aligned to the first one, and the camera is centred on the contacting residues so that the figures are comparable.
   - The result is ray-traced at 2560 × 1440 and saved as `<name>.png` and `<name>.pse`.

## Interaction table format

`complex_nw2.py` expects one file per complex, named `mod_<name>.csv` for the structure `<name>.pdb`. Each row is one atom pair, with whitespace-separated (tab or space) columns. Commas are not split.

| Column | Content | Used by the figure script |
|:------:|---------|:-------------------------:|
| 1 | Ligand residue name | Yes |
| 2 | Ligand residue number | Yes |
| 3 | Ligand atom name | Yes |
| 4 | Ligand chain | No |
| 5 | Ligand atom number | No |
| 6 | Separator (`AND`) | No |
| 7 | Receptor residue name | Yes |
| 8 | Receptor residue number | Yes |
| 9 | Receptor atom name | Yes |
| 10 | Receptor chain | No |
| 11 | Receptor atom number | No |
| 12 | Distance (Å) | No |

Example rows (illustrative):

```text
LIG	300	O1	A	1	AND	SER	62	OG	A	323	3.0
LIG	300	N2	A	3	AND	GLU	96	OE1	A	595	3.3
```

Notes for your own tables:
- Keep all columns, because the script reads them by position. Use any placeholder for the columns that aren't used.
- The receptor atoms are selected on chain `A`, and all complexes should share the same residue numbering so that they align and share one view.
- If you supply `mod_<name>.csv` files directly, you don't need `pdb_std` or `table_mod.py`.

## Notes

- `complex_nw2.py` processes every `*.pdb` in the current folder. The first file that `glob` returns is used as the reference for alignment and view, and its order is not sorted.
- `table_mod.py` reads the raw `pdb_std` output and relies on its column layout. It is not meant for hand-made tables.
- Generated files (`<name>.csv`, `mod_*.csv`, `table_all.csv`, PNG and PyMOL sessions) are written to the working folder.
