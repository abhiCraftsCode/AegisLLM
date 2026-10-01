import type { ProfileSchema, OAuthProvider } from "@/types/api";

export interface AuthContextValue {
  user: ProfileSchema | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (identifier: string, password: string) => Promise<void>;
  register: (data: { name: string; email?: string; phone?: string; password: string }) => Promise<void>;
  loginWithOAuth: (provider: OAuthProvider, code: string) => Promise<void>;
  logout: () => void;
  setUser: (user: ProfileSchema) => void;
}
