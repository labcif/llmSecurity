import logging
from typing import Any, Optional, Type

from pydantic import BaseModel, Field

from fuzzy.handlers.attacks.base import (BaseAttackTechniqueHandler,
                                         attack_handler_fm)
from fuzzy.handlers.attacks.enums import FuzzerAttackMode
from fuzzy.handlers.attacks.models import AttackResultEntry
from fuzzy.llm.providers.base import BaseLLMProvider

from fuzzy.handlers.attacks.videogame_roleplay.prompts_EN import (PROMPT_TEMPLATE_PREFIX, PROMPT_TEMPLATE_SUFIX)

from fuzzy.temperature import get_temperature
from fuzzy.top_p import get_top_p

logger = logging.getLogger(__name__)


#class PleaseAttackHandlerExtraParams(BaseModel):
#    add_prefix: bool = Field(True, description="Adds 'please' before the prompt. default: True")
#    add_suffix: bool = Field(True, description="Adds 'please' after the prompt. default: True")

@attack_handler_fm.flavor(FuzzerAttackMode.VIDEOGAME_ROLEPLAY)
class VideoGameAttackHandler(BaseAttackTechniqueHandler[BaseModel]):
    """
    Videogame roleplay attack handler - Modifies the input prompt by adding a roleplay videogame element prefix and suffix.
    """

    def __init__(self, **extra: Any):
        filtered_extra = {k: v for k, v in extra.items() if v is not None}
        super().__init__(**filtered_extra)

    async def _attack(self, prompt: str, **extra: Any) -> Optional[AttackResultEntry]:
        llm: BaseLLMProvider

        async with self._borrow(self._model) as llm:
            changed_prompt: str = prompt
            #if not self._extra_args.add_suffix and not self._extra_args.add_prefix:
            #    logger.warning("add_suffix and add_prefix are both false, nothing will be added to the prompt")
            #if self._extra_args.add_prefix:
            #    changed_prompt = f"Please {prompt}"
            #if self._extra_args.add_suffix:
            #    changed_prompt += ", please"

            changed_prompt = f"{PROMPT_TEMPLATE_PREFIX}{prompt}{PROMPT_TEMPLATE_SUFIX}"

            temp = get_temperature()
            top_p = get_top_p()

            if temp is not None and top_p is not None:
                response = await llm.generate(changed_prompt, temperature=temp, top_p=top_p, max_tokens=1000000)
            elif temp is not None and top_p is None:
                response = await llm.generate(changed_prompt, temperature=temp, max_tokens=1000000)
            elif temp is None and top_p is not None:
                response = await llm.generate(changed_prompt, top_p=top_p, max_tokens=1000000)
            else:
                response = await llm.generate(changed_prompt, max_tokens=1000000)
                
            result = AttackResultEntry(original_prompt=prompt,
                                       current_prompt=changed_prompt,
                                       response=response.response) if response else None
            logger.debug("Response: %s", response.response if response else "None")

        classifications = await self._classify_llm_response(response)

        if result:
            result.classifications = classifications
        return result

   # @classmethod
    #def extra_args_cls(cls) -> Type[BaseModel]:
    #    return PleaseAttackHandlerExtraParams