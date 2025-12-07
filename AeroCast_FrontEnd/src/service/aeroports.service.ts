import instance from "./http/instance.http";

export class AeroportsService {
  static readonly keys = {
    all: ["aeroports"] as const,
    list: () => [...this.keys.all, "list"] as const,
    detail: (codeAeroport: string) =>
      [...this.keys.all, "detail", codeAeroport] as const,
    pistes: (codeAeroport: string) =>
      [...this.keys.all, "pistes", codeAeroport] as const,
  };

  static async getAll() {
    const { data } = await instance.get("/api/v1/aeroports/");
    return data;
  }

  static async getByCode(codeAeroport: string) {
    const { data } = await instance.get(`/api/v1/aeroports/${codeAeroport}`);
    return data;
  }

  static async getPistes(codeAeroport: string) {
    const { data } = await instance.get(
      `/api/v1/aeroports/${codeAeroport}/pistes`
    );
    return data;
  }
}
