import { useState } from "react";
import { Copy, Check, Download } from "lucide-react";
import { Dialog } from "@/components/ui/Dialog";
import { Button } from "@/components/ui/Button";
import { copyToClipboard, downloadTextFile } from "@/lib/utils";
import { useToast } from "@/components/ui/Toast";
import type { GenerateResponse } from "@/types/api";

export function KeyCreatedDialog({
  result,
  onDone,
}: {
  result: GenerateResponse;
  onDone: () => void;
}) {
  const { toast } = useToast();
  const [copied, setCopied] = useState(false);

  async function handleCopy() {
    const ok = await copyToClipboard(result.secret);
    if (ok) {
      setCopied(true);
      toast("Copied to clipboard", "success");
      window.setTimeout(() => setCopied(false), 2000);
    }
  }

  function handleDownload() {
    downloadTextFile(
      `aegisllm-${result.key.name ?? result.key.prefix}.txt`,
      `AegisLLM API Key\nName: ${result.key.name ?? "Untitled"}\nSecret: ${result.secret}\n`
    );
  }

  return (
    <Dialog open onClose={onDone} title="API key created" description="This key will not be shown again.">
      <div className="rounded-lg border border-aegis-border bg-aegis-bg/60 p-3">
        <code className="block break-all font-mono text-sm text-aegis-cyan">{result.secret}</code>
      </div>
      <div className="mt-4 flex gap-2">
        <Button variant="secondary" size="sm" onClick={handleCopy} className="flex-1">
          {copied ? <Check size={14} /> : <Copy size={14} />}
          {copied ? "Copied" : "Copy"}
        </Button>
        <Button variant="secondary" size="sm" onClick={handleDownload} className="flex-1">
          <Download size={14} />
          Download
        </Button>
      </div>
      <Button className="mt-6 w-full" onClick={onDone}>
        Done
      </Button>
    </Dialog>
  );
}
