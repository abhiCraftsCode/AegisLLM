#tier2:- onnx
import os
import numpy as np
import onnxruntime as ort
from transformers import AutoTokenizer
from typing import Tuple
from app.config import settings

class Tier2ONNXEngine:
    def __init__(self):
        self.tokenizer = None
        self.session = None
        self._load_engine()

    def _load_engine(self):
        model_path = settings.MODEL_PATH
        
        # Fallback to local model path check
        if not os.path.exists(model_path):
            print(f"[WARNING] ONNX model file not found at path: '{model_path}'. Tier 2 fallback mode active.")
            return

        print(f"[INFO] Initializing Tier 2 DeBERTa ONNX Engine from {model_path}...")
        
        # Load HuggingFace Tokenizer (Base DeBERTa-v3 tokenizer)
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/deberta-v3-small")
        
        # Initialize ONNX Execution Session with CPU Provider
        self.session = ort.InferenceSession(
            model_path,
            providers=["CPUExecutionProvider"]
        )
        print("[INFO] ONNX Session successfully loaded.")

    def predict(self, prompt: str) -> Tuple[bool, float]:
        """
        Runs tokenizer and ONNX neural model inference on input text.
        Returns: (is_threat: bool, threat_score: float)
        """
        if self.session is None or self.tokenizer is None:
            # Fallback safe response if model file is not present during early dev
            return False, 0.00

        # 1. Tokenize Input Text (Truncate to 512 max tokens)
        inputs = self.tokenizer(
            prompt,
            padding="max_length",
            truncation=True,
            max_length=512,
            return_tensors="np"
        )

        # Filter out input keys not expected by the DeBERTa ONNX graph
        input_names = [i.name for i in self.session.get_inputs()]
        onnx_inputs = {k: v for k, v in inputs.items() if k in input_names}

        outputs = self.session.run(None, onnx_inputs)
        # 4. Safely extract logits (Convert raw output to standard NumPy float array)
        raw_logits = np.asarray(outputs[0])
        logits = raw_logits[0] if raw_logits.ndim > 1 else raw_logits

        # 5. Apply Softmax Activation to get Threat Probability
        exp_logits = np.exp(logits - np.max(logits))
        probabilities = exp_logits / np.sum(exp_logits)
        
        # Index 1 represents Injection/Threat class
        threat_score = float(probabilities[1])
        is_threat = threat_score >= settings.THREAT_BLOCK_THRESHOLD

        return is_threat, round(threat_score, 4)

# Global Engine Instance Singleton
onnx_engine = Tier2ONNXEngine()