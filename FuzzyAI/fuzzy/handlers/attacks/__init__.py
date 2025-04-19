from .artprompt.handler import ArtPromptAttackHandler
from .default.handler import DefaultAttackHandler
from .genetic.handler import GeneticAttackTechniqueHandler
from .gpt_fuzzer.handler import GPTFuzzerAttackHandler
from .history_framing.handler import HistoryFramingAttackHandler
from .please.handler import PleaseAttackHandler

# the attacks bellow are the ones we are focusing because we are using them in our automatation script

from .shuffle_inconsistency.handler import ShuffleInconsistencyAttackHandler
from .bon.handler import BonAttackHandler
from .ascii_smuggling.handler import AsciiSmugglingAttackHandler
from .actor_attack.handler import ActorAttackHandler
from .piglatin.handler import PigLatinAttackHandler

# loads all english handlers first to avoid erros 
# then if language is set to another value loads specific language handlers with the function bellow 

from .thought_experiment.handler_EN import ThoughtExperimentAttackHandler
from .dan.handler_EN import DanAttackHandler
from .word_game.handler_EN import WordGameAttackHandler
from .taxonomy.handler_EN import TaxonomyParaphraser
from .hallucinations.handler_EN import HallucinationsAttackHandler
from .paraphraser.handler_EN import PresuasiveParaphraser
from .back_to_the_past.handler_EN import BackToThePastAttackHandler
from .manyshot.handler_EN import ManyShotAttackHandler
from .crescendo.handler_EN import CrescendoAttackHandler

def load_language_specific_handlers():
    from fuzzy.language import get_language
    language = get_language()

    if language == 'pt':
        from .dan.handler_PT import DanAttackHandler 
        from .word_game.handler_PT import WordGameAttackHandler 
        from .thought_experiment.handler_PT import ThoughtExperimentAttackHandler
        from .taxonomy.handler_PT import TaxonomyParaphraser
        from .hallucinations.handler_PT import HallucinationsAttackHandler
        from .paraphraser.handler_PT import PresuasiveParaphraser
        from .back_to_the_past.handler_PT import BackToThePastAttackHandler
        from .manyshot.handler_PT import ManyShotAttackHandler
        from .crescendo.handler_PT import CrescendoAttackHandler
    else:
        raise ValueError(f"Language not supported: {language}")
