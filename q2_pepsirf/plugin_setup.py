import importlib
import qiime2.plugin
import q2_pepsirf._demux
import q2_pepsirf._deconv
from q2_pepsirf._types import LinkedSpeciesPeptide, ProteinSequence
from q2_pepsirf._types import SequenceNames
from q2_pepsirf._format import LinkedSpeciesPeptideFmt, LinkedSpeciesPeptideDirFmt
from q2_pepsirf._format import SequenceNamesFmt, SequenceNamesDirFmt
from q2_pepsirf._format import ProteinSequenceFmt, ProteinSequenceDirFmt
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

plugin.register_formats( LinkedSpeciesPeptideFmt, LinkedSpeciesPeptideDirFmt,
                         SequenceNamesFmt, SequenceNamesDirFmt,
                         ProteinSequenceFmt, ProteinSequenceDirFmt
                       )
plugin.register_semantic_types( LinkedSpeciesPeptide, SequenceNames, ProteinSequence )
plugin.register_semantic_type_to_format( LinkedSpeciesPeptide,
                                         artifact_format = LinkedSpeciesPeptideDirFmt
                                       )
plugin.register_semantic_type_to_format( SequenceNames,
                                         artifact_format = SequenceNamesDirFmt
                                       )
plugin.register_semantic_type_to_format( FeatureData[ProteinSequence],
                                         artifact_format = ProteinSequenceDirFmt
                                       )

plugin.methods.register_function(
    function = q2_pepsirf._deconv.deconv,
    name = 'Perform species deconvolution on a list of enriched peptides.',
    description = (''),
    inputs = {},
    parameters = {
        'single_threaded': qiime2.plugin.Bool,
        'fractional_scoring': qiime2.plugin.Bool,
        'summation_scoring': qiime2.plugin.Bool,
        'score_filtering': qiime2.plugin.Bool,
        },

    outputs = [ ( 'noop', LinkedSpeciesPeptide ) ],
    input_descriptions = {},
    parameter_descriptions = { 'single_threaded': 'By default this module uses two '
                               'threads. Include this option with no '
                               'arguments if you only want  one thread '
                               'to be used.',

                               'fractional_scoring': 'Use fractional instead of integer '
                                                     'scoring. For integer scoring the score '
                                                     'of each species is defined by the '
                                                     'number of peptides that share a 7mer '
                                                     'with that species. For fractional '
                                                     'scoring the score of each species is '
                                                     'defined by 1/n for each peptide, where '
                                                     'n is the number of species a peptide '
                                                     'shares a 7mer with. In this method of '
                                                     'scoring peptides with fewer species are'
                                                     'worth more. Note that if neither this '
                                                     'flag nor --summation_scoring are '
                                                     'included, integer scoring will be used.'
                                                     'In integer scoring each species is '
                                                     'scored by the number of peptides it '
                                                     'shares a kmer with. ',

                               'summation_scoring': 'Include this flag (without any '
                                                    'arguments) if you want summation '
                                                    'scoring to be used instead of '
                                                    'fractional or integer scoring. For '
                                                    'summation scoring, the --linked file '
                                                    'passed must be of the form created by '
                                                    '--create_linkage. This means a file of '
                                                    'tab-delimited values, one per line. '
                                                    'Each line is of the form peptide_name '
                                                    'TAB id:score,id:score, and so on. '
                                                    'Undefined behavior will result if input'
                                                    'is not in this format. For summation '
                                                    'scoring, each species is scored based '
                                                    'on the number of kmers it shares with '
                                                    'each peptide with which it shares a '
                                                    'kmer.'
                                                     'For example, assume a line in the '
                                                    '--linked file looks like the following:'
                                                    ' peptide_1 TAB 123:4,543:8 '
                                                    'Both species "123" and "543" will '
                                                    'receive a score of 4 and 8 '
                                                    'respectively.Note that if neither this '
                                                    'flag nor --summation_scoring are '
                                                    'included, integer scoring will be used.'
                                                    'In integer scoring each species is '
                                                    'scored by the number of peptides it '
                                                    'shares a kmer with.',

                               'score_filtering': 'Include this flag if you want filtering '
                                                  'to be done by the score of each '
                                                  'species. Note that score is determined '
                                                  'by the different flags specifying how a'
                                                  'species should be scored. This means '
                                                  'that any species whose score falls '
                                                  'below --threshold will be removed from '
                                                  'consideration. Note that for integer '
                                                  'scoring, both score filtering and count'
                                                  'filtering are the same. If this flag is'
                                                  'not included, then any species whose '
                                                  'count falls below --threshold will be '
                                                  'removed from consideration. Score '
                                                  'filtering is best suited for the '
                                                  'summation scoring algorithm.'

                               
    },
    output_descriptions = { }
)

plugin.methods.register_function(
    function = q2_pepsirf._deconv.create_linkage,
    name = 'Create a linkage file for species deconvolution.',
    description = ( 'This command will create the file that '
                    'is used for species deconvolution. '
                    'This file will contain a header followed '
                    'one record per line. A record is a tab-delimited '
                    'line where the first entry is the name '
                    'of the peptide, and the second is a '
                    'comma-separated list of species ids where each entry '
                    'can be a colon-delimited pair with the first entry '
                    'as the species id, and the second is the number of kmers '
                    'the peptide shares with the species.'
    ),
    inputs = {
        'protein_file': FeatureData[ ProteinSequence ],
        'peptide_file': FeatureData[ ProteinSequence ]
        },
    parameters = {
        'single_threaded': qiime2.plugin.Bool,
        'kmer_size': qiime2.plugin.Int
        },
    outputs = [ ( 'linked', LinkedSpeciesPeptide ) ],
    input_descriptions = {
        'protein_file': 'Name of fasta file containing protein '
                        'sequences from which a design was '
                        'created.',
        'peptide_file': 'Name of fasta file containing amino acid '
                        'peptides that have been designed as '
                        'part of a library.'
    },
    parameter_descriptions = { 'single_threaded': 'By default this module uses two '
                               'threads. Include this option with no '
                               'arguments if you only want  one thread '
                               'to be used.'
    },
    output_descriptions    = { 'linked': 'output' }
)

plugin.methods.register_function( 
    function = q2_pepsirf._demux.demux, 
    inputs = {
        'library':     FeatureData[ Sequence ],
        'reads':       MultiplexedSingleEndBarcodeInSequence,
        'barcodes':    FeatureData[ Sequence ]
    },
    # TODO: Change index /seq location parameters
    parameters = { 'samplelist':     qiime2.plugin.Str,
                   'seq_location': qiime2.plugin.List[ qiime2.plugin.Int ],
                   'f_index_location': qiime2.plugin.List[ qiime2.plugin.Int ], 
                   'r_index_location': qiime2.plugin.List[ qiime2.plugin.Int ],
                   'read_per_loop': qiime2.plugin.Int,
                   'num_threads'  : qiime2.plugin.Int,
                   'concatemer'   :  qiime2.plugin.Str,
                   'aa_counts'    :  qiime2.plugin.Str
                 },
    outputs = [ ( 'nt_counts', FeatureTable[ Frequency ] ),
                ( 'aa_counts_o', FeatureTable[ Frequency ] )
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
                                              'reverse (I2) index, and the third is the '
                                              'sample name. ',

                               'f_index_location': 'Positional values for f_index. This '
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

                               'r_index_location': 'Positional values for r_index. This '
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

                               'seq_location': 'Positional values for nucleotide '
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
                   'concatemer'  :  qiime2.plugin.Str,
                    'aa_counts'  :  qiime2.plugin.Str
                 },
    outputs = [ ( 'nt_counts', FeatureTable[ Frequency ] ),
                ( 'aa_counts_o', FeatureTable[ Frequency ] )
              ],
    input_descriptions     = { 'library': 'Designed library containing nucleic acid'
                                          'peptides. Library should be in fasta '
                                          'format and should contain sequences that'
                                          'were used to design the sequences in reads.',
                               'f_reads':   'Input reads file to parse.',
                               'r_reads':   'Input reverse reads file to parse. '
                                            'This file can contain either just barcode reads '
                                            'or contain reverse reads. Either way the expected position '
                                            'of the reverse barcodes must be specified by the r_index parameter.',
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
