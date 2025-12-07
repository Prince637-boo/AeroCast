export type User = {
  id: string;
  name: string;
  email: string;
  role?: string;
  numero_passport?: string;
};

export type AuthResponse = {
  token: string;
  user: User;
};

export type TokenPayload = {
  id: string;
  email: string;
  iat: number;
  exp: number;
};

export type BaggageStatus = "pending" | "in_transit" | "delivered" | "lost";

export type BaggageStation = {
  station: string;
  time?: string;
  status: BaggageStatus;
  location?: string;
};

export type Baggage = {
  id: string;
  code: string;
  qrCode: string;
  route: BaggageStation[];
  owner: string;
  flightNumber: string;
  weight?: number;
  status: BaggageStatus;
};

export type LoginCredentials = {
  email: string;
  password: string;
};

export type RegisterCredentials = {
  name: string;
  email: string;
  password: string;
  numero_passport: string;
};
