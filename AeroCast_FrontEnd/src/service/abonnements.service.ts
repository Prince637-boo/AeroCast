import instance from "./http/instance.http";

export class AbonnementsService {
  static readonly keys = {
    all: ["abonnements"] as const,
    forfaits: () => [...this.keys.all, "forfaits"] as const,
    utilisation: (idCompagnie: string) =>
      [...this.keys.all, "utilisation", idCompagnie] as const,
    facturation: (idCompagnie: string) =>
      [...this.keys.all, "facturation", idCompagnie] as const,
  };

  static async getForfaits() {
    const { data } = await instance.get("/api/v1/abonnements/forfaits");
    return data;
  }

  static async souscrire(payload: any) {
    const { data } = await instance.post(
      "/api/v1/abonnements/souscrire",
      payload
    );
    return data;
  }

  static async getUtilisation(idCompagnie: string) {
    const { data } = await instance.get(
      `/api/v1/abonnements/${idCompagnie}/utilisation`
    );
    return data;
  }

  static async getFacturation(idCompagnie: string) {
    const { data } = await instance.get(
      `/api/v1/abonnements/${idCompagnie}/facturation`
    );
    return data;
  }
}
