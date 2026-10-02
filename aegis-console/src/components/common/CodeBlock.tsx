import { useState } from "react";
import { Copy, Check } from "lucide-react";
import { copyToClipboard } from "@/lib/utils";
import { useToast } from "@/components/ui/Toast";

export function CodeBlock({
  code,
  language = "text",
  label,
}: {
  code: string;
  language?: string;
  label?: string;
}) {
  const { toast } = useToast();
  const [copied, setCopied] = useState(false);

  async function handleCopy() {
    const ok = await copyToClipboard(code);
    if (ok) {
      setCopied(true);
      toast("Copied to clipboard", "success");
      window.setTimeout(() => setCopied(false), 2000);
    }
  }

  return (
    <div className="overflow-hidden rounded-xl border border-aegis-border bg-aegis-bg/60">
      <div className="flex items-center justify-between border-b border-aegis-border bg-white/[0.02] px-3.5 py-2">
        <span className="font-mono text-[11px] uppercase tracking-wider text-aegis-textFaint">
          {label ?? language}
        </span>
        <button
          onClick={handleCopy}
          className="flex items-center gap-1.5 rounded-md px-2 py-1 text-xs text-aegis-textMuted transition-colors hover:bg-white/5 hover:text-aegis-text"
          aria-label="Copy code"
        >
          {copied ? <Check size={13} /> : <Copy size={13} />}
          {copied ? "Copied" : "Copy"}
        </button>
      </div>
      <pre className="overflow-x-auto p-3.5 text-[13px] leading-relaxed text-aegis-text">
        <code className="font-mono">{code}</code>
      </pre>
    </div>
  );
}
