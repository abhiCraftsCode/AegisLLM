import os
import numpy as np
import onnxruntime as ort
from transformers import AutoTokenizer
from huggingface_hub import hf_hub_download

from app.core.config import settings


class ONNXEngine:
  """tier 2 onnx serach engine"""
  def __init__(self):
    """intializes the engine's tokenizer and session"""
    model_path = settings.LOCAL_MODEL_PATH
    # check for model presence
    if model_path is not None and os.path.exists(model_path):
      #model present locally
      print(f"[ONNXEngine] Using local model path: {model_path}")
    else:
      #model not present locally downloadig from hugging face
      repo_id=settings.HF_REPO_ID
      print(f"[ONNXEngine] Resolving model from Hugging Face Hub: {repo_id}")
      model_path=hf_hub_download(
        repo_id=repo_id,
        filename=settings.HF_MODEL_NAME
      )
      print(f"[ONNXEngine] Model resolved at cache path: {model_path}")
    #or we can direclty fetch from huggingface removing the local model check/dependency
    #alwayse create my own local model
    
    self.tokenizer = AutoTokenizer.from_pretrained(
      "microsoft/deberta-v3-small"
    )
    print(f"[ONNXEngine] creating session for engine.")
    self.session = ort.InferenceSession(
      model_path,
      providers=["CPUExecutionProvider"],
    )
    print(f"[ONNXEngine] successfully created session for engine.")

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