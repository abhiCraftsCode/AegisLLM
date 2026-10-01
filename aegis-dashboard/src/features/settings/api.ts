import { apiClient } from "@/lib/api";
import type { UpdateSchema, PasswordSchema, ProfileSchema } from "@/types/api";

export const userApi = {
  updateProfile: (data: UpdateSchema) => apiClient.patch<ProfileSchema>("/users/update/profile", data),
  updatePassword: (data: PasswordSchema) => apiClient.put<void>("/users/update", data),
};
