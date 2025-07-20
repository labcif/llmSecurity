import logging
from typing import Any, Optional

from pydantic import BaseModel

from fuzzy.handlers.attacks.base import (BaseAttackTechniqueHandler,
                                         attack_handler_fm)
from fuzzy.handlers.attacks.enums import FuzzerAttackMode
from fuzzy.handlers.attacks.hallucinations.prompt_PT import PROMPT_TEMPLATE
from fuzzy.handlers.attacks.models import AttackResultEntry
from fuzzy.handlers.db.adv_prompts import AdversarialPromptDTO
from fuzzy.llm.providers.base import BaseLLMMessage, BaseLLMProvider

from fuzzy.temperature import get_temperature
from fuzzy.top_p import get_top_p

logger = logging.getLogger(__name__)

@attack_handler_fm.flavor(FuzzerAttackMode.HALLUCINATIONS)
class HallucinationsAttackHandler(BaseAttackTechniqueHandler[BaseModel]):
    """
    Hallucinations attack technique (https://arxiv.org/pdf/2403.04769.pdf)
    """
    def __init__(self, **extra: Any):
        filtered_extra = {k: v for k, v in extra.items() if v is not None}
        super().__init__(**filtered_extra)
        
    def _generate_attack_params(self, prompts: list[AdversarialPromptDTO]) -> list[dict[str, Any]]:
        return [{"prompt": prompt.prompt} for prompt in prompts]

    async def _reduce_attack_params(self, entries: list[AttackResultEntry], 
                                    attack_params: list[dict[str, Any]]) -> list[dict[str, Any]]:
        
        updated_params = [param for param in attack_params
                            if not any(entry.original_prompt == param['prompt']
                                for entry in entries)]
        
        return updated_params
    
    async def _attack(self, prompt: str, **extra: Any) -> Optional[AttackResultEntry]:
        result: Optional[AttackResultEntry] = None
        llm: BaseLLMProvider
        classifications: dict[str, Any] = {}

        async with self._borrow(self._model) as llm:
            logger.debug("Generating response for prompt: %s", prompt)
            reversed_prompt: str = prompt.upper()[::-1]
            target = " ".join([x.upper() for x in prompt.split(" ")[:2]])
            full_template = PROMPT_TEMPLATE.format(goal=reversed_prompt, target=target)
            logger.debug("Generated template: %s", full_template)
            messages = [
                BaseLLMMessage(role="user", content=full_template),
            ]

            temp = get_temperature()
            top_p = get_top_p()

            if temp is not None and top_p is not None:
                response = await llm.chat(messages, temperature=temp, top_p=top_p, max_tokens=1000000)
            elif temp is not None and top_p is None:
                response = await llm.chat(messages, temperature=temp, max_tokens=1000000)
            elif temp is None and top_p is not None:
                response = await llm.chat(messages, top_p=top_p, max_tokens=1000000)
            else:
                response = await llm.chat(messages, max_tokens=1000000)
            
            result = AttackResultEntry(original_prompt=prompt,
                                       current_prompt=full_template, 
                                       response=response.response) if response else None
            logger.debug("Response: %s", response.response if response else "None")
            
        classifications = await self._classify_llm_response(response, original_prompt=prompt)
        
        if result:
            result.classifications = classifications

        return result
            
