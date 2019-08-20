# Demultiplex Example
This example walks through importing the necessary files into the
correct qiime2 artifacts for demultiplexing single-end reads.
   
## Importing the required files 

#### Import the gzipped single-end reads to be demultiplexed.
```
qiime tools import --type MultiplexedSingleEndBarcodeInSequence \
                   --input-path raw_files/demux_ex_fastq.fastq.gz \
                   --output-path artifacts/f_reads.qza
```


#### Import the nucleotide library.
```
qiime tools import --type FeatureData[Sequence] \
                   --input-path raw_files/ex_library.fasta \
                   --output-path artifacts/library.qza
```

#### Importing the barcode sequences that may appear in a read.
```
qiime tools import --type FeatureData[Sequence] \
                   --input-path raw_files/ex_barcodes.fa \
                   --output-path artifacts/barcodes.qza
```

#### Demultiplex the reads, using the previously imported artifacts.
```
qiime pepsirf demux --i-reads artifacts/f_reads.qza \
                    --i-library artifacts/library.qza \
					--i-barcodes artifacts/barcodes.qza \ 
					--p-f-index-location 12 12 2 \ 
					--p-seq-location 43 90 2 \ 
					--p-num-threads 2 \ 
					--p-samplelist raw_files/ex_samplelist.tsv \ 
					--output-dir output_demux \ 
					--verbose
```
