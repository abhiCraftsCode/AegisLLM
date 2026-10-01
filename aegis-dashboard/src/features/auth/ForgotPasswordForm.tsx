import { useState, type FormEvent } from "react";
import { Link } from "react-router-dom";
import { CheckCircle2 } from "lucide-react";
import { Input } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";
import { authApi } from "./api";
import { ApiError } from "@/lib/api";

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export function ForgotPasswordForm() {
  const [email, setEmail] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [formError, setFormError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setFormError(null);
    if (!EMAIL_RE.test(email.trim())) {
      setError("Enter a valid email address.");
      return;
    }
    setError(null);
    setIsSubmitting(true);
    try {
      await authApi.forgotPassword({ email: email.trim() });
      setSubmitted(true);
    } catch (err) {
      setFormError(err instanceof ApiError ? err.message : "Something went wrong. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  }

  if (submitted) {
    return (
      <div className="flex flex-col items-center gap-4 rounded-2xl border border-aegis-border bg-aegis-surface/50 p-6 text-center">
        <div className="flex h-11 w-11 items-center justify-center rounded-full bg-aegis-mint/10 text-aegis-mint">
          <CheckCircle2 size={22} />
        </div>
        <div>
          <h2 className="text-sm font-semibold text-aegis-text">Check your inbox</h2>
          <p className="mt-1.5 text-sm text-aegis-textMuted">
            If an account exists for that email, we&apos;ve sent a link to reset your password.
          </p>
        </div>
        <Link to="/login" className="text-sm font-medium text-aegis-cyan hover:underline">
          Back to Sign In
        </Link>
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
      <Input
        label="Email"
        name="email"
        type="email"
        autoComplete="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        error={error ?? undefined}
        placeholder="you@company.com"
      />
      <Button type="submit" size="lg" className="mt-2 w-full" isLoading={isSubmitting}>
        {isSubmitting ? "Sending..." : "Send reset link"}
      </Button>
      <p className="text-center text-sm text-aegis-textMuted">
        <Link to="/login" className="font-medium text-aegis-cyan hover:underline">
          Back to Sign In
        </Link>
      </p>
    </form>
  );
}
