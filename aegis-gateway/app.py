import gradio as gr

from app.main import app as fastapi_app


with gr.Blocks(title="Aegis Gateway") as demo:
    gr.Markdown("# 🛡️ Aegis Gateway is Live")
    gr.Markdown("FastAPI gateway is active.")
    gr.Markdown("- **Interactive Swagger Docs:** Access [`/docs`](/docs)")


server = gr.Server(title="Aegis Gateway")

# Add all existing FastAPI routes.
server.include_router(fastapi_app.router)

# Preserve the ORIGINAL FastAPI lifespan.
server.router.lifespan_context = fastapi_app.router.lifespan_context

# Mount Gradio onto the same FastAPI server.
gr.mount_gradio_app(
    server,
    demo,
    path="/",
    ssr_mode=False,
)


if __name__ == "__main__":
    server.launch(
        server_name="0.0.0.0",
        server_port=7860,
        ssr_mode=False,
    )