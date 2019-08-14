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
from ._format import TaxIdLineageFmt, TaxIdLineageDirFmt
from ._format import EnrichedPeptideFmt, EnrichedPeptideDirFmt
from ._format import DeconvolutedSpeciesFmt, DeconvolutedSpeciesDirFmt

import qiime2.plugin

def _run_cmd( cmd ):
    cmd = [ str( item ) for item in cmd ]
    return subprocess.check_output( cmd )

def _mutually_exclusive( *args ):
    curr = False
    for cond in args:
        curr = curr ^ cond
    return curr 

def _add_if( lis, cond, *items ):
    if cond:
        for it in items:
            lis.append( it )

def deconv( linked: LinkedSpeciesPeptideFmt,
            enriched: EnrichedPeptideFmt,
            threshold: qiime2.plugin.Int,
            single_threaded: qiime2.plugin.Bool = False,
            fractional_scoring: qiime2.plugin.Bool = False,
            summation_scoring: qiime2.plugin.Bool = False,
            score_filtering: qiime2.plugin.Bool = False,
            score_tie_threshold: qiime2.plugin.Float = 0.0,
            score_overlap_threshold: qiime2.plugin.Float = 1.0,
            id_name_map: TaxIdLineageFmt = None
          ) -> ( DeconvolutedSpeciesFmt ):

    cmd = [ 'pep_sirf',
            'deconv',
            '--enriched', str( enriched ),
            '--linked', str( linked ),
            '--threshold', threshold,
            '--score_tie_threshold', score_tie_threshold,
            '--score_overlap_threshold', score_overlap_threshold,
          ]
    output = DeconvolutedSpeciesFmt()
    
    if not _mutually_exclusive( fractional_scoring,
                                summation_scoring,
                                not( fractional_scoring    #represents integer scoring
                                     or summation_scoring
                                   )
                              ):
        raise ValueError( 'Either fractional_scoring, summation_scoring, '
                          'or neither must be included (Which means integer '
                          'scoring is used). You have provided '
                          'both fractional_scoring and summation_scoring.'
                        )
        
    _add_if( cmd, single_threaded, '--single_threaded' )
    _add_if( cmd, fractional_scoring, '--fractional_scoring' )
    _add_if( cmd, summation_scoring, '--summation_scoring' )
    _add_if( cmd, id_name_map != None, '--id_name_map', str( id_name_map ) )

    cmd += [ '--output', str( output ) ]
    print( _run_cmd( cmd ).decode( 'ascii' ) )
    return output

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
