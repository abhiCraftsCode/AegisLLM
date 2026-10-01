import { useState } from "react";
import { Dialog } from "@/components/ui/Dialog";
import { KeyForm, type KeyFormValues } from "./KeyForm";
import { apiKeysApi } from "./api";
import { ApiError } from "@/lib/api";
import { useToast } from "@/components/ui/Toast";
import type { GenerateResponse } from "@/types/api";

export function CreateKeyDialog({
  open,
  onClose,
  onCreated,
}: {
  open: boolean;
  onClose: () => void;
  onCreated: (result: GenerateResponse) => void;
}) {
  const { toast } = useToast();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(values: KeyFormValues) {
    setIsSubmitting(true);
    setError(null);
    try {
      const result = await apiKeysApi.generate({
        name: values.name,
        llm_name: values.llm_name,
        llm_url: values.llm_url,
        llm_auth: values.llm_auth,
      });
      onCreated(result);
    } catch (err) {
      const message = err instanceof ApiError ? err.message : "Couldn't create the API key.";
      setError(message);
      toast(message, "error");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <Dialog open={open} onClose={onClose} title="Create API Key" description="Connect a new application to AegisLLM.">
      {error && (
        <div role="alert" className="mb-4 rounded-lg border border-aegis-coral/30 bg-aegis-coral/10 px-3 py-2.5 text-sm text-aegis-coral">
          {error}
        </div>
      )}
      <KeyForm mode="create" onSubmit={handleSubmit} onCancel={onClose} isSubmitting={isSubmitting} />
    </Dialog>
  );
}
