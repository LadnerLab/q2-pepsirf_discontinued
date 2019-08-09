import csv

import qiime2.plugin.model as model
import numpy as np
from qiime2.plugin import ValidationError


class LinkedSpeciesPeptideFmt( model.TextFileFormat ):
    def _check_n_records( self, n ):
        with open( str( self ) ) as fh:
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
