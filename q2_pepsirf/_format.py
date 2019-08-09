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
