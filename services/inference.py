import time
import torch
import numpy as np
import onnxruntime as ort
from transformers import AutoTokenizer
from pydantic import BaseModel

class ThreatResult(BaseModel):
    threat_score: float
    is_malicious: bool
    latency_ms: float

class AegisInferencePipeline:
    def __init__(self, model_path: str = "aegis_model.onnx", model_name: str = "distilbert-base-uncased"):
        print(f"Loading Tokenizer ({model_name}) & ONNX Runtime Session...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # Configure hardware-accelerated CPU session
        sess_options = ort.SessionOptions()
        sess_options.intra_op_num_threads = 2
        sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        self.session = ort.InferenceSession(model_path, sess_options=sess_options, providers=['CPUExecutionProvider'])

    def preprocess(self, text: str) -> dict:
        encoded = self.tokenizer(
            text,
            return_tensors="np",
            padding="max_length",
            max_length=128,
            truncation=True
        )
        return {
            "input_ids": encoded["input_ids"].astype("int64"),
            "attention_mask": encoded["attention_mask"].astype("int64")
        }

    def run_inference(self, inputs: dict) -> np.ndarray:
        return self.session.run(None, inputs)[0]

    def postprocess(self, logits: np.ndarray) -> float:
        tensor_logits = torch.from_numpy(logits)
        probs = torch.softmax(tensor_logits, dim=-1)
        return round(float(probs[0][1]), 4)

    def predict(self, text: str, threshold: float = 0.80) -> ThreatResult:
        start_time = time.time()
        inputs = self.preprocess(text)
        logits = self.run_inference(inputs)
        score = self.postprocess(logits)
        latency = round((time.time() - start_time) * 1000, 2)
        
        return ThreatResult(
            threat_score=score,
            is_malicious=(score >= threshold),
            latency_ms=latency
        )