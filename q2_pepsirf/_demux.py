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
           samplelist: qiime2.plugin.Str
         ) -> ( pd.DataFrame, pd.DataFrame  ):
    print( "Hello everybody" )

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
            # '--input_r1', str( reads.file.view( FastqGzFormat ) ),
            '--input_r1', temp_in.name,
            '--f_index', "12,12,0",
            '--r_index', "112,8,0",
            '--seq', '43,45,0',
            '--library', str( library ),
            '--read_per_loop', '800000',
            '--aa_counts', aa_count_out.name,
            '--output', tsv_count_out.name,
            '--samplelist', samplelist,
            '--index', str( sample_seqs )
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
