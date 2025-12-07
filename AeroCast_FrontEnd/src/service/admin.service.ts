import instance from "./http/instance.http";

export class AdminService {
  static readonly keys = {
    all: ["admin"] as const,
    statistiques: () => [...this.keys.all, "statistiques"] as const,
    logs: () => [...this.keys.all, "logs"] as const,
    sante: () => [...this.keys.all, "sante"] as const,
  };

  static async getStatistiques(params?: Record<string, any>) {
    const { data } = await instance.get("/api/v1/admin/statistiques", {
      params,
    });
    return data;
  }

  static async getLogs(params?: Record<string, any>) {
    const { data } = await instance.get("/api/v1/admin/logs", { params });
    return data;
  }

  static async getSante() {
    const { data } = await instance.get("/api/v1/admin/sante");
    return data;
  }

  static async maintenance(payload: any) {
    const { data } = await instance.post("/api/v1/admin/maintenance", payload);
    return data;
  }
}
