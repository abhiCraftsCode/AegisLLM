import { createContext, useCallback, useEffect, useState, type ReactNode } from "react";
import type { ProfileSchema, OAuthProvider } from "@/types/api";
import { ACCESS_TOKEN_KEY, REFRESH_TOKEN_KEY } from "@/lib/constants";
import { UNAUTHORIZED_EVENT } from "@/lib/api";
import { authApi } from "./api";
import type { AuthContextValue } from "./types";

export const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUserState] = useState<ProfileSchema | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const clearSession = useCallback(() => {
    localStorage.removeItem(ACCESS_TOKEN_KEY);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
    setUserState(null);
  }, []);

  useEffect(() => {
    const token = localStorage.getItem(ACCESS_TOKEN_KEY);
    if (!token) {
      setIsLoading(false);
      return;
    }
    authApi
      .me()
      .then((profile) => setUserState(profile))
      .catch(() => clearSession())
      .finally(() => setIsLoading(false));
  }, [clearSession]);

  useEffect(() => {
    const handler = () => clearSession();
    window.addEventListener(UNAUTHORIZED_EVENT, handler);
    return () => window.removeEventListener(UNAUTHORIZED_EVENT, handler);
  }, [clearSession]);

  const login = useCallback(async (identifier: string, password: string) => {
    const res = await authApi.login({ identifier, password });
    localStorage.setItem(ACCESS_TOKEN_KEY, res.tokens.access_token);
    localStorage.setItem(REFRESH_TOKEN_KEY, res.tokens.refresh_token);
    setUserState(res.user);
  }, []);

  const register = useCallback(
    async (data: { name: string; email?: string; phone?: string; password: string }) => {
      const res = await authApi.register(data);
      localStorage.setItem(ACCESS_TOKEN_KEY, res.tokens.access_token);
      localStorage.setItem(REFRESH_TOKEN_KEY, res.tokens.refresh_token);
      setUserState(res.user);
    },
    []
  );

  const loginWithOAuth = useCallback(async (provider: OAuthProvider, code: string) => {
    const res = await authApi.oauth({ provider, code });
    localStorage.setItem(ACCESS_TOKEN_KEY, res.tokens.access_token);
    localStorage.setItem(REFRESH_TOKEN_KEY, res.tokens.refresh_token);
    setUserState(res.user);
  }, []);

  const logout = useCallback(() => {
    clearSession();
  }, [clearSession]);

  const setUser = useCallback((u: ProfileSchema) => setUserState(u), []);

  const value: AuthContextValue = {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    register,
    loginWithOAuth,
    logout,
    setUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
