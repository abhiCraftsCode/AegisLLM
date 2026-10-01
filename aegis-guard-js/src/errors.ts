export class AegisError extends Error {
  readonly statusCode: number;

  constructor(detail = "Unexpected Aegis error occurred.", statusCode = 500) {
    super(detail);

    this.name = "AegisError";
    this.statusCode = statusCode;
  }
}

export class AegisAuthenticationError extends AegisError {
  constructor(detail = "Authentication failed.", statusCode = 401) {
    super(detail, statusCode);

    this.name = "AegisAuthenticationError";
  }
}

export class AegisRateLimitError extends AegisError {
  constructor(detail = "Request was rate limited.", statusCode = 429) {
    super(detail, statusCode);

    this.name = "AegisRateLimitError";
  }
}

export class AegisGatewayError extends AegisError {
  constructor(detail = "Aegis gateway error occurred.", statusCode = 502) {
    super(detail, statusCode);

    this.name = "AegisGatewayError";
  }
}
