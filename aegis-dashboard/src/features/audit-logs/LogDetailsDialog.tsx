import { Copy, Check } from "lucide-react";
import { useState, type ReactNode } from "react";
import { Dialog } from "@/components/ui/Dialog";
import { StatusBadge } from "@/components/ui/StatusBadge";
import { formatDateTime, copyToClipboard } from "@/lib/utils";
import type { LogSchema } from "@/types/api";

function Field({ label, value }: { label: string; value: ReactNode }) {
  return (
    <div className="flex items-center justify-between border-b border-aegis-border py-2.5 last:border-0">
      <span className="text-xs text-aegis-textMuted">{label}</span>
      <span className="text-sm font-medium text-aegis-text">{value}</span>
    </div>
  );
}

export function LogDetailsDialog({ log, onClose }: { log: LogSchema; onClose: () => void }) {
  const [copied, setCopied] = useState(false);

  async function handleCopy() {
    const ok = await copyToClipboard(log.request_id);
    if (ok) {
      setCopied(true);
      window.setTimeout(() => setCopied(false), 2000);
    }
  }

  return (
    <Dialog open onClose={onClose} title="Audit log details">
      <div>
        <Field label="Status" value={<StatusBadge tone={log.is_blocked ? "danger" : "success"}>{log.is_blocked ? "Blocked" : "Allowed"}</StatusBadge>} />
        <Field label="Threat score" value={log.threat_score.toFixed(2)} />
        <Field
          label="Request ID"
          value={
            <button onClick={handleCopy} className="flex items-center gap-1.5 font-mono text-xs text-aegis-cyan hover:underline">
              {log.request_id}
              {copied ? <Check size={13} /> : <Copy size={13} />}
            </button>
          }
        />
        <Field label="Reason" value={<span className="max-w-[220px] truncate text-right">{log.reason ?? "No reason provided"}</span>} />
        <Field label="Latency" value={`${log.latency_ms.toFixed(1)} ms`} />
        <Field label="Created" value={formatDateTime(log.created_at)} />
        <Field label="LLM name" value={log.llm_name ?? "—"} />
        <Field label="LLM URL" value={<span className="max-w-[220px] truncate text-right">{log.llm_url ?? "—"}</span>} />
        <Field label="Key ID" value={log.key_id ?? "—"} />
      </div>
    </Dialog>
  );
}
