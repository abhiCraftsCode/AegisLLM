import { useState, type FormEvent } from "react";
import { Input } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";
import { useAuth } from "@/hooks/useAuth";
import { useToast } from "@/components/ui/Toast";
import { userApi } from "./api";
import { ApiError } from "@/lib/api";

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const PHONE_RE = /^(\+91)?[6-9]\d{9}$/;

export function ProfileForm() {
  const { user, setUser } = useAuth();
  const { toast } = useToast();

  const [name, setName] = useState(user?.name ?? "");
  const [email, setEmail] = useState(user?.email ?? "");
  const [phone, setPhone] = useState(user?.phone ?? "");
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (!user) return null;

  function validate(): boolean {
    const next: Record<string, string> = {};
    if (name.trim().length < 2) next.name = "Name must be at least 2 characters.";
    if (email.trim() && !EMAIL_RE.test(email.trim())) next.email = "Enter a valid email address.";
    if (phone.trim() && !PHONE_RE.test(phone.trim().replace(/\s/g, ""))) {
      next.phone = "Enter a valid Indian mobile number.";
    }
    setErrors(next);
    return Object.keys(next).length === 0;
  }

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    if (!validate() || isSubmitting || !user) return;
    setIsSubmitting(true);
    try {
      const payload: Record<string, string> = {};
      if (name.trim() !== user.name) payload.name = name.trim();
      if (email.trim() !== (user.email ?? "")) payload.email = email.trim();
      if (phone.trim() !== (user.phone ?? "")) payload.phone = phone.trim();

      const updated = await userApi.updateProfile(payload);
      setUser(updated);
      toast("Profile updated", "success");
    } catch (err) {
      toast(err instanceof ApiError ? err.message : "Couldn't update your profile.", "error");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <form onSubmit={onSubmit} noValidate className="flex flex-col gap-4">
      <Input label="Name" name="name" value={name} onChange={(e) => setName(e.target.value)} error={errors.name} />
      <Input label="Email" name="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} error={errors.email} />
      <Input
        label="Phone"
        name="phone"
        type="tel"
        value={phone}
        onChange={(e) => setPhone(e.target.value)}
        error={errors.phone}
        hint="Indian mobile number"
      />
      <div className="flex justify-end">
        <Button type="submit" size="sm" isLoading={isSubmitting}>
          {isSubmitting ? "Saving..." : "Save Changes"}
        </Button>
      </div>
    </form>
  );
}
