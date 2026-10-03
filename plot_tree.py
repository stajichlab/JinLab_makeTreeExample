#!/usr/bin/env python3
"""Draw the FastTree support tree: rooted on Saccharomycotina, support at nodes, lineage labels.

Usage: plot_tree.py TREEFILE OUTPREFIX
"""
import sys
from Bio import Phylo
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

treefile, outprefix = sys.argv[1], sys.argv[2]

# tip id -> (species as requested, strain/FungiDB source)
TIPS = {
    "Calbicans_SC5314": ("Candida albicans", "SC5314"),
    "Scerevisiae_S288C": ("Saccharomyces cerevisiae", "S288C"),
    "Aniger_CBS513-88": ("Aspergillus niger", "CBS 513.88"),
    "Afumigatus_Af293": ("Aspergillus fumigatus", "Af293"),
    "Prubens_Wisconsin54-1255": ("Penicillium chrysogenum", "Wisconsin 54-1255 (FungiDB: P. rubens)"),
    "Bcinerea_B05-10": ("Botrytis cinerea", "B05.10"),
    "Poryzae_70-15": ("Magnaporthe oryzae", "70-15 (FungiDB: Pyricularia oryzae)"),
    "Ncrassa_OR74A": ("Neurospora crassa", "OR74A"),
    "Vdahliae_JR2": ("Verticillium dahliae", "JR2"),
    "Fgraminearum_PH-1": ("Gibberella zeae", "PH-1 (= Fusarium graminearum)"),
    "Tvirens_Gv29-8": ("Trichoderma virens", "Gv29-8"),
}
# lineage label -> member tips (from the requested taxonomy)
CLADES = {
    "Saccharomycotina": ["Calbicans_SC5314", "Scerevisiae_S288C"],
    "Pezizomycotina": [t for t in TIPS if t not in ("Calbicans_SC5314", "Scerevisiae_S288C")],
    "Eurotiomycetes": ["Aniger_CBS513-88", "Afumigatus_Af293", "Prubens_Wisconsin54-1255"],
    "Leotiomycetes + Sordariomycetes": ["Bcinerea_B05-10", "Poryzae_70-15", "Ncrassa_OR74A",
                                        "Vdahliae_JR2", "Fgraminearum_PH-1", "Tvirens_Gv29-8"],
    "Sordariomycetes": ["Poryzae_70-15", "Ncrassa_OR74A", "Vdahliae_JR2", "Fgraminearum_PH-1", "Tvirens_Gv29-8"],
    "Sordariomycetidae": ["Poryzae_70-15", "Ncrassa_OR74A"],
    "Hypocreomycetidae": ["Vdahliae_JR2", "Fgraminearum_PH-1", "Tvirens_Gv29-8"],
    "Hypocreales": ["Fgraminearum_PH-1", "Tvirens_Gv29-8"],
}

tree = Phylo.read(treefile, "newick")
yeast = tree.common_ancestor(*[{"name": t} for t in CLADES["Saccharomycotina"]])
assert {t.name for t in yeast.get_terminals()} == set(CLADES["Saccharomycotina"]), \
    "Saccharomycotina is not a clade in the unrooted tree"
yeast_support = yeast.confidence
tree.root_with_outgroup(yeast, outgroup_branch_length=(yeast.branch_length or 0.0) / 2)
# the two root children share one split, so they carry the same support
for c in tree.root.clades:
    if c.confidence is None:
        c.confidence = yeast_support
tree.ladderize()

# --- check each named lineage against the data (monophyly) ---
found = {}
for name, members in CLADES.items():
    mrca = tree.common_ancestor(*[{"name": m} for m in members])
    tips = {t.name for t in mrca.get_terminals()}
    found[name] = (tips == set(members), mrca)
    print(f"{name:34s} monophyletic={tips == set(members)}")

# --- layout ---
terms = tree.get_terminals()
ypos = {t: i for i, t in enumerate(reversed(terms))}
xpos = {}
def xcalc(clade, x):
    x += clade.branch_length or 0.0
    xpos[clade] = x
    for c in clade.clades:
        xcalc(c, x)
xcalc(tree.root, 0.0)
def ycalc(clade):
    if clade.is_terminal():
        return ypos[clade]
    ys = [ycalc(c) for c in clade.clades]
    ypos[clade] = sum(ys) / len(ys)
    return ypos[clade]
ycalc(tree.root)

INK, MUTED, GRID = "#1f2328", "#59636e", "#8c959f"
fig = plt.figure(figsize=(12.5, 6.6), dpi=200)
ax = fig.add_axes([0.02, 0.09, 0.62, 0.84])
ax2 = fig.add_axes([0.64, 0.09, 0.34, 0.84], sharey=ax)
def draw(clade):
    x0 = xpos[clade] - (clade.branch_length or 0.0)
    ax.plot([x0, xpos[clade]], [ypos[clade]] * 2, color=INK, lw=1.6, solid_capstyle="butt")
    if clade.clades:
        ys = [ypos[c] for c in clade.clades]
        ax.plot([xpos[clade]] * 2, [min(ys), max(ys)], color=INK, lw=1.6, solid_capstyle="butt")
        for c in clade.clades:
            draw(c)
draw(tree.root)

xmax = max(xpos[t] for t in terms)
pad = xmax * 0.02
for t in terms:
    sp, strain = TIPS[t.name]
    ax.text(xpos[t] + pad, ypos[t] + 0.08, sp, style="italic", va="center", ha="left", fontsize=10.5, color=INK)
    ax.text(xpos[t] + pad, ypos[t] - 0.30, strain, va="center", ha="left", fontsize=6.8, color=MUTED)

# support values (FastTree SH-like local support, 0-1) above the stem of each internal node
for c in tree.get_nonterminals():
    if c is tree.root or c.confidence is None:
        continue
    ax.text(xpos[c] - pad * 0.5, ypos[c] + 0.10, f"{c.confidence:.2f}", fontsize=6.8, color=MUTED,
            ha="right", va="bottom")

# lineage brackets: one column per lineage so no label shares space with another
order = ["Leotiomycetes", "Hypocreales", "Eurotiomycetes", "Sordariomycetidae", "Saccharomycotina",
         "Hypocreomycetidae", "Sordariomycetes", "Leotiomycetes + Sordariomycetes", "Pezizomycotina"]
bcin = next(t for t in terms if t.name == "Bcinerea_B05-10")
for col, name in enumerate(order):
    if name == "Leotiomycetes":
        ys = [ypos[bcin]]
    else:
        ok, mrca = found[name]
        if not ok:
            continue
        ys = [ypos[t] for t in mrca.get_terminals()]
    x = col + 0.25
    ax2.plot([x, x], [min(ys) - 0.28, max(ys) + 0.28], color=GRID, lw=1.4, solid_capstyle="round")
    ax2.text(x + 0.18, (min(ys) + max(ys)) / 2, name, rotation=90, va="center", ha="left",
             fontsize=8.5, color=INK, fontweight="bold")
ax2.set_xlim(0, len(order))
ax2.axis("off")

# scale bar
sb = 0.1
ax.plot([0, sb], [-1.0, -1.0], color=INK, lw=1.6)
ax.text(sb / 2, -1.25, f"{sb} substitutions/site", ha="center", va="top", fontsize=7.5, color=MUTED)

ax.set_xlim(-xmax * 0.02, xmax * 1.75)
ax.set_ylim(-1.9, len(terms) - 0.2)
ax.axis("off")
fig.text(0.02, 0.965, "Ascomycota: 11 taxa, FastTree on 80 BUSCO fungi_odb12 loci (LG model), rooted on Saccharomycotina",
         fontsize=10.5, color=INK, ha="left")
fig.text(0.02, 0.012, "Node values: FastTree SH-like local support (1000 resamples, range 0-1), not bootstrap. "
         "Proteomes: FungiDB release 68. Scale: substitutions per site.", fontsize=7, color=MUTED)
fig.savefig(outprefix + ".png", bbox_inches="tight", facecolor="white")
fig.savefig(outprefix + ".pdf", bbox_inches="tight", facecolor="white")
fig.savefig(outprefix + ".svg", bbox_inches="tight", facecolor="white")
