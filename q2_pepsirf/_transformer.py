from .plugin_setup import plugin
import skbio
from q2_types.feature_data import FeatureData
from ._format import LinkedSpeciesPeptideFmt
from ._format import SequenceNamesFmt
from ._format import ProteinSequenceFmt
import pandas as pd


def _read_fasta( path ):
    return skbio.read( path, format = 'fasta' )

def _fasta_to_series( ff ):
    data = {}

    for sequence in _read_fasta( str( ff ) ):
        id_ = sequence.Metadata[ 'id' ]

        if id_ in data:
            raise ValueError( 'FASTA Sequence names must be unique. The '
                              'following ID was included more than once: %s.'
                              % id_
                            )
        data[ id_ ] = sequence
    return pd.Series( data )
    
def _file_to_df( ff, index_col = 'Name' ):
    df = pd.read_csv( str( ff ), sep = '\t',
                      index_col = index_col
                    )
    return df

@plugin.register_transformer
def _1( ff: LinkedSpeciesPeptideFmt ) -> qiime2.Metadata:
    return qiime2.Metadata( _file_to_df( ff ) )

@plugin.register_transformer
def _2( ff: LinkedSpeciesPeptideFmt ) -> pd.DataFrame:
    return _file_to_df( ff ) 

@plugin.register_transformer
def _3( ff: SequenceNamesFmt ) -> pd.DataFrame:
    return _file_to_df( ff, index_col = 'Name' )

@plugin.register_transformer
def _4( ff: ProteinSequenceFmt ) -> pd.Series:
    return _file_to_df( ff, index_col = 'Name' )
