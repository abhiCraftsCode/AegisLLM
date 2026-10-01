import { useState } from "react";
import { Dialog } from "@/components/ui/Dialog";
import { KeyForm, type KeyFormValues } from "./KeyForm";
import { apiKeysApi } from "./api";
import { ApiError } from "@/lib/api";
import { useToast } from "@/components/ui/Toast";
import type { KeySchema } from "@/types/api";

export function EditKeyDialog({
  keyRecord,
  onClose,
  onUpdated,
}: {
  keyRecord: KeySchema;
  onClose: () => void;
  onUpdated: () => void;
}) {
  const { toast } = useToast();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(values: KeyFormValues) {
    setIsSubmitting(true);
    setError(null);
    try {
      await apiKeysApi.update(keyRecord.id, {
        llm_name: values.llm_name,
        llm_url: values.llm_url,
        llm_auth: values.llm_auth,
      });
      toast("API key updated", "success");
      onUpdated();
    } catch (err) {
      const message = err instanceof ApiError ? err.message : "Couldn't update the API key.";
      setError(message);
      toast(message, "error");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <Dialog open onClose={onClose} title="Edit API Key" description={keyRecord.name ?? keyRecord.prefix}>
      {error && (
        <div role="alert" className="mb-4 rounded-lg border border-aegis-coral/30 bg-aegis-coral/10 px-3 py-2.5 text-sm text-aegis-coral">
          {error}
        </div>
      )}
      <KeyForm
        mode="edit"
        initialValues={{ llm_name: keyRecord.llm_name ?? "", llm_url: keyRecord.llm_url ?? "" }}
        onSubmit={handleSubmit}
        onCancel={onClose}
        isSubmitting={isSubmitting}
      />
    </Dialog>
  );
}
