from qiime2.plugin import SemanticType
from q2_types.feature_data import FeatureData
from q2_types.feature_table import FeatureTable

TaxIdLineage = SemanticType( 'TaxIdLineage' )

LinkedSpeciesPeptide = SemanticType( 'LinkedSpeciesPeptide' )

SequenceNames = SemanticType( 'SequenceNames' )

ProteinSequence = SemanticType( 'ProteinSequence',
                                variant_of = FeatureData.field[ 'type' ]
                              )

EnrichedPeptide = SemanticType( 'EnrichedPeptide' )

DeconvolutedSpecies = SemanticType( 'DeconvolutedSpecies',
                                variant_of = FeatureTable.field[ 'content' ]
                              )

