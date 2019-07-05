import importlib
import qiime2.plugin
import q2_pepsirf._demux
from q2_types.feature_data import FeatureData, Sequence
from q2_types.feature_table import FeatureTable, Frequency
from q2_types.sample_data import SampleData
from q2_types.per_sample_sequences import Sequences
from q2_types.multiplexed_sequences import MultiplexedSingleEndBarcodeInSequence

plugin = qiime2.plugin.Plugin( 
    name = 'pepsirf',
    version = q2_pepsirf.__version__,
    website = '',
    package = 'q2_pepsirf',
    user_support_text = None,
    short_description = 'Plugin for pepsirf.',
    description = ( 'Plugin for pepsirf.' ),
    citations = None
)

plugin.methods.register_function( 
    function = q2_pepsirf._demux.demux, 
    inputs = {
        'library':     FeatureData[ Sequence ],
        'reads':       MultiplexedSingleEndBarcodeInSequence,
        'sample_seqs': FeatureData[ Sequence ]
    },
    parameters = { 'samplelist':     qiime2.plugin.Str,
                    'f_index':       qiime2.plugin.Str,
                    'r_index':       qiime2.plugin.Str,
                    'seq':           qiime2.plugin.Str,
                    'read_per_loop': qiime2.plugin.Int,
                    'num_threads'  : qiime2.plugin.Int
                 },
    outputs = [ ( 'nt_counts', FeatureTable[ Frequency ] ),
                ( 'aa_counts', FeatureTable[ Frequency ] )
              ],
    input_descriptions     = {},
    parameter_descriptions = {},
    output_descriptions    = {},
    name = 'PepSIRF Demux',
    description = ( 'Description' )
    
    )

plugin.methods.register_function( 
    function = q2_pepsirf._demux.demux_paired, 
    inputs = {
        'library':     FeatureData[ Sequence ],
        'f_reads':     MultiplexedSingleEndBarcodeInSequence,
        'r_reads':     MultiplexedSingleEndBarcodeInSequence,
        'sample_seqs': FeatureData[ Sequence ]
    },
    parameters = { 'samplelist':     qiime2.plugin.Str,
                    'f_index':       qiime2.plugin.Str,
                    'r_index':       qiime2.plugin.Str,
                    'seq':           qiime2.plugin.Str,
                    'read_per_loop': qiime2.plugin.Int,
                    'num_threads'  : qiime2.plugin.Int
                 },
    outputs = [ ( 'nt_counts', FeatureTable[ Frequency ] ),
                ( 'aa_counts', FeatureTable[ Frequency ] )
              ],
    input_descriptions     = {},
    parameter_descriptions = {},
    output_descriptions    = {},
    name = 'PepSIRF Demux',
    description = ( 'Description' )
    
    )
