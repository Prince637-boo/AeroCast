import instance from "./http/instance.http";

export class AuthService {
  static readonly keys = {
    all: ["auth"] as const,
    profil: () => [...this.keys.all, "profil"] as const,
  };

  static async inscription(payload: {
    numero_passport: string;
    nom: string;
    email: string;
    password: string;
  }) {
    const { data } = await instance.post("/api/v1/auth/inscription", payload);
    return data;
  }

  static async connexion(payload: { email: string; password: string }) {
    const { data } = await instance.post("/api/v1/auth/connexion", payload);
    return data;
  }

  static async rafraichir() {
    const { data } = await instance.post("/api/v1/auth/rafraichir");
    return data;
  }

  static async getProfil() {
    const { data } = await instance.get("/api/v1/auth/profil");
    return data;
  }

  static async deconnexion() {
    const { data } = await instance.post("/api/v1/auth/deconnexion");
    return data;
  }
}
