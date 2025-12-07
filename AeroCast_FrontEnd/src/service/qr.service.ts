import instance from "./http/instance.http";

export class QrService {
  static readonly keys = {
    all: ["qr"] as const,
    valider: (codeQr: string) => [...this.keys.all, "valider", codeQr] as const,
  };

  static async generer(payload: any) {
    const { data } = await instance.post("/api/v1/qr/generer", payload);
    return data;
  }

  static async valider(codeQr: string) {
    const { data } = await instance.get(`/api/v1/qr/valider/${codeQr}`);
    return data;
  }

  static async telecharger(codeQr: string) {
    const { data } = await instance.get(`/api/v1/qr/telecharger/${codeQr}`, {
      responseType: "blob",
    });
    return data;
  }
}
