import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { User } from "@/types";

type AuthState = {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
};

type AuthActions = {
  setAuth: (token: string, user: User) => void;
  logout: () => void;
  setLoading: (loading: boolean) => void;
  checkAuth: () => Promise<boolean>;
};

export const useAuthStore = create<AuthState & AuthActions>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: true,

      setAuth: (token: string, user: User) => {
        sessionStorage.setItem("token", token);
        set({ token, user, isAuthenticated: true, isLoading: false });
      },

      logout: () => {
        sessionStorage.removeItem("token");
        set({
          token: null,
          user: null,
          isAuthenticated: false,
          isLoading: false,
        });
      },

      setLoading: (loading: boolean) => {
        set({ isLoading: loading });
      },

      checkAuth: async () => {
        const token = sessionStorage.getItem("token");
        if (!token) {
          set({ isAuthenticated: false, isLoading: false });
          return false;
        }

        try {
          // Mock validation - à remplacer par un vrai appel API
          const payload = JSON.parse(atob(token.split(".")[1]));
          const isExpired = payload.exp * 1000 < Date.now();

          if (isExpired) {
            get().logout();
            return false;
          }

          set({ token, isAuthenticated: true, isLoading: false });
          return true;
        } catch (error) {
          get().logout();
          return false;
        }
      },
    }),
    {
      name: "auth-storage",
      partialize: (state) => ({
        user: state.user,
      }),
    }
  )
);
