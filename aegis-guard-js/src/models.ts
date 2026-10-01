export interface InspectResponse {
  request_id: string;
  is_blocked: boolean;
  threat_score: number;
  reason: string;
  latency_ms: number;
}

export interface ChatCompletionResponse extends InspectResponse {
  response: Record<string, unknown> | null;
}
