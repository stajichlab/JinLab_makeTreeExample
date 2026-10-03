#!/usr/bin/bash -l
#SBATCH -p short -c 2 --mem 4gb -t 2:00:00 --out logs/jinlab_tree_nf.%j.log -J jinlab_tree
# Nextflow driver: stajichlab/nf_phyling, protein mode, all steps on the 'short' queue.
# Resubmit with the same command to continue (-resume) if the 2 h driver limit is hit.
cd /bigdata/stajichlab/jstajich/projects/jinlab_tree || exit 1
# Pipeline source: the published GitHub project (or a local checkout via PIPELINE=<dir>).
# REVISION pins a git branch/tag/commit.
PIPELINE=${PIPELINE:-stajichlab/nf_phyling}
REVISION=${REVISION:-}
export NXF_SINGULARITY_CACHEDIR=/bigdata/stajichlab/shared/singularity_cache
module load singularity
module load nextflow
nextflow -c short_queue.config run "${PIPELINE}" ${REVISION:+-r "${REVISION}"} -ansi-log false \
    -profile singularity_slurm,ucr_hpcc \
    --seq_type protein \
    --input /bigdata/stajichlab/jstajich/projects/jinlab_tree/pep \
    --prefix jinlab_tree \
    --markerset fungi_odb12 \
    --outdir results/pep \
    --phyling_db /bigdata/stajichlab/jstajich/projects/jinlab_tree/phyling_db \
    -resume
