import { AuthLayout } from "@/components/auth/AuthLayout";
import { LoginForm } from "@/features/auth/LoginForm";

export default function LoginPage() {
  return (
    <AuthLayout title="Welcome back" subtitle="Sign in to your AegisLLM workspace.">
      <LoginForm />
    </AuthLayout>
  );
}
