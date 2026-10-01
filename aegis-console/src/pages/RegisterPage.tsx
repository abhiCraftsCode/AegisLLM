import { AuthLayout } from "@/components/auth/AuthLayout";
import { RegisterForm } from "@/features/auth/RegisterForm";

export default function RegisterPage() {
  return (
    <AuthLayout title="Create your account" subtitle="Start protecting your LLM traffic in minutes.">
      <RegisterForm />
    </AuthLayout>
  );
}
