import {
  AegisAuthenticationError,
  AegisError,
  AegisGatewayError,
  AegisRateLimitError,
} from "./errors.js";

export class AegisTransport {
  private readonly baseUrl: string;
  private readonly apiKey: string;
  private readonly timeout: number;

  constructor(baseUrl: string, apiKey: string, timeout = 30000) {
    this.baseUrl = baseUrl.replace(/\/+$/, "");
    this.apiKey = apiKey;
    this.timeout = timeout;
  }

  async post(
    path: string,
    payload: Record<string, unknown>,
  ): Promise<Record<string, unknown>> {
    const controller = new AbortController();

    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    let response: Response;

    try {
      response = await fetch(`${this.baseUrl}/${path.replace(/^\/+/, "")}`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${this.apiKey}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
        signal: controller.signal,
      });
    } catch (error) {
      if (error instanceof DOMException && error.name === "AbortError") {
        throw new AegisGatewayError("Request to Aegis timed out.");
      }
      throw new AegisGatewayError("Unable to connect to the Aegis gateway.");
    } finally {
      clearTimeout(timeoutId);
    }

    await this.handleError(response);

    try {
      const data: unknown = await response.json();

      if (typeof data !== "object" || data === null || Array.isArray(data)) {
        throw new Error();
      }

      return data as Record<string, unknown>;
    } catch {
      throw new AegisError("Aegis returned an invalid response.");
    }
  }

  private async handleError(response: Response): Promise<void> {
    if (response.status < 400) {
      return;
    }

    const detail = await this.getErrorDetail(response);
    const statusCode = response.status;

    if (statusCode === 401 || statusCode === 403) {
      throw new AegisAuthenticationError(detail, statusCode);
    }

    if (statusCode === 429) {
      throw new AegisRateLimitError(detail, statusCode);
    }

    if (statusCode === 502 || statusCode === 504) {
      throw new AegisGatewayError(detail, statusCode);
    }

    throw new AegisError(detail, statusCode);
  }

  private async getErrorDetail(response: Response): Promise<string> {
    try {
      const data: unknown = await response.json();

      if (typeof data === "object" && data !== null && !Array.isArray(data)) {
        const detail = (data as { detail?: unknown }).detail;

        if (typeof detail === "string" && detail.length > 0) {
          return detail;
        }
      }
    } catch {
      // Fall back to the HTTP status below.
    }

    return `Aegis request failed with status ${response.status}.`;
  }
}
