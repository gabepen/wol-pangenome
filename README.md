# wol-pangenome

## ncbi-datasets-parser.py
    - filters down the complete wolbachia genome dataset to have an unbaised representation of different wolbachia supergroups

## extract-gene-seq.py
    - functions for extracting gene sequences from a dataset of genomic fastas based on gene-ID or 16S sequence predictions 

## binarize-tree.py
    - uses ete3 toolkit to binarize guide tree for cactus 
    - ete3 must be installed in seperate env
        - conda create -n ete3 python=3
        - conda activate ete3
        - conda install -c etetoolkit ete3 ete_toolchain
    