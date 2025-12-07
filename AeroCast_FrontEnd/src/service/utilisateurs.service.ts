import instance from "./http/instance.http";

export class UtilisateursService {
  static readonly keys = {
    all: ["utilisateurs"] as const,
    permissions: (idUtilisateur: string) =>
      [...this.keys.all, "permissions", idUtilisateur] as const,
  };

  static async getPermissions(idUtilisateur: string) {
    const { data } = await instance.get(
      `/api/v1/utilisateurs/${idUtilisateur}/permissions`
    );
    return data;
  }

  static async updateRole(idUtilisateur: string, payload: { role: string }) {
    const { data } = await instance.patch(
      `/api/v1/utilisateurs/${idUtilisateur}/role`,
      payload
    );
    return data;
  }
}
