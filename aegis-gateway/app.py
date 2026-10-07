import gradio as gr
from app.main import app as fastapi_app

# Minimal status view rendered on the root page
with gr.Blocks(title="Aegis Gateway") as demo:
    gr.Markdown("# 🛡️ Aegis Gateway is Live")
    gr.Markdown("FastAPI gateway is active.")
    gr.Markdown("- **Interactive Swagger Docs:** Access [`/docs`](/docs)")

# Mount Gradio at the root onto your existing FastAPI application preserving all the endpoints
# This leaves all your FastAPI routes (such as /docs and /v1/...) running untouched
app = gr.mount_gradio_app(fastapi_app, demo, path="/")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)