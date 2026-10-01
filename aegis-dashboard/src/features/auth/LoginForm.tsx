import { useState, type FormEvent } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "@/hooks/useAuth";
import { Input, PasswordInput } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";
import { ApiError } from "@/lib/api";
import { OAuthButtons } from "./OAuthButtons";

export function LoginForm() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState<{ identifier?: string; password?: string }>({});
  const [formError, setFormError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  function validate(): boolean {
    const next: typeof errors = {};
    if (!identifier.trim()) next.identifier = "Email or phone number is required.";
    if (password.length < 8) next.password = "Password must be at least 8 characters.";
    setErrors(next);
    return Object.keys(next).length === 0;
  }

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setFormError(null);
    if (!validate() || isSubmitting) return;
    setIsSubmitting(true);
    try {
      await login(identifier, password);
      const from = (location.state as { from?: string } | null)?.from ?? "/app/dashboard";
      navigate(from, { replace: true });
    } catch (err) {
      if (err instanceof ApiError) {
        setFormError(err.status === 401 ? "Invalid credentials. Please try again." : err.message);
      } else {
        setFormError("Something went wrong. Please try again.");
      }
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <form onSubmit={onSubmit} noValidate className="flex flex-col gap-4">
      {formError && (
        <div role="alert" className="rounded-lg border border-aegis-coral/30 bg-aegis-coral/10 px-3 py-2.5 text-sm text-aegis-coral">
          {formError}
        </div>
      )}
      <Input
        label="Email or phone number"
        name="identifier"
        autoComplete="username"
        value={identifier}
        onChange={(e) => setIdentifier(e.target.value)}
        error={errors.identifier}
        placeholder="you@company.com"
      />
      <div>
        <div className="flex items-center justify-between">
          <label htmlFor="password" className="text-sm font-medium text-aegis-text">
            Password
          </label>
          <Link to="/forgot-password" className="text-xs font-medium text-aegis-cyan hover:underline">
            Forgot password?
          </Link>
        </div>
        <div className="mt-1.5">
          <PasswordInput
            name="password"
            autoComplete="current-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            error={errors.password}
            placeholder="••••••••"
          />
        </div>
      </div>
      <Button type="submit" size="lg" className="mt-2 w-full" isLoading={isSubmitting}>
        {isSubmitting ? "Signing in..." : "Sign In"}
      </Button>
      <OAuthButtons />
      <p className="text-center text-sm text-aegis-textMuted">
        Don&apos;t have an account?{" "}
        <Link to="/register" className="font-medium text-aegis-cyan hover:underline">
          Create one
        </Link>
      </p>
    </form>
  );
}
