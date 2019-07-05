#!/usr/bin/env python3
import os
import tempfile
import subprocess
import gzip
import shutil

import pandas as pd
from qiime2 import Metadata
from q2_types.feature_data import FeatureData, Sequence
from q2_types.feature_table import FeatureTable, Frequency
from q2_types.sample_data import SampleData
from q2_types.per_sample_sequences import ( Sequences, FastqGzFormat )
from q2_types.feature_data import DNAFASTAFormat
from q2_types.multiplexed_sequences import MultiplexedSingleEndBarcodeInSequenceDirFmt
from q2_types.multiplexed_sequences import MultiplexedSingleEndBarcodeInSequenceDirFmt
import qiime2.plugin

def demux( reads: MultiplexedSingleEndBarcodeInSequenceDirFmt,
           library: DNAFASTAFormat,
           sample_seqs: DNAFASTAFormat,
           samplelist: qiime2.plugin.Str,
           f_index: qiime2.plugin.Str,
           r_index: qiime2.plugin.Str,
           seq:     qiime2.plugin.Str,
           num_threads: qiime2.plugin.Int,
           read_per_loop: qiime2.plugin.Int
         ) -> ( pd.DataFrame, pd.DataFrame  ):
    aa_counts  = DNAFASTAFormat
    tsv_counts = DNAFASTAFormat

    aa_count_out  = tempfile.NamedTemporaryFile( mode = 'w+' )
    tsv_count_out = tempfile.NamedTemporaryFile( mode = 'w+' )

    with gzip.open( str( reads.file.view( FastqGzFormat ) ), 'rb' ) as zip_file:
        temp_in  = tempfile.NamedTemporaryFile( mode = 'wb' )
        shutil.copyfileobj( zip_file, temp_in )
        # flush the file buffer to ensure the whole unzipped file is written
        temp_in.flush() 

    cmd = [ 'pep_sirf',
            'demux',
            '--input_r1', temp_in.name,
            '--f_index', f_index,
            '--r_index', r_index,
            '--seq',     seq,
            '--library', str( library ),
            '--read_per_loop', str( read_per_loop ),
            '--aa_counts', aa_count_out.name,
            '--output', tsv_count_out.name,
            '--samplelist', samplelist,
            '--index', str( sample_seqs ),
            '--num_threads', str( num_threads )
            ]

    print( subprocess.check_output( cmd ).decode( 'ascii' ) ) 

    temp_in.close()
    one = pd.read_csv( tsv_count_out.name, sep = '\t', index_col = 'Sequence name' )
    two = pd.read_csv( aa_count_out.name,  sep = '\t', index_col = 'Sequence name' )
    print( one )
    print( two )

    aa_count_out.close()
    tsv_count_out.close()

    return one, two
