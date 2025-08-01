from typing import Any, Optional, Protocol

from fuzzy.handlers.attacks.models import AttackResultEntry, AttackSummary
from fuzzy.handlers.db.adv_prompts import AdversarialPromptDTO


class BaseAttackTechniqueHandlerProto(Protocol):
    @classmethod
    def extra_args(cls) -> dict[str, str] | None:
        """
        Get extra arguments for the attack handler.

        Returns:
            dict[str, str]: Extra arguments for the attack handler in the form of (arg, help)
        """
        ...

    async def attack(self, prompts: list[AdversarialPromptDTO]) -> Optional[AttackSummary]:
        """
        Perform the attack using the given prompt.

        Args:
            prompts (list[AdversarialPromptDTO]): Prompts to use for the attack.

        Returns:
            AttackResult: Adversarial prompts generated by the attack.
        """
        ...

    async def close(self) -> None:
        """
        Close the handler.
        """
        ...

    async def _attack(self, prompt: str, *args: Any, **extra: Any) -> Optional[AttackResultEntry]:
        """
        Perform the attack using the given prompt.

        Args:
            prompt (str): Prompt to use for the attack.
            extra (Any): Extra arguments for the attack.

        Returns:
            AttackResultEntry: Attack entry(ies) generated by the attack and the execution time 
        """
        ...

    def _generate_attack_params(self, prompts: list[AdversarialPromptDTO]) -> list[dict[str, Any]]:
        """
        Generate attack parameters. The dictionary must include the 'prompt' key with any additional 
        parameters required for each iteration of the attack.

        Args:
            prompts (list[AdversarialPromptDTO]): Prompts to use for the attack.

        Returns:
            list[dict[str, Any]]: Attack parameters.
        """
        ...

    async def _reduce_attack_params(self, entries: list[AttackResultEntry], 
                                    attack_params: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """
        Reduce attack parameters.

        Args:
            entires (list[AttackResultEntry]): Previous attack results for the givven attack_id.
            attack_params (list[dict[str, Any]]): Attack parameters to reduce.

        Returns:
            list[dict[str, Any]]: Reduced attack parameters.
        """
        ...
