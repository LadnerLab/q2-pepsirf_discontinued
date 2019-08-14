#!/usr/bin/env python3
import os
import tempfile
import subprocess
import gzip
import io
import shutil
from shutil import copyfile

import pandas as pd
from qiime2 import Metadata
from q2_types.feature_data import FeatureData, Sequence
from q2_types.feature_table import FeatureTable, Frequency
from q2_types.sample_data import SampleData
from q2_types.per_sample_sequences import ( Sequences, FastqGzFormat )
from q2_types.feature_data import DNAFASTAFormat
from q2_types.multiplexed_sequences import MultiplexedSingleEndBarcodeInSequenceDirFmt
from ._format import LinkedSpeciesPeptideFmt, LinkedSpeciesPeptideDirFmt
from ._format import SequenceNamesFmt, SequenceNamesDirFmt
from ._format import SequenceNamesFmt, SequenceNamesDirFmt
from ._format import ProteinSequenceFmt, ProteinSequenceDirFmt

import qiime2.plugin


def deconv( single_threaded: qiime2.plugin.Bool = False,
            fractional_scoring: qiime2.plugin.Bool = False,
            summation_scoring: qiime2.plugin.Bool = False,
            score_filtering: qiime2.plugin.Bool = False
          ) -> ( LinkedSpeciesPeptideFmt ):
    pass

def create_linkage( protein_file : ProteinSequenceFmt,
                    peptide_file: ProteinSequenceFmt,
                    single_threaded: qiime2.plugin.Bool,
                    kmer_size: qiime2.plugin.Int
                  ) -> ( LinkedSpeciesPeptideFmt ):
    out_dir = LinkedSpeciesPeptideFmt()
    with tempfile.NamedTemporaryFile() as protein_f:
        with tempfile.NamedTemporaryFile() as peptide_f:
            copyfile( str( protein_file ), protein_f.name )
            copyfile( str( peptide_file ), peptide_f.name )

            cmd = [ 'pep_sirf',
                    'deconv',
                    '--create_linkage',
                    '--protein_file', protein_f.name,
                    '--peptide_file', peptide_f.name,
                    '--output', str( out_dir ),
                    '--kmer_size', str( kmer_size )
                    ]
            if single_threaded:
                cmd += [ '--single_threaded' ]
            subprocess.check_output( cmd )
            

    return out_dir
