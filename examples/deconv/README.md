# Species Deconvolution Example
This example walks through importing the necessary files into the correct qiime2 artifacts for performing species
deconvolution.

## Importing the files required for creating the linkage file.

#### Import the file of designed peptides.
```
qiime tools import \
--type FeatureData[ProteinSequence] \
--input-path raw_files/ex_peptide_file.fasta \
--output-path artifacts/ex_peptide_file.qza
```

#### Import the protein sequences used to create the designed peptides.
```
qiime tools import \
--type FeatureData[ProteinSequence] \
--input-path raw_files/ex_protein_file.fasta \
--output-path artifacts/ex_protein_file.qza
```

#### Create the linkage file that maps peptdies to species.
```
qiime pepsirf create-linkage \
--i-protein-file artifacts/ex_protein_file.qza \
--i-peptide-file artifacts/ex_peptide_file.qza \
--p-kmer-size 9 \
--o-linked artifacts/linked_file.qza \
--verbose
```

#### Import the file containing names of enriched peptides.
```
qiime tools import \
--type EnrichedPeptide \
--input-path raw_files/ex_enriched_file.txt \
--output-path artifacts/ex_enriched_file.qza
```

#### Unzip the lineage file (unzips to ~30MB)
```
gunzip raw_files/virus_lineage.dmp.gz
```

#### Import the lineage file to qiime format
```
qiime tools import \
--type TaxIdLineage \
--input-path raw_files/virus_lineage.dmp \
--output-path artifacts/virus_lineage.qza
```

#### Perform species decovolution
```
qiime pepsirf deconv \
--i-linked artifacts/linked_file.qza \
--i-enriched artifacts/ex_enriched_file.qza \
--i-id-name-map artifacts/virus_lineage.qza \
--p-threshold 10  \
--output-dir deconv_output
```
