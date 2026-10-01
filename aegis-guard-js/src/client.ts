import type { ChatCompletionResponse, InspectResponse } from "./models.js";
import { AegisTransport } from "./transport.js";

export interface AegisClientOptions {
  apiKey: string;
  baseUrl: string;
  timeout?: number;
}

export class AegisClient {
  private readonly transport: AegisTransport;

  constructor(options: AegisClientOptions) {
    if (typeof options.apiKey !== "string" || !options.apiKey.trim()) {
      throw new Error("apiKey must be a non-empty string.");
    }

    if (typeof options.baseUrl !== "string" || !options.baseUrl.trim()) {
      throw new Error("baseUrl must be a non-empty string.");
    }

    if (options.timeout !== undefined && options.timeout <= 0) {
      throw new Error("timeout must be greater than 0.");
    }

    this.transport = new AegisTransport(
      options.baseUrl,
      options.apiKey,
      options.timeout,
    );
  }

  async inspect(prompt: string): Promise<InspectResponse> {
    if (typeof prompt !== "string" || !prompt.trim()) {
      throw new Error("prompt must be a non-empty string.");
    }

    const data = await this.transport.post("/chat/inspect", {
      prompt,
    });

    return data as unknown as InspectResponse;
  }

  async chat(
    model: string,
    messages: Record<string, unknown>[],
  ): Promise<ChatCompletionResponse> {
    if (typeof model !== "string" || !model.trim()) {
      throw new Error("model must be a non-empty string.");
    }

    if (!Array.isArray(messages) || messages.length === 0) {
      throw new Error("messages must be a non-empty array.");
    }

    const data = await this.transport.post("/chat/completions", {
      model,
      messages,
    });

    return data as unknown as ChatCompletionResponse;
  }
}
