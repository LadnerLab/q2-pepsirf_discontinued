from qiime2.plugin import SemanticType
from q2_types.feature_data import FeatureData

LinkedSpeciesPeptide = SemanticType( 'LinkedSpeciesPeptide' )
SequenceNames = SemanticType( 'SequenceNames' )
ProteinSequence = SemanticType( 'ProteinSequence',
                                variant_of = FeatureData.field[ 'type']
                              )
