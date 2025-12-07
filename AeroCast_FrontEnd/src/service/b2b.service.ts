import instance from "./http/instance.http";

export class B2BService {
  static readonly keys = {
    all: ["b2b"] as const,
    documentation: () => [...this.keys.all, "documentation"] as const,
  };

  static async meteoLot(payload: any) {
    const { data } = await instance.post("/api/v1/b2b/meteo/lot", payload);
    return data;
  }

  static async scannerLot(payload: any) {
    const { data } = await instance.post(
      "/api/v1/b2b/bagages/scanner-lot",
      payload
    );
    return data;
  }

  static async getDocumentation() {
    const { data } = await instance.get("/api/v1/b2b/documentation");
    return data;
  }

  static async configurerWebhook(payload: any) {
    const { data } = await instance.post(
      "/api/v1/b2b/webhook/configurer",
      payload
    );
    return data;
  }
}
