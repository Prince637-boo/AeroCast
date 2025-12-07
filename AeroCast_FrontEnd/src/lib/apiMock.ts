import type {
  AuthResponse,
  LoginCredentials,
  RegisterCredentials,
} from "@/types";

// Mock data pour simuler les réponses API
const MOCK_USER = {
  id: "1",
  name: "John Doe",
  email: "john@example.com",
  role: "user",
};

// const MOCK_TOKEN =
//   "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEiLCJlbWFpbCI6ImpvaG5AZXhhbXBsZS5jb20iLCJpYXQiOjE3MzM1NjgwMDAsImV4cCI6MTczMzY1NDQwMH0.abc123";

export async function mockLogin(
  credentials: LoginCredentials
): Promise<AuthResponse> {
  // Simuler un délai réseau
  await new Promise((resolve) => setTimeout(resolve, 1000));

  // Simuler une validation
  if (
    credentials.email === "admin@aerocast.com" &&
    credentials.password === "password123"
  ) {
    // Créer un vrai token JWT avec expiration dans 24h
    const now = Math.floor(Date.now() / 1000);
    const payload = {
      id: MOCK_USER.id,
      email: credentials.email,
      iat: now,
      exp: now + 86400, // 24 heures
    };

    const token = `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.${btoa(
      JSON.stringify(payload)
    )}.signature`;

    return {
      token,
      user: { ...MOCK_USER, email: credentials.email },
    };
  }

  throw new Error("Email ou mot de passe incorrect");
}

export async function mockRegister(
  credentials: RegisterCredentials
): Promise<AuthResponse> {
  // Simuler un délai réseau
  await new Promise((resolve) => setTimeout(resolve, 1500));

  // Créer un token JWT
  const now = Math.floor(Date.now() / 1000);
  const payload = {
    id: "2",
    email: credentials.email,
    iat: now,
    exp: now + 86400,
  };

  const token = `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.${btoa(
    JSON.stringify(payload)
  )}.signature`;

  return {
    token,
    user: {
      id: "2",
      name: credentials.name,
      email: credentials.email,
      numero_passport: credentials.numero_passport,
    },
  };
}

export async function mockCheckAuth(): Promise<boolean> {
  // Simuler une vérification
  await new Promise((resolve) => setTimeout(resolve, 500));
  return true;
}
