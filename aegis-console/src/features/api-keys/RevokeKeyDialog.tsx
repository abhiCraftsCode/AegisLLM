import { useState } from "react";
import { ConfirmDialog } from "@/components/common/ConfirmDialog";
import { apiKeysApi } from "./api";
import { ApiError } from "@/lib/api";
import { useToast } from "@/components/ui/Toast";
import type { KeySchema } from "@/types/api";

export function RevokeKeyDialog({
  keyRecord,
  onClose,
  onRevoked,
}: {
  keyRecord: KeySchema;
  onClose: () => void;
  onRevoked: () => void;
}) {
  const { toast } = useToast();
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleConfirm() {
    setIsSubmitting(true);
    try {
      await apiKeysApi.deactivate(keyRecord.id);
      toast("API key revoked", "success");
      onRevoked();
    } catch (err) {
      toast(err instanceof ApiError ? err.message : "Couldn't revoke the API key.", "error");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <ConfirmDialog
      open
      onClose={onClose}
      onConfirm={handleConfirm}
      title="Revoke API key?"
      description="This action permanently disables this key. Requests using it will no longer be authorized."
      confirmLabel="Revoke Key"
      isLoading={isSubmitting}
      danger
    />
  );
}
