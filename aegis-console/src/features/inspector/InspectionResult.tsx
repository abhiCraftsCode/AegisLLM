import { useState } from "react";
import { ShieldCheck, ShieldAlert, Copy, Check } from "lucide-react";
import { Skeleton } from "@/components/ui/Skeleton";
import { ErrorState } from "@/components/common/ErrorState";
import { EmptyState } from "@/components/common/EmptyState";
import { copyToClipboard, shortenId } from "@/lib/utils";
import type { InspectResponse } from "@/types/api";

export function InspectionResult({
  result,
  isLoading,
  error,
}: {
  result: InspectResponse | null;
  isLoading: boolean;
  error: string | null;
}) {
  const [copied, setCopied] = useState(false);

  async function handleCopy(id: string) {
    const ok = await copyToClipboard(id);
    if (ok) {
      setCopied(true);
      window.setTimeout(() => setCopied(false), 2000);
    }
  }

  return (
    <div className="flex h-full flex-col rounded-2xl border border-aegis-border bg-aegis-surface/60 p-5">
      <h2 className="text-sm font-semibold text-aegis-text">Security Inspection</h2>

      <div className="mt-3 flex-1">
        {isLoading && (
          <div className="space-y-3">
            <Skeleton className="h-10 w-40" />
            <Skeleton className="h-24" />
            <Skeleton className="h-16" />
          </div>
        )}

        {!isLoading && error && <ErrorState message={error} />}

        {!isLoading && !error && !result && (
          <EmptyState title="Ready to inspect" description="Enter a prompt and run a security inspection." />
        )}

        {!isLoading && !error && result && (
          <div className="space-y-4">
            <div
              className={`flex items-center gap-2 rounded-xl border px-4 py-3 text-sm font-semibold ${
                result.is_blocked
                  ? "border-aegis-coral/40 bg-aegis-coral/10 text-aegis-coral"
                  : "border-aegis-mint/30 bg-aegis-mint/10 text-aegis-mint"
              }`}
            >
              {result.is_blocked ? <ShieldAlert size={18} /> : <ShieldCheck size={18} />}
              {result.is_blocked ? "Prompt Blocked" : "Prompt Allowed"}
            </div>

            <div className="rounded-xl bg-white/[0.02] p-4">
              <p className="text-xs text-aegis-textFaint">Reason</p>
              <p className="mt-1 text-sm text-aegis-text">{result.reason}</p>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div className="rounded-xl bg-white/[0.02] p-4">
                <p className="text-xs text-aegis-textFaint">Threat score</p>
                <p className="mt-1 text-lg font-semibold text-aegis-text">{result.threat_score.toFixed(2)}</p>
              </div>
              <div className="rounded-xl bg-white/[0.02] p-4">
                <p className="text-xs text-aegis-textFaint">Latency</p>
                <p className="mt-1 text-lg font-semibold text-aegis-text">{result.latency_ms.toFixed(1)} ms</p>
              </div>
            </div>

            <div className="flex items-center justify-between rounded-xl bg-white/[0.02] p-4">
              <div>
                <p className="text-xs text-aegis-textFaint">Request</p>
                <p className="font-mono text-sm text-aegis-text">{shortenId(result.request_id)}</p>
              </div>
              <button
                onClick={() => handleCopy(result.request_id)}
                className="flex items-center gap-1.5 rounded-lg border border-aegis-border px-2.5 py-1.5 text-xs text-aegis-textMuted hover:text-aegis-text"
              >
                {copied ? <Check size={13} /> : <Copy size={13} />}
                {copied ? "Copied" : "Copy"}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
