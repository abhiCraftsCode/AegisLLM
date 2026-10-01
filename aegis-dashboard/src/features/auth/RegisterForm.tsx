import { useState, type FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "@/hooks/useAuth";
import { Input, PasswordInput } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";
import { ApiError } from "@/lib/api";

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const PHONE_RE = /^(\+91)?[6-9]\d{9}$/;

export function RegisterForm() {
  const { register } = useAuth();
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [formError, setFormError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  function validate(): boolean {
    const next: Record<string, string> = {};
    if (name.trim().length < 2) next.name = "Name must be at least 2 characters.";
    if (!email.trim() && !phone.trim()) {
      next.contact = "Provide at least an email address or phone number.";
    }
    if (email.trim() && !EMAIL_RE.test(email.trim())) next.email = "Enter a valid email address.";
    if (phone.trim() && !PHONE_RE.test(phone.trim().replace(/\s/g, ""))) {
      next.phone = "Enter a valid Indian mobile number.";
    }
    if (password.length < 8 || password.length > 128) {
      next.password = "Password must be between 8 and 128 characters.";
    }
    setErrors(next);
    return Object.keys(next).length === 0;
  }

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setFormError(null);
    if (!validate() || isSubmitting) return;
    setIsSubmitting(true);
    try {
      await register({
        name: name.trim(),
        email: email.trim() || undefined,
        phone: phone.trim() || undefined,
        password,
      });
      navigate("/app/dashboard", { replace: true });
    } catch (err) {
      if (err instanceof ApiError) {
        setFormError(err.message);
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
        label="Full name"
        name="name"
        autoComplete="name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        error={errors.name}
        placeholder="Ada Lovelace"
      />
      <div>
        <Input
          label="Email"
          name="email"
          type="email"
          autoComplete="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          error={errors.email}
          placeholder="you@company.com"
        />
      </div>
      <div>
        <Input
          label="Phone"
          name="phone"
          type="tel"
          autoComplete="tel"
          value={phone}
          onChange={(e) => setPhone(e.target.value)}
          error={errors.phone}
          placeholder="9876543210"
        />
      </div>
      {errors.contact && <p className="-mt-2 text-xs text-aegis-coral">{errors.contact}</p>}
      {!errors.contact && (
        <p className="-mt-2 text-xs text-aegis-textFaint">Provide at least an email address or phone number.</p>
      )}
      <PasswordInput
        label="Password"
        name="password"
        autoComplete="new-password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        error={errors.password}
        hint="8–128 characters"
        placeholder="••••••••"
      />
      <Button type="submit" size="lg" className="mt-2 w-full" isLoading={isSubmitting}>
        {isSubmitting ? "Creating account..." : "Create Account"}
      </Button>
      <p className="text-center text-sm text-aegis-textMuted">
        Already have an account?{" "}
        <Link to="/login" className="font-medium text-aegis-cyan hover:underline">
          Sign in
        </Link>
      </p>
    </form>
  );
}
