import { apiClient } from "@/lib/api";
import type {
  AuthResponse,
  LoginSchema,
  RegisterSchema,
  ForgotSchema,
  ResetSchema,
  ProfileSchema,
  OauthLoginSchema,
} from "@/types/api";

export const authApi = {
  login: (data: LoginSchema) => apiClient.post<AuthResponse>("/auth/login", data, { auth: false }),

  register: (data: RegisterSchema) =>
    apiClient.post<AuthResponse>("/auth/register", data, { auth: false }),

  forgotPassword: (data: ForgotSchema) =>
    apiClient.post<void>("/auth/forgot-password", data, { auth: false }),

  resetPassword: (data: ResetSchema) =>
    apiClient.post<void>("/auth/reset-password", data, { auth: false }),

  me: () => apiClient.get<ProfileSchema>("/users/me"),

  oauth: (data: OauthLoginSchema) => apiClient.post<AuthResponse>("/auth/oauth", data, { auth: false }),
};
