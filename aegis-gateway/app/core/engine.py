import asyncio
from time import perf_counter
from dataclasses import dataclass
from abc import ABC,abstractmethod

from app.core.onnxEngine import ONNXEngine
from app.core.heuristicEngine import HeuristicEngine

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
    """base for inspect function/method"""
    pass

class AegisEngine(SecurityEngine):
  """our main engine that runs everything for inspection cycle."""
  def __init__(self) -> None:
    #either create these two here or take in parameter
    self.heuristic=HeuristicEngine()
    self.onnx=ONNXEngine()

  async def inspect(self, prompt: str) -> InspectionResult:
    """process the prompt through the two engines for threat analysis"""
    start=perf_counter()
    #tier1 heuristic scan 
    blocked,score,reason=(self.heuristic.scan(prompt))
    if blocked:
      latency=perf_counter()-start
      #early exit
      return InspectionResult(
        is_blocked=blocked,
        latency_ms=latency,
        threat_score=score,
        reason=reason
      )

    #tier2 model prediction and scoring
    blocked,score=await asyncio.to_thread(
      self.onnx.predict,
      prompt
    )
    latency=perf_counter()-start
    reason=("TIER_2_ONNX:THREAT" if blocked else "TIER_2_ONNX:SAFE")

    return InspectionResult(
      reason=reason,
      threat_score=score,
      is_blocked=blocked,
      latency_ms=latency
    )