import os
import numpy as np
import onnxruntime as ort
from transformers import AutoTokenizer

from app.core.config import settings
from app.core.exceptions import ModelNotFoundError


class ONNXEngine:
  """tier 2 onnx serach engine"""
  def __init__(self):
    """intializes the engine's tokenizer and session"""
    model_path = settings.MODEL_PATH
    # check for model presence
    if not os.path.exists(model_path):
      raise ModelNotFoundError()

    self.tokenizer = AutoTokenizer.from_pretrained(
      "microsoft/deberta-v3-small"
    )

    self.session = ort.InferenceSession(
      model_path,
      providers=["CPUExecutionProvider"],
    )

  def predict(self, prompt: str) -> tuple[bool, float]:
    """prompt scoring for inspection"""
    inputs = self.tokenizer(
      prompt,
      padding="max_length",
      truncation=True,
      max_length=512,
      return_tensors="np",
    )

    input_names = [
      input_.name for input_ in self.session.get_inputs()
    ]

    onnx_inputs = {
      key: value
      for key, value in inputs.items()
      if key in input_names
    }

    outputs = self.session.run(
      None,
      onnx_inputs,
    )

    raw_logits = np.asarray(outputs[0])

    logits = (
      raw_logits[0]
      if raw_logits.ndim > 1
      else raw_logits
    )

    exp_logits = np.exp(
      logits - np.max(logits)
    )

    probabilities = (
      exp_logits / np.sum(exp_logits)
    )

    threat_score = float(
      probabilities[1]
    )

    is_threat = (
      threat_score >= settings.THREAT_BLOCK_THRESHOLD
    )

    return (is_threat,round(threat_score, 4))