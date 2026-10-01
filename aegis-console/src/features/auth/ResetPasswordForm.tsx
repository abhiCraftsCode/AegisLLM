import { useState, type FormEvent } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { CheckCircle2 } from "lucide-react";
import { PasswordInput } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";
import { authApi } from "./api";
import { ApiError } from "@/lib/api";

export function ResetPasswordForm() {
  const { token } = useParams<{ token: string }>();
  const navigate = useNavigate();

  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [errors, setErrors] = useState<{ newPassword?: string; confirmPassword?: string }>({});
  const [formError, setFormError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [done, setDone] = useState(false);

  function validate(): boolean {
    const next: typeof errors = {};
    if (newPassword.length < 8 || newPassword.length > 128) {
      next.newPassword = "Password must be between 8 and 128 characters.";
    }
    if (confirmPassword !== newPassword) {
      next.confirmPassword = "Passwords do not match.";
    }
    setErrors(next);
    return Object.keys(next).length === 0;
  }

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setFormError(null);
    if (!token) {
      setFormError("This reset link is invalid or missing a token.");
      return;
    }
    if (!validate() || isSubmitting) return;
    setIsSubmitting(true);
    try {
      await authApi.resetPassword({ new_password: newPassword, token });
      setDone(true);
    } catch (err) {
      setFormError(err instanceof ApiError ? err.message : "Something went wrong. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  }

  if (done) {
    return (
      <div className="flex flex-col items-center gap-4 rounded-2xl border border-aegis-border bg-aegis-surface/50 p-6 text-center">
        <div className="flex h-11 w-11 items-center justify-center rounded-full bg-aegis-mint/10 text-aegis-mint">
          <CheckCircle2 size={22} />
        </div>
        <div>
          <h2 className="text-sm font-semibold text-aegis-text">Password updated</h2>
          <p className="mt-1.5 text-sm text-aegis-textMuted">Your password has been changed successfully.</p>
        </div>
        <Button onClick={() => navigate("/login", { replace: true })}>Continue to Sign In</Button>
      </div>
    );
  }

  return (
    <form onSubmit={onSubmit} noValidate className="flex flex-col gap-4">
      {formError && (
        <div role="alert" className="rounded-lg border border-aegis-coral/30 bg-aegis-coral/10 px-3 py-2.5 text-sm text-aegis-coral">
          {formError}
        </div>
      )}
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
      <Button type="submit" size="lg" className="mt-2 w-full" isLoading={isSubmitting}>
        {isSubmitting ? "Updating..." : "Update password"}
      </Button>
      <p className="text-center text-sm text-aegis-textMuted">
        <Link to="/login" className="font-medium text-aegis-cyan hover:underline">
          Back to Sign In
        </Link>
      </p>
    </form>
  );
}
