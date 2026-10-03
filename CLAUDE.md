# jinlab_tree: Ascomycota phylogeny

## Goal

Build a phylogeny of the 11 taxa in the tree below. Use real data. Resolve the tree with FastTree.

```
ASCOMYCOTA
│
├── Saccharomycotina
│   ├── Candida albicans
│   └── Saccharomyces cerevisiae
│
└── Pezizomycotina
    │
    ├── Eurotiomycetes
    │   ├── Aspergillus niger
    │   ├── Aspergillus fumigatus
    │   └── Penicillium chrysogenum
    │
    └── Leotiomycetes + Sordariomycetes
        │
        ├── Leotiomycetes
        │   └── Botrytis cinerea
        │
        └── Sordariomycetes
            │
            ├── Sordariomycetidae
            │   ├── Magnaporthe oryzae
            │   └── Neurospora crassa
            │
            └── Hypocreomycetidae
                ├── Verticillium dahliae
                │
                └── Hypocreales
                    ├── Gibberella zeae
                    │   (= Fusarium graminearum)
                    └── Trichoderma virens
```

## Instructions

1. **Verify the taxa list** before you use it. Report any name change or doubtful placement.
2. **Proteomes:** use FungiDB, if possible. Use one strain per taxon. Uncompress the gzip files or ensure gzip files are compressed with bgzip
3. **Provenance:** record where every input file came from. Give the source path or URL, the date, the size, the sequence count and the md5. Keep this in `PROVENANCE.tsv`. State clearly if you copied a local file and did not download it.
4. **Pipeline:** run `nextflow run stajichlab/nf_phyling`. This pulls the pipeline from GitHub. No clone is needed.
5. **Tree method:** use the FastTree tree. Use the `-boot` tree (SH-like support) for the figure.
6. **Queue:** run every step on the SLURM `short` queue. The limit is 2 hours. Use `short_queue.config` to force this.
7. **Root:** root the tree on Saccharomycotina (*Saccharomyces* and *Candida*).
8. **Figure:** draw the tree with bootstrap support on the internal nodes. Add internal labels for the named lineages (for example Eurotiomycetes, Sordariomycetes, Hypocreales).
9. **Validate your statements.** Report only results from real data and real statistics. If you have no data for a decision, say so.

## Run settings

| Item | Value |
|---|---|
| Launcher | `sbatch run_jinlab_tree.sh` |
| Pipeline | `stajichlab/nf_phyling` |
| Profile | `singularity_slurm,ucr_hpcc` |
| Site override | `short_queue.config` (every step on `short`, 2 h) |
| Mode | `--seq_type protein` |
| Input | `pep/` (one `.fa.gz` per taxon) |
| Markerset | `fungi_odb12` (assistant's choice; change it if needed) |
| Output | `results/pep` |
| Prefix | `jinlab_tree` |
| Phyling DB cache | `phyling_db/` |

## Inputs

The proteomes come from the shared FungiDB release 68 copy at `/bigdata/stajichlab/shared/FungiDB/release-68/<organism>/fasta/data/FungiDB-68_<organism>_AnnotatedProteins.fasta.gz`. Direct download from `fungidb.org` was not used.

| Requested taxon | FungiDB strain |
|---|---|
| Candida albicans | SC5314 |
| Saccharomyces cerevisiae | S288C |
| Aspergillus niger | CBS 513.88 |
| Aspergillus fumigatus | Af293 |
| Penicillium chrysogenum | Wisconsin 54-1255 (FungiDB name: *P. rubens*) |
| Botrytis cinerea | B05.10 |
| Magnaporthe oryzae | 70-15 (FungiDB name: *Pyricularia oryzae*) |
| Neurospora crassa | OR74A |
| Verticillium dahliae | JR2 |
| Gibberella zeae | PH-1 (FungiDB name: *Fusarium graminearum*) |
| Trichoderma virens | Gv29-8 |

Do not use `Pchrysosporium`. It is *Phanerochaete chrysosporium*, a basidiomycete.

## Notes

- The 2-hour limit also applies to the Nextflow driver job. If it times out, resubmit with the same command. The script uses `-resume`.
- IQ-TREE and RAxML-NG may exceed 2 hours. The pipeline ignores their failures. FastTree does not depend on them.
- Put `-c` before `run` in the Nextflow command: `nextflow -c short_queue.config run ...`.
