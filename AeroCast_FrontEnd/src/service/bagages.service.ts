import instance from "./http/instance.http";

export class BagagesService {
  static readonly keys = {
    all: ["bagages"] as const,
    detail: (idBagage: string) =>
      [...this.keys.all, "detail", idBagage] as const,
    byQr: (codeQr: string) => [...this.keys.all, "qr", codeQr] as const,
    byVol: (numeroVol: string) => [...this.keys.all, "vol", numeroVol] as const,
    historique: (idBagage: string) =>
      [...this.keys.all, "historique", idBagage] as const,
    statistiques: (numeroVol: string) =>
      [...this.keys.all, "statistiques", numeroVol] as const,
  };

  static async enregistrer(payload: any) {
    const { data } = await instance.post(
      "/api/v1/bagages/enregistrer",
      payload
    );
    return data;
  }

  static async getById(idBagage: string) {
    const { data } = await instance.get(`/api/v1/bagages/${idBagage}`);
    return data;
  }

  static async getByQr(codeQr: string) {
    const { data } = await instance.get(`/api/v1/bagages/qr/${codeQr}`);
    return data;
  }

  static async getByVol(numeroVol: string) {
    const { data } = await instance.get(`/api/v1/bagages/vol/${numeroVol}`);
    return data;
  }

  static async scanner(payload: any) {
    const { data } = await instance.post("/api/v1/bagages/scanner", payload);
    return data;
  }

  static async getHistorique(idBagage: string) {
    const { data } = await instance.get(
      `/api/v1/bagages/${idBagage}/historique`
    );
    return data;
  }

  static async signalerIncident(idBagage: string, payload: any) {
    const { data } = await instance.post(
      `/api/v1/bagages/${idBagage}/incident`,
      payload
    );
    return data;
  }

  static async getStatistiques(numeroVol: string) {
    const { data } = await instance.get(
      `/api/v1/bagages/statistiques/vol/${numeroVol}`
    );
    return data;
  }
}
