import { useState, type FormEvent } from "react";
import { Input, PasswordInput } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";

export interface KeyFormValues {
  name?: string;
  llm_name?: string;
  llm_url?: string;
  llm_auth?: string;
}

export function KeyForm({
  mode,
  initialValues,
  onSubmit,
  onCancel,
  isSubmitting,
}: {
  mode: "create" | "edit";
  initialValues?: KeyFormValues;
  onSubmit: (values: KeyFormValues) => void;
  onCancel: () => void;
  isSubmitting?: boolean;
}) {
  const [name, setName] = useState(initialValues?.name ?? "");
  const [llmName, setLlmName] = useState(initialValues?.llm_name ?? "");
  const [llmUrl, setLlmUrl] = useState(initialValues?.llm_url ?? "");
  const [llmAuth, setLlmAuth] = useState("");

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    const values: KeyFormValues = {
      llm_name: llmName.trim() || undefined,
      llm_url: llmUrl.trim() || undefined,
      llm_auth: llmAuth.trim() || undefined,
    };
    if (mode === "create") {
      values.name = name.trim() || undefined;
    }
    onSubmit(values);
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4">
      {mode === "create" && (
        <Input
          label="Name"
          name="name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Production Chatbot"
        />
      )}

      <div className="rounded-xl border border-aegis-border bg-white/[0.02] p-4">
        <p className="mb-3 text-xs font-semibold uppercase tracking-wider text-aegis-textFaint">
          LLM Configuration
        </p>
        <div className="flex flex-col gap-4">
          <Input
            label="LLM Name"
            name="llm_name"
            value={llmName}
            onChange={(e) => setLlmName(e.target.value)}
            placeholder="My LLM"
          />
          <Input
            label="LLM URL"
            name="llm_url"
            value={llmUrl}
            onChange={(e) => setLlmUrl(e.target.value)}
            placeholder="https://example.com/v1/chat/completions"
          />
          <PasswordInput
            label="LLM Authorization"
            name="llm_auth"
            value={llmAuth}
            onChange={(e) => setLlmAuth(e.target.value)}
            placeholder={mode === "edit" ? "Enter new authorization (optional)" : "xx-api-key-xx"}
            hint={mode === "edit" ? "Leave blank to keep the existing authorization." : undefined}
          />
        </div>
      </div>

      <div className="mt-2 flex justify-end gap-2">
        <Button type="button" variant="secondary" size="sm" onClick={onCancel} disabled={isSubmitting}>
          Cancel
        </Button>
        <Button type="submit" size="sm" isLoading={isSubmitting}>
          {mode === "create" ? "Create Key" : "Save Changes"}
        </Button>
      </div>
    </form>
  );
}
