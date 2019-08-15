import csv

import qiime2.plugin.model as model
import numpy as np
from qiime2.plugin import ValidationError

class LinkedSpeciesPeptideFmt( model.TextFileFormat ):
    def _check_n_records( self, n ):
        with open( str( self ), 'r' ) as fh:
            csv_reader = csv.reader( fh, delimiter = '\t' )

            for i, row in enumerate( csv_reader ):
                if i == n:
                    break
                else:
                    if len( row ) != 2:
                        raise ValidationError( 'Incorrect number of fields detected on line %d. '
                                               'Should be exactly 2.' % ( i + 1 )
                                             )

    def _validate_( self, level ):
        record_count_map = { 'min': 5, 'max': np.inf }
        self._check_n_records( record_count_map[ level ] )

LinkedSpeciesPeptideDirFmt = model.SingleFileDirectoryFormat( 'LinkedSpeciesPeptideDirFmt',
                                                              'linked.tsv',
                                                              LinkedSpeciesPeptideFmt
                                                            )

class SequenceNamesFmt( model.TextFileFormat ):
    def _check_n_records( self, n ):
        with open( str( self ), 'r' ) as fh:
            for lineno, record in enumerate( fh ):
                if lineno == n:
                    break
                else:
                    if len( record.strip() ) == 0:
                        raise ValidationError( 'Error on line %d, '
                                               'empty lines are not permitted.' % ( lineno + 1 )
                                             )

    def _validate_( self, level ):
        record_count_map = { 'min': 5, 'max': np.inf }
        self._check_n_records( record_count_map[ level ] )

SequenceNamesDirFmt = model.SingleFileDirectoryFormat( 'SequenceNamesDirFmt',
                                                       'names.txt',
                                                       SequenceNamesFmt
                                                     )

class ProteinSequenceFmt( model.TextFileFormat ):
    def _check_n_records( self, n ):
        last_was_id = False
        non_id_lines = 0

        with open( str( self ), 'r'  ) as fh:
            for lineno, line in enumerate( fh ):
                if line[ 0 ] == '>':
                    if last_was_id:
                        raise ValueError( 'Two sequence names were found in a row, '
                                          'error on line %d.' % ( lineno + 1 )
                                        )
                    last_was_id = True
                else:
                    last_was_id = False
                    non_id_lines += 1
                        
                if lineno >= n:
                    if non_id_lines: # there is at least one name and one sequence
                        break
                    raise ValueError( 'Fasta File does not contain at least one '
                                      'name and one sequence.'
                                    )

                    

    def _validate_( self, level ):
        record_count_map = { 'min': 5, 'max': np.inf }
        self._check_n_records( record_count_map[ level ] )
        
ProteinSequenceDirFmt = model.SingleFileDirectoryFormat( 'ProteinSequenceDirFmt',
                                                         'sequences.fasta',
                                                         ProteinSequenceFmt
                                                       )

class TaxIdLineageFmt( model.TextFileFormat ):
    def _check_n_records( self, n ):
        with open( str( self ), 'r' ) as of:
            for lineno, line in enumerate( of ):
                if lineno == n:
                    return True

                else:
                    spl = line.split( '|' )
                    if len( spl ) == 0:
                        raise ValueError( 'Error on line %d: '
                                          'TaxIdLineage file must have one or more '
                                          'values separated by the "|" delimiter.' % ( lineno + 1 )
                                        )
                    try:
                        id = int( spl[ 0 ].strip() )
                    except:
                        raise ValueError( 'Error on line %d: '
                                          'The first item in each line must be '
                                          'the id for a species.' % ( lineno + 1 )
                                        )

    def _validate_( self, level ):
        record_count_map = { 'min': 5, 'max': np.inf }
        self._check_n_records( record_count_map[ level ] )

TaxIdLineageDirFmt = model.SingleFileDirectoryFormat( 'TaxIdLineageDirFmt',
                                                      'lineage.dmp',
                                                      TaxIdLineageFmt
                                                    )

class EnrichedPeptideFmt( model.TextFileFormat ):
    def _check_n_records( self, n ):
        with open( str( self ), 'r' ) as of:
            for lineno, line in enumerate( of ):
                if lineno == n:
                    break
                if len( line.strip() ) == 0:
                    raise ValueError( 'Error on line %d: '
                                      'Enriched peptide file must'
                                      'contain one name per line!'
                                      % ( lineno + 1 )
                                    )

    def _validate_( self, level ):
        record_count_map = { 'min': 5, 'max': np.inf }
        self._check_n_records( record_count_map[ level ] )

EnrichedPeptideDirFmt = model.SingleFileDirectoryFormat( 'EnrichedPeptideDirFmt',
                                                         'peptides.txt',
                                                         EnrichedPeptideFmt
                                                       )

class DeconvolutedSpeciesFmt( model.TextFileFormat ):
    def _check_n_records( self, n ):
        pass

    def _validate_( self, level ):
        record_count_map = { 'min': 5, 'max': np.inf }
        self._check_n_records( record_count_map[ level ] )
        
DeconvolutedSpeciesDirFmt = model.SingleFileDirectoryFormat( 'DeconvolutedSpeciesDirFmt',
                                                             'deconv_species.tsv',
                                                             DeconvolutedSpeciesFmt
                                                           )

class SpeciesAssignMapFmt( model.TextFileFormat ):
    def _check_n_records( self, n ):
        pass

    def _validate_( self, level ):
        record_count_map = { 'min': 5, 'max': np.inf }
        self._check_n_records( record_count_map[ level ] )

SpeciesAssignMapDirFmt = model.SingleFileDirectoryFormat( 'SpeciesAssignMapDirFmt',
                                                          'species_peptide_assignments.tsv',
                                                          SpeciesAssignMapFmt
                                                        )        
