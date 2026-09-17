from dataclasses import dataclass
from abc import ABC,abstractmethod

@dataclass
class InspectionResult:
    is_blocked: bool
    threat_score: float
    reason: str
    latency_ms: float


class SecurityEngine(ABC):
    """interface for prompt security inspection"""

    @abstractmethod
    async def inspect(self, prompt: str) -> InspectionResult:
        raise NotImplementedError

