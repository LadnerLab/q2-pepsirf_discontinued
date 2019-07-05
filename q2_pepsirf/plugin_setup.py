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
    website = 'https://github.com/LadnerLab/q2-pepsirf',
    package = 'q2_pepsirf',
    user_support_text = None,
    short_description = 'Plugin for pepsirf.',
    description = ( 'This QIIME2 plugin wraps pep_sirf, '
                    'where each module in pep_sirf has at least '
                    'command. To get specific information about each '
                    'module and its commands.'
                  ),
    citations = None
)

plugin.methods.register_function( 
    function = q2_pepsirf._demux.demux, 
    inputs = {
        'library':     FeatureData[ Sequence ],
        'reads':       MultiplexedSingleEndBarcodeInSequence,
        'barcodes':    FeatureData[ Sequence ]
    },
    parameters = { 'samplelist':     qiime2.plugin.Str,
                    'f_index':       qiime2.plugin.Str,
                    'r_index':       qiime2.plugin.Str,
                    'seq':           qiime2.plugin.Str,
                    'read_per_loop': qiime2.plugin.Int,
                    'num_threads'  : qiime2.plugin.Int,
                    'concatemer'  :  qiime2.plugin.Str
                 },
    outputs = [ ( 'nt_counts', FeatureTable[ Frequency ] ),
                ( 'aa_counts', FeatureTable[ Frequency ] )
              ],
    input_descriptions     = { 'library': 'Designed library containing nucleic acid'
                                          'peptides. Library should be in fasta '
                                          'format and should contain sequences that'
                                          'were used to design the sequences in reads.',
                               'reads':   'Input reads file to parse. These should be '
                                          'in fastq format. Reads can already be indexed on '
                                          'the reverse barcode sequences, in which case the '
                                          'r_index parameter should not be specified. If the '
                                          'reverse barcodes are in the reads the r_index parameter '
                                          'should be specified. If you have one file for forward reads '
                                          'and one for reverse reads the demux_paired command '
                                          'should be used.',
                               'barcodes':  'Name of fasta file containing forward '
                                            'and (potentially) reverse barcode '
                                            'sequences.'
                             },
    parameter_descriptions = { 'samplelist': 'A tab-delimited list of samples, one '
                                              'sample per line. If the samples are '
                                              'already indexed by I2 only the forward '
                                              'index (I1) and the sample name are '
                                              'required. The first item in each '
                                              'tab-delimited line is the forward (I1) '
                                              'index, the second (if included) is the '
                                              'reverse (I2) index, and the third is the'
                                              'samplename. ',

                               'f_index': 'Positional values for f_index. This '
                                           'argument must be passed as 3 '
                                           'comma-separated values. The first item '
                                           'represents the (0-based) expected start '
                                           'index of the forward index. The second '
                                           'represents the length of the forward '
                                           'index, and the third represents the '
                                           'number of mismatches that are tolerated '
                                           'for this index. An example is "--f_index'
                                           '12,12,2". This says that we start at '
                                           '(0-based) index 12, grab the next 12 '
                                           'characters, and if a perfect match is '
                                           'not found for these grabbed characters '
                                           'we look for a match to the forward index'
                                           'sequences with up to two allowed '
                                           'mismatches.',

                               'r_index': 'Positional values for r_index. This '
                                          'argument must be passed as 3 '
                                           'comma-separated values. The first item '
                                           'represents the (0-based) expected start '
                                           'index of the reverse index. The second '
                                           'represents the length of the reverse '
                                           'index, and the third represents the '
                                           'number of mismatches that are tolerated '
                                           'for this index. An example is "--r_index'
                                           '12,12,2". This says that we start at '
                                           '(0-based) index 12, grab the next 12 '
                                           'characters, and if a perfect match is '
                                           'not found for these grabbed characters '
                                           'we look for a match to the reverse index'
                                           'sequences with up to two allowed '
                                           'mismatches.',

                               'seq': 'Positional values for nucleotide '
                                       'sequence data. This argument must be '
                                       'passed as 3 comma-separated values. The '
                                       'first item represents the (0-based) '
                                       'expected start index of the sequence. '
                                       'The second represents the length of the '
                                       'sequence, and the third represents the '
                                       'number of mismatches that are tolerated '
                                       'for a sequence. An example is "--seq '
                                       '43,90,2". This says that we start at '
                                       '(0-based) index 43, grab the next 90 '
                                       'characters, and if a perfect match is '
                                       'not found for these grabbed characters '
                                       'we look for a match to the designed '
                                       'library sequences with up to two allowed'
                                       'mismatches.',

                               'read_per_loop': 'The number of fastq records read a time.'
                                                'A higher value will result in more '
                                                'memory usage by the program, but will '
                                                'also result in fewer disk accesses, '
                                                'increasing performance of the program.',
                               'concatemer': 'Concatenated primer sequences. If this '
                                             'concatemer is found within a read, we '
                                             'know that a potential sequence from the '
                                             'designed library was not included. The '
                                             'number of times this concatemer is '
                                             'recorded in the input file is reported.',
                               'num_threads': 'The number of threads to use for analyses'
                             },
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
                    'barcodes':    FeatureData[ Sequence ]
              },
    parameters = { 'samplelist':     qiime2.plugin.Str,
                   'f_index':       qiime2.plugin.Str,
                   'r_index':       qiime2.plugin.Str,
                   'seq':           qiime2.plugin.Str,
                   'read_per_loop': qiime2.plugin.Int,
                   'num_threads'  : qiime2.plugin.Int,
                   'concatemer'  :  qiime2.plugin.Str
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
