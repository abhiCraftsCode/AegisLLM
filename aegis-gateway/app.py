import os

import gradio as gr
import uvicorn

from starlette.applications import Starlette
from starlette.routing import Mount

from app.main import app as fastapi_app


with gr.Blocks(title="Aegis Gateway") as demo:
    gr.Markdown("# 🛡️ Aegis Gateway is Live")
    gr.Markdown("FastAPI gateway is active.")
    gr.Markdown("- **Interactive Swagger Docs:** Access [`/docs`](/docs)")


# Mount the Gradio UI onto the existing FastAPI application.
fastapi_app = gr.mount_gradio_app(
    fastapi_app,
    demo,
    path="/",
    ssr_mode=False,
)


# Explicitly propagate the FastAPI application's lifespan.
async def lifespan(app):
    async with fastapi_app.router.lifespan_context(fastapi_app):
        yield


# Outer ASGI application used by Uvicorn.
app = Starlette(
    routes=[
        Mount("/", app=fastapi_app),
    ],
    lifespan=lifespan,
)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
    )