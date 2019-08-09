from .plugin_setup import plugin
from ._format import LinkedSpeciesPeptideFmt
from ._format import SequenceNamesFmt
import pandaas as pd


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
