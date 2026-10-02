export type IntegrationMethodId =
  | "rest"
  | "python"
  | "node"
  | "openai"
  | "langchain";

export type ContentBlock =
  | { type: "paragraph"; text: string }
  | { type: "code"; language: string; code: string; title?: string }
  | { type: "note"; text: string };

export interface ContentSection {
  heading: string;
  blocks: ContentBlock[];
}

export interface IntegrationMethod {
  id: IntegrationMethodId;
  label: string;
  overview: string;
  sections: ContentSection[];
}

export const integrationMethods: IntegrationMethod[] = [
  // ---------------------------------------------------------------- REST
  {
    id: "rest",
    label: "REST API",
    overview:
      "Call AegisLLM directly over HTTP from any language that can make a request — no SDK required.",
    sections: [
      {
        heading: "Authentication",
        blocks: [
          {
            type: "paragraph",
            text: "Every request is authenticated with your AegisLLM API key, sent as a bearer token.",
          },
          {
            type: "code",
            language: "http",
            code: "Authorization: Bearer aegis_xxxxx",
          },
          {
            type: "note",
            text: "Keep API keys server-side. Never embed them in client-side code or ship them to a browser.",
          },
        ],
      },
      {
        heading: "Inspect",
        blocks: [
          {
            type: "paragraph",
            text: "Inspect a prompt without forwarding it to an upstream LLM — useful for pre-flight checks.",
          },
          { type: "code", language: "http", code: "POST /api/v1/chat/inspect" },
          {
            type: "code",
            language: "json",
            title: "Request",
            code: `{
  "prompt": "Your prompt here"
}`,
          },
          {
            type: "code",
            language: "json",
            title: "Response",
            code: `{
  "request_id": "uuid",
  "is_blocked": false,
  "threat_score": 0.02,
  "reason": "safe",
  "latency_ms": 25.4
}`,
          },
        ],
      },
      {
        heading: "Chat Completion",
        blocks: [
          {
            type: "paragraph",
            text: "AegisLLM inspects the request first, then forwards it to your configured upstream LLM only if it's allowed.",
          },
          {
            type: "code",
            language: "http",
            code: "POST /api/v1/chat/completions",
          },
          {
            type: "code",
            language: "json",
            title: "Request",
            code: `{
  "model": "your-model",
  "messages": [
    {
      "role": "user",
      "content": "Your prompt here"
    }
  ]
}`,
          },
          {
            type: "code",
            language: "json",
            title: "Response — allowed (illustrative)",
            code: `{
  "request_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "is_blocked": false,
  "threat_score": 0.03,
  "reason": "safe",
  "latency_ms": 184.2,
  "response": {
    "id": "chatcmpl-example",
    "choices": [
      {
        "message": {
          "role": "assistant",
          "content": "This is an illustrative response."
        }
      }
    ]
  }
}`,
          },
          {
            type: "paragraph",
            text: "If the prompt is blocked, the request never reaches your LLM and no response body is generated:",
          },
          {
            type: "code",
            language: "json",
            title: "Response — blocked",
            code: `{
  "is_blocked": true,
  "response": null
}`,
          },
          {
            type: "note",
            text: "All example values above are illustrative, not live data.",
          },
        ],
      },
    ],
  },
  // -------------------------------------------------------------- PYTHON
  {
    id: "python",
    label: "Python SDK",
    overview:
      "A thin Python client around the REST API for quicker integration into Python services.",
    sections: [
      {
        heading: "Installation",
        blocks: [
          { type: "code", language: "bash", code: "pip install aegis-guard" },
        ],
      },
      {
        heading: "Initialization",
        blocks: [
          {
            type: "code",
            language: "python",
            code: `from aegis_guard import AegisClient

client = AegisClient(
    api_key="aegis_xxxxx",
    base_url="https://your-aegis-server/api/v1"
)`,
          },
        ],
      },
      {
        heading: "Inspect",
        blocks: [
          {
            type: "code",
            language: "python",
            code: `result = client.inspect("Your prompt here")

print(result.is_blocked)
print(result.threat_score)
print(result.reason)`,
          },
        ],
      },
      {
        heading: "Chat",
        blocks: [
          {
            type: "code",
            language: "python",
            code: `result = client.chat(
    model="your-model",
    messages=[
        {
            "role": "user",
            "content": "Your prompt here"
        }
    ]
)`,
          },
          {
            type: "paragraph",
            text: "When the prompt is safe, result carries the upstream LLM's response. When it's blocked, result.is_blocked is true and no upstream call is made.",
          },
        ],
      },
    ],
  },
  // ---------------------------------------------------------------- NODE
  {
    id: "node",
    label: "Node.js SDK",
    overview:
      "A TypeScript-first client for Node.js services and edge runtimes.",
    sections: [
      {
        heading: "Installation",
        blocks: [
          { type: "code", language: "bash", code: "npm install aegis-guard" },
        ],
      },
      {
        heading: "Initialization",
        blocks: [
          {
            type: "code",
            language: "typescript",
            code: `import { AegisClient } from "aegis-guard";

const client = new AegisClient({
    apiKey: "aegis_xxxxx",
    baseUrl: "https://your-aegis-server/api/v1",
});`,
          },
        ],
      },
      {
        heading: "Inspect",
        blocks: [
          {
            type: "code",
            language: "typescript",
            code: `const result = await client.inspect("Your prompt here");

console.log(result.is_blocked);
console.log(result.threat_score);
console.log(result.reason);`,
          },
        ],
      },
      {
        heading: "Chat",
        blocks: [
          {
            type: "code",
            language: "typescript",
            code: `const result = await client.chat({
    model: "your-model",
    messages: [
        {
            role: "user",
            content: "Your prompt here",
        },
    ],
});`,
          },
          {
            type: "paragraph",
            text: "When the prompt is safe, result carries the upstream LLM's response. When it's blocked, result.is_blocked is true and no upstream call is made.",
          },
        ],
      },
    ],
  },
  // ------------------------------------------------------------- OPENAI
  {
    id: "openai",
    label: "OpenAI Compatible",
    overview:
      "Point an existing OpenAI SDK integration at AegisLLM instead of OpenAI directly — no code changes beyond the client configuration.",
    sections: [
      {
        heading: "Configuration",
        blocks: [
          {
            type: "code",
            language: "python",
            code: `from openai import OpenAI

client = OpenAI(
    api_key="aegis_xxxxx",
    base_url="https://your-aegis-server/api/v1/openai"
)`,
          },
        ],
      },
      {
        heading: "Chat Completion",
        blocks: [
          {
            type: "code",
            language: "python",
            code: `response = client.chat.completions.create(
    model="your-model",
    messages=[
        {
            "role": "user",
            "content": "Your prompt here"
        }
    ]
)`,
          },
          { type: "paragraph", text: "The request reaches:" },
          {
            type: "code",
            language: "text",
            code: "/api/v1/openai/chat/completions",
          },
          {
            type: "paragraph",
            text: "AegisLLM runs its security inspection before calling the upstream LLM, then returns a normalized OpenAI-style response with an added aegis field:",
          },
          {
            type: "code",
            language: "json",
            title: "Response (illustrative)",
            code: `{
  "id": "aegis-...",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "your-model",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "..."
      },
      "finish_reason": "stop"
    }
  ],
  "aegis": {
    "request_id": "...",
    "is_blocked": false,
    "threat_score": 0.01,
    "reason": "safe",
    "latency_ms": 12.4
  }
}`,
          },
          {
            type: "note",
            text: "All example values above are illustrative, not live data.",
          },
        ],
      },
    ],
  },
  // ---------------------------------------------------------- LANGCHAIN
  {
    id: "langchain",
    label: "LangChain Middleware",
    overview:
      "Drop AegisLLM into a LangChain agent as middleware so every user input is inspected before the model runs.",
    sections: [
      {
        heading: "Installation",
        blocks: [
          {
            type: "code",
            language: "bash",
            code: "pip install aegis-guard langchain",
          },
        ],
      },
      {
        heading: "Setup",
        blocks: [
          {
            type: "code",
            language: "python",
            code: `from aegis_guard.middleware import AegisMiddleware

middleware = AegisMiddleware(
    api_key="aegis_xxxxx",
    base_url="https://your-aegis-server/api/v1"
)`,
          },
        ],
      },
      {
        heading: "Add to Agent",
        blocks: [
          {
            type: "code",
            language: "python",
            code: `agent = create_agent(
    model=model,
    tools=[],
    middleware=[middleware]
)`,
          },
          {
            type: "paragraph",
            text: "The middleware inspects the user's input before the agent is allowed to call the model:",
          },
          {
            type: "code",
            language: "text",
            code: `User Input
    ↓
LangChain Agent
    ↓
Aegis Middleware
    ↓
Security Inspection
    ↓
Safe ──────→ LLM
Blocked ───→ LLM call stopped`,
          },
        ],
      },
    ],
  },
];
