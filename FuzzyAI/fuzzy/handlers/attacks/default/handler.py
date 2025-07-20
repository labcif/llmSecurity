import logging
from typing import Any, Optional

from pydantic import BaseModel

from fuzzy.handlers.attacks.base import (BaseAttackTechniqueHandler,
                                         attack_handler_fm)
from fuzzy.handlers.attacks.enums import FuzzerAttackMode
from fuzzy.handlers.attacks.models import AttackResultEntry
from fuzzy.llm.providers.base import BaseLLMProvider

from fuzzy.temperature import get_temperature
from fuzzy.top_p import get_top_p

logger = logging.getLogger(__name__)

@attack_handler_fm.flavor(FuzzerAttackMode.DEFAULT)
class DefaultAttackHandler(BaseAttackTechniqueHandler[BaseModel]):
    """
    Default attack handler - just generates the prompt as is.
    """
    def __init__(self, **extra: Any):
        filtered_extra = {k: v for k, v in extra.items() if v is not None}
        super().__init__(**filtered_extra)

    async def _attack(self, prompt: str, **extra: Any) -> Optional[AttackResultEntry]:
        result: Optional[AttackResultEntry] = None
        llm: BaseLLMProvider
        classifications: dict[str, Any] = {}

        async with self._borrow(self._model) as llm:
            
            # logger.debug("Generating response for prompt: %s", adv_prompt)
            #logger.info({get_temperature(),get_top_p()})
            
            temp = get_temperature()
            top_p = get_top_p()

            if temp is not None and top_p is not None:
                response = await llm.generate(prompt, temperature=temp, top_p=top_p, max_tokens=1000000)
            elif temp is not None and top_p is None:
                response = await llm.generate(prompt, temperature=temp, max_tokens=1000000)
            elif temp is None and top_p is not None:
                response = await llm.generate(prompt, top_p=top_p, max_tokens=1000000)
            else:
                response = await llm.generate(prompt, max_tokens=1000000)
            #response = await llm.generate(prompt,temperature=1.0, top_p=1.0)
            #response = await llm.generate(prompt)
            result = AttackResultEntry(original_prompt=prompt,
                                       current_prompt=prompt, 
                                       response=response.response) if response else None
            logger.debug("Response: %s", response.response if response else "None")
            
        classifications = await self._classify_llm_response(response, original_prompt=prompt)
        
        if result:
            result.classifications = classifications

        return result
