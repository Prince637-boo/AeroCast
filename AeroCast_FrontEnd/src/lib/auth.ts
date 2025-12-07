import type { TokenPayload } from "@/types";

export function decodeToken(token: string): TokenPayload | null {
  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    return payload;
  } catch (error) {
    console.error("Erreur lors du décodage du token:", error);
    return null;
  }
}

export function isTokenExpired(token: string): boolean {
  const payload = decodeToken(token);
  if (!payload) return true;

  return payload.exp * 1000 < Date.now();
}

export function getToken(): string | null {
  return sessionStorage.getItem("token");
}

export function setToken(token: string): void {
  sessionStorage.setItem("token", token);
}

export function removeToken(): void {
  sessionStorage.removeItem("token");
}

export function checkTokenValidity(): boolean {
  const token = getToken();
  if (!token) return false;

  return !isTokenExpired(token);
}
