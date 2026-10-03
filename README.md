# JinLab_makeTreeExample

Example: build an Ascomycota phylogeny of 11 taxa with
[stajichlab/nf_phyling](https://github.com/stajichlab/nf_phyling) and FastTree.

- `CLAUDE.md`: the instructions given to the assistant and the run settings.
- `run_jinlab_tree.sh`: SLURM launcher (`sbatch run_jinlab_tree.sh`).
- `short_queue.config`: puts every step on the UCR HPCC `short` queue (2 h).
- `pep/PROVENANCE.tsv`: source path, size, sequence count and md5 of each input proteome.

The proteomes are not in this repository. They come from FungiDB release 68. Use the paths in
`pep/PROVENANCE.tsv` to copy them to `pep/` as `<label>.fa.gz`.
