class AegisGuard {
  constructor(config = {}) {
    this.apiKey = config.apiKey;
    this.baseUrl =
      config.baseUrl || "http://localhost:8000/v1/chat/completions";
  }

  async checkAndExecute({ model = "gpt-4o", modelApiKey = null, prompt }) {
    try {
      const res = await fetch(this.baseUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${this.apiKey}`,
        },
        body: JSON.stringify({
          model,
          modelApiKey,
          messages: [{ role: "user", content: prompt }],
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        return {
          success: false,
          status: "BLOCKED",
          reason: data.reason || "Blocked by Aegis Security Gateway",
          threatScore: data.threat_score,
        };
      }

      return {
        success: true,
        status: "ALLOWED",
        response: data.choices[0].message.content,
      };
    } catch (err) {
      return { success: false, status: "ERROR", message: err.message };
    }
  }
}

export default AegisGuard;
