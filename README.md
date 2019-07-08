# q2-pepsirf: A QIIME 2 plugin for the [pep_sirf](https://github.com/LadnerLab/PepSIRF) software package

### Install 
The [pep_sirf](https://github.com/LadnerLab/PepSIRF) package must first be installed and built, 
and the executable must be accessible by calling 'pep_sirf' from your command-line environment.
The best way to do this would be to put the [pep_sirf](https://github.com/LadnerLab/PepSIRF) executable
somewhere located in your $PATH.

Clone this repo and enter the ```q2-pepsirf``` directory.
Then, activate your qiime2 conda environment and run 
```
python setup.py install
qiime dev refresh-cache
```
The plugin should now be available from qiime.

### Usage

#### Demux

```
Usage: qiime pepsirf demux [OPTIONS]

  Description

Inputs:
  --i-reads ARTIFACT MultiplexedSingleEndBarcodeInSequence
                          Input reads file to parse. These should be in fastq
                          format. Reads can already be indexed on the reverse
                          barcode sequences, in which case the r-index
                          parameter should not be specified. If the reverse
                          barcodes are in the reads the r-index parameter
                          should be specified. If you have one file for
                          forward reads and one for reverse reads the
                          demux_paired command should be used.      [required]
  --i-library ARTIFACT FeatureData[Sequence]
                          Designed library containing nucleic acidpeptides.
                          Library should be in fasta format and should contain
                          sequences thatwere used to design the sequences in
                          reads.                                    [required]
  --i-barcodes ARTIFACT FeatureData[Sequence]
                          Name of fasta file containing forward and
                          (potentially) reverse barcode sequences.  [required]
Parameters:
  --p-samplelist TEXT     A tab-delimited list of samples, one sample per
                          line. If the samples are already indexed by I2 only
                          the forward index (I1) and the sample name are
                          required. The first item in each tab-delimited line
                          is the forward (I1) index, the second (if included)
                          is the reverse (I2) index, and the third is the
                          sample name.                              [required]
  --p-f-index TEXT        Positional values for f-index. This argument must
                          be passed as 3 comma-separated values. The first
                          item represents the (0-based) expected start index
                          of the forward index. The second represents the
                          length of the forward index, and the third
                          represents the number of mismatches that are
                          tolerated for this index. An example is
                          "--f_index12,12,2". This says that we start at
                          (0-based) index 12, grab the next 12 characters, and
                          if a perfect match is not found for these grabbed
                          characters we look for a match to the forward
                          indexsequences with up to two allowed mismatches.
                                                                    [required]
  --p-seq TEXT            Positional values for nucleotide sequence data.
                          This argument must be passed as 3 comma-separated
                          values. The first item represents the (0-based)
                          expected start index of the sequence. The second
                          represents the length of the sequence, and the third
                          represents the number of mismatches that are
                          tolerated for a sequence. An example is "--seq
                          43,90,2". This says that we start at (0-based) index
                          43, grab the next 90 characters, and if a perfect
                          match is not found for these grabbed characters we
                          look for a match to the designed library sequences
                          with up to two allowedmismatches.         [required]
  --p-r-index TEXT        Positional values for r-index. This argument must
                          be passed as 3 comma-separated values. The first
                          item represents the (0-based) expected start index
                          of the reverse index. The second represents the
                          length of the reverse index, and the third
                          represents the number of mismatches that are
                          tolerated for this index. An example is
                          "--r_index12,12,2". This says that we start at
                          (0-based) index 12, grab the next 12 characters, and
                          if a perfect match is not found for these grabbed
                          characters we look for a match to the reverse
                          indexsequences with up to two allowed mismatches.
                                                                 [default: '']
  --p-num-threads INTEGER The number of threads to use for analyses
                                                                  [default: 2]
  --p-read-per-loop INTEGER
                          The number of fastq records read a time.A higher
                          value will result in more memory usage by the
                          program, but will also result in fewer disk
                          accesses, increasing performance of the program.
                                                             [default: 800000]
  --p-concatemer TEXT     Concatenated primer sequences. If this concatemer
                          is found within a read, we know that a potential
                          sequence from the designed library was not included.
                          The number of times this concatemer is recorded in
                          the input file is reported.            [default: '']
  --p-aa-counts TEXT                                             [default: '']
Outputs:
  --o-nt-counts ARTIFACT FeatureTable[Frequency]
                                                                    [required]
  --o-aa-counts-o ARTIFACT FeatureTable[Frequency]
                                                                    [required]
Miscellaneous:
  --output-dir PATH       Output unspecified results to a directory
  --verbose / --quiet     Display verbose output to stdout and/or stderr
                          during execution of this action. Or silence output
                          if execution is successful (silence is golden).
  --citations             Show citations and exit.
  --help                  Show this message and exit.
```

#### Demux-paired
Demultiplex paired-end reads, where the second read can be either a file containing only
reverse indexes or reverse reads.
    
```
Usage: qiime pepsirf demux-paired [OPTIONS]

  Description

Inputs:
  --i-f-reads ARTIFACT MultiplexedSingleEndBarcodeInSequence
                          Input reads file to parse.                [required]
  --i-r-reads ARTIFACT MultiplexedSingleEndBarcodeInSequence
                          Input reverse reads file to parse. This file can
                          contain either just barcode reads or contain reverse
                          reads. Either way the expected position of the
                          reverse barcodes must be specified by the r-index
                          parameter.                                [required]
  --i-library ARTIFACT FeatureData[Sequence]
                          Designed library containing nucleic acidpeptides.
                          Library should be in fasta format and should contain
                          sequences thatwere used to design the sequences in
                          reads.                                    [required]
  --i-barcodes ARTIFACT FeatureData[Sequence]
                          Name of fasta file containing forward and
                          (potentially) reverse barcode sequences.  [required]
Parameters:
  --p-samplelist TEXT     A tab-delimited list of samples, one sample per
                          line. If the samples are already indexed by I2 only
                          the forward index (I1) and the sample name are
                          required. The first item in each tab-delimited line
                          is the forward (I1) index, the second (if included)
                          is the reverse (I2) index, and the third is
                          thesamplename.                            [required]
  --p-seq TEXT            Positional values for nucleotide sequence data.
                          This argument must be passed as 3 comma-separated
                          values. The first item represents the (0-based)
                          expected start index of the sequence. The second
                          represents the length of the sequence, and the third
                          represents the number of mismatches that are
                          tolerated for a sequence. An example is "--seq
                          43,90,2". This says that we start at (0-based) index
                          43, grab the next 90 characters, and if a perfect
                          match is not found for these grabbed characters we
                          look for a match to the designed library sequences
                          with up to two allowedmismatches.         [required]
  --p-f-index TEXT        Positional values for f-index. This argument must
                          be passed as 3 comma-separated values. The first
                          item represents the (0-based) expected start index
                          of the forward index. The second represents the
                          length of the forward index, and the third
                          represents the number of mismatches that are
                          tolerated for this index. An example is
                          "--f_index12,12,2". This says that we start at
                          (0-based) index 12, grab the next 12 characters, and
                          if a perfect match is not found for these grabbed
                          characters we look for a match to the forward
                          indexsequences with up to two allowed mismatches.
                                                                    [required]
  --p-r-index TEXT        Positional values for r-index. This argument must
                          be passed as 3 comma-separated values. The first
                          item represents the (0-based) expected start index
                          of the reverse index. The second represents the
                          length of the reverse index, and the third
                          represents the number of mismatches that are
                          tolerated for this index. An example is
                          "--r_index12,12,2". This says that we start at
                          (0-based) index 12, grab the next 12 characters, and
                          if a perfect match is not found for these grabbed
                          characters we look for a match to the reverse
                          indexsequences with up to two allowed mismatches.
                                                                 [default: '']
  --p-num-threads INTEGER The number of threads to use for analyses
                                                                  [default: 2]
  --p-read-per-loop INTEGER
                          The number of fastq records read a time.A higher
                          value will result in more memory usage by the
                          program, but will also result in fewer disk
                          accesses, increasing performance of the program.
                                                             [default: 800000]
  --p-concatemer TEXT     Concatenated primer sequences. If this concatemer
                          is found within a read, we know that a potential
                          sequence from the designed library was not included.
                          The number of times this concatemer is recorded in
                          the input file is reported.            [default: '']
  --p-aa-counts TEXT                                             [default: '']
Outputs:
  --o-nt-counts ARTIFACT FeatureTable[Frequency]
                                                                    [required]
  --o-aa-counts-o ARTIFACT FeatureTable[Frequency]
                                                                    [required]
Miscellaneous:
  --output-dir PATH       Output unspecified results to a directory
  --verbose / --quiet     Display verbose output to stdout and/or stderr
                          during execution of this action. Or silence output
                          if execution is successful (silence is golden).
  --citations             Show citations and exit.
  --help                  Show this message and exit.

```