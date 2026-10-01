import { useState } from "react";
import { PageHeader } from "@/components/common/PageHeader";
import { PromptEditor } from "@/features/inspector/PromptEditor";
import { InspectionResult } from "@/features/inspector/InspectionResult";
import { inspectorApi } from "@/features/inspector/api";
import { ApiError } from "@/lib/api";
import type { InspectResponse } from "@/types/api";

export default function InspectorPage() {
  const [prompt, setPrompt] = useState("");
  const [keySecret, setKeySecret] = useState("");
  const [result, setResult] = useState<InspectResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleInspect() {
    if (!prompt.trim() || !keySecret.trim()) return;
    setIsLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await inspectorApi.inspect({ prompt }, keySecret.trim());
      setResult(res);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Couldn't complete the inspection.");
    } finally {
      setIsLoading(false);
    }
  }

  function handleClear() {
    setPrompt("");
    setResult(null);
    setError(null);
  }

  return (
    <div>
      <PageHeader title="Security Inspector" description="Test how AegisLLM inspects a prompt before it reaches your LLM." />
      <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
        <PromptEditor
          prompt={prompt}
          onPromptChange={setPrompt}
          keySecret={keySecret}
          onKeySecretChange={setKeySecret}
          onInspect={handleInspect}
          onClear={handleClear}
          isLoading={isLoading}
        />
        <InspectionResult result={result} isLoading={isLoading} error={error} />
      </div>
    </div>
  );
}
