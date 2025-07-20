import json
import logging
from typing import Any

from fuzzy.handlers.attacks.base import attack_handler_fm
from fuzzy.handlers.attacks.enums import FuzzerAttackMode
from fuzzy.handlers.attacks.taxonomy.handler_EN import TaxonomyParaphraser

logger = logging.getLogger(__name__)

DEFAULT_TAXONOMY_MODEL = "openai/gpt-4o"

@attack_handler_fm.flavor(FuzzerAttackMode.HISTORY_FRAMING)
class HistoryFramingAttackHandler(TaxonomyParaphraser):
    """
    History framing attack technique
    """
    def __init__(self, **extra: Any) -> None:
        filtered_extra = {k: v for k, v in extra.items() if v is not None}
        super().__init__(**filtered_extra)

        self._extra_args.taxonomy_model = DEFAULT_TAXONOMY_MODEL

    def _load_taxonomy_dataset(self) -> None:
        with open('resources/persuasion_taxonomy.jsonl', 'r') as f:
            data = f.read()

        self._taxonomies = [json.loads(jline) for jline in data.splitlines()][:1]
    
    @classmethod
    def default_auxiliary_models(cls) -> list[str]:
        return [DEFAULT_TAXONOMY_MODEL]

        