import { PasswordInput } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";

export function PromptEditor({
  prompt,
  onPromptChange,
  keySecret,
  onKeySecretChange,
  onInspect,
  onClear,
  isLoading,
}: {
  prompt: string;
  onPromptChange: (v: string) => void;
  keySecret: string;
  onKeySecretChange: (v: string) => void;
  onInspect: () => void;
  onClear: () => void;
  isLoading: boolean;
}) {
  return (
    <div className="flex h-full flex-col rounded-2xl border border-aegis-border bg-aegis-surface/60 p-5">
      <h2 className="text-sm font-semibold text-aegis-text">Prompt Workspace</h2>
      <textarea
        value={prompt}
        onChange={(e) => onPromptChange(e.target.value)}
        placeholder="Paste or write the prompt you want to test…"
        className="mt-3 h-56 w-full flex-1 resize-none rounded-xl border border-aegis-border bg-aegis-surface2/60 p-3.5 text-sm text-aegis-text outline-none placeholder:text-aegis-textFaint focus:border-aegis-cyan/60"
      />

      <div className="mt-4 border-t border-aegis-border pt-4">
        <PasswordInput
          label="API key secret"
          name="keySecret"
          value={keySecret}
          onChange={(e) => onKeySecretChange(e.target.value)}
          placeholder="Paste a generated API key secret"
          hint="Inspections authenticate with a gateway API key, not your account session. This value is kept only in memory for this session."
        />
      </div>

      <div className="mt-4 flex justify-end gap-2">
        <Button variant="secondary" size="sm" onClick={onClear} disabled={isLoading}>
          Clear
        </Button>
        <Button size="sm" onClick={onInspect} isLoading={isLoading} disabled={!prompt.trim() || !keySecret.trim()}>
          {isLoading ? "Inspecting..." : "Inspect"}
        </Button>
      </div>
    </div>
  );
}
