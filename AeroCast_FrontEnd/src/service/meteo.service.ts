import instance from "./http/instance.http";

export class MeteoService {
  static readonly keys = {
    all: ["meteo"] as const,
    predictions: (codeAeroport: string) =>
      [...this.keys.all, "predictions", codeAeroport] as const,
    predictionsPiste: (codeAeroport: string, idPiste: string) =>
      [
        ...this.keys.all,
        "predictions",
        codeAeroport,
        "piste",
        idPiste,
      ] as const,
    alertes: (codeAeroport: string) =>
      [...this.keys.all, "alertes", codeAeroport] as const,
    comparer: () => [...this.keys.all, "comparer"] as const,
    statut: () => [...this.keys.all, "statut"] as const,
  };

  static async getPredictions(codeAeroport: string) {
    const { data } = await instance.get(
      `/api/v1/meteo/predictions/${codeAeroport}`
    );
    return data;
  }

  static async getPredictionsPiste(codeAeroport: string, idPiste: string) {
    const { data } = await instance.get(
      `/api/v1/meteo/predictions/${codeAeroport}/piste/${idPiste}`
    );
    return data;
  }

  static async getAlertes(codeAeroport: string) {
    const { data } = await instance.get(
      `/api/v1/meteo/alertes/${codeAeroport}`
    );
    return data;
  }

  static async comparer(params: Record<string, any>) {
    const { data } = await instance.get("/api/v1/meteo/comparer", { params });
    return data;
  }

  static async declencherMiseAJour() {
    const { data } = await instance.post(
      "/api/v1/meteo/declencher-mise-a-jour"
    );
    return data;
  }

  static async getStatut() {
    const { data } = await instance.get("/api/v1/meteo/statut");
    return data;
  }
}
