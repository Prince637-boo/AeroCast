import axios from "axios";
import { useAuthStore } from "@/stores/useAuth";
import { toast } from "sonner";

const instance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:3000/api",
  timeout: 10000,
});

// Request interceptor - ajoute le token et vérifie l'expiration
instance.interceptors.request.use(
  (config) => {
    const token = sessionStorage.getItem("token");

    if (token) {
      try {
        // Vérifier l'expiration du token
        const payload = JSON.parse(atob(token.split(".")[1]));
        const isExpired = payload.exp * 1000 < Date.now();

        if (isExpired) {
          // Token expiré - déconnexion
          useAuthStore.getState().logout();
          toast.error("Votre session a expiré", {
            description: "Veuillez vous reconnecter pour continuer.",
          });
          window.location.href = "/login?expired=true";
          return Promise.reject(new Error("Token expiré"));
        }

        // Token valide - ajouter au header
        config.headers.Authorization = `Bearer ${token}`;
      } catch (error) {
        console.error("Erreur lors de la vérification du token:", error);
        useAuthStore.getState().logout();
      }
    }

    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor - gérer les erreurs 401
instance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout();
      toast.error("Session expirée", {
        description: "Veuillez vous reconnecter.",
      });
      window.location.href = "/login?expired=true";
    }
    return Promise.reject(error);
  }
);

export default instance;
