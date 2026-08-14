import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

def generate_local_onnx():
    print("Loading base DistilBERT weights from Hugging Face...")
    model_name = "distilbert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
    model.eval()

    dummy_text = "Test prompt for ONNX tracing."
    inputs = tokenizer(
        dummy_text,
        return_tensors="pt",
        padding="max_length",
        max_length=128,
        truncation=True
    )

    print("Exporting to aegis_model.onnx...")
    torch.onnx.export(
        model,
        (inputs["input_ids"], inputs["attention_mask"]),
        "aegis_model.onnx",
        input_names=["input_ids", "attention_mask"],
        output_names=["logits"],
        dynamic_axes={
            "input_ids": {0: "batch_size", 1: "sequence"},
            "attention_mask": {0: "batch_size", 1: "sequence"}
        },
        opset_version=14,
        dynamo=False  # Ensures stable, legacy tracing
    )
    print("SUCCESS: 'aegis_model.onnx' created in your workspace!")

if __name__ == "__main__":
    generate_local_onnx()