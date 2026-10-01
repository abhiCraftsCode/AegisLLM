import { useState, type FormEvent } from "react";
import { Dialog } from "@/components/ui/Dialog";
import { PasswordInput } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";
import { useToast } from "@/components/ui/Toast";
import { userApi } from "./api";
import { ApiError } from "@/lib/api";

export function PasswordForm({ open, onClose }: { open: boolean; onClose: () => void }) {
  const { toast } = useToast();
  const [currPassword, setCurrPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  function reset() {
    setCurrPassword("");
    setNewPassword("");
    setConfirmPassword("");
    setErrors({});
  }

  function validate(): boolean {
    const next: Record<string, string> = {};
    if (currPassword.length < 8) next.currPassword = "Enter your current password.";
    if (newPassword.length < 8 || newPassword.length > 128) {
      next.newPassword = "Password must be between 8 and 128 characters.";
    }
    if (confirmPassword !== newPassword) next.confirmPassword = "Passwords do not match.";
    setErrors(next);
    return Object.keys(next).length === 0;
  }

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    if (!validate() || isSubmitting) return;
    setIsSubmitting(true);
    try {
      await userApi.updatePassword({ curr_password: currPassword, new_password: newPassword });
      toast("Password changed", "success");
      reset();
      onClose();
    } catch (err) {
      toast(err instanceof ApiError ? err.message : "Couldn't change your password.", "error");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <Dialog open={open} onClose={onClose} title="Change Password" description="Update your account password.">
      <form onSubmit={onSubmit} noValidate className="flex flex-col gap-4">
        <PasswordInput
          label="Current password"
          name="currPassword"
          autoComplete="current-password"
          value={currPassword}
          onChange={(e) => setCurrPassword(e.target.value)}
          error={errors.currPassword}
        />
        <PasswordInput
          label="New password"
          name="newPassword"
          autoComplete="new-password"
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
          error={errors.newPassword}
          hint="8–128 characters"
        />
        <PasswordInput
          label="Confirm new password"
          name="confirmPassword"
          autoComplete="new-password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          error={errors.confirmPassword}
        />
        <div className="mt-2 flex justify-end gap-2">
          <Button type="button" variant="secondary" size="sm" onClick={onClose} disabled={isSubmitting}>
            Cancel
          </Button>
          <Button type="submit" size="sm" isLoading={isSubmitting}>
            Change Password
          </Button>
        </div>
      </form>
    </Dialog>
  );
}
