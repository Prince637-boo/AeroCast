import * as v from "valibot";

export const loginSchema = v.object({
  email: v.pipe(v.string("L'email est requis"), v.email("Email invalide")),
  password: v.pipe(
    v.string("Le mot de passe est requis"),
    v.minLength(8, "Le mot de passe doit contenir au moins 8 caractères")
  ),
});

export const registerSchema = v.object({
  name: v.pipe(
    v.string("Le nom est requis"),
    v.minLength(2, "Le nom doit contenir au moins 2 caractères")
  ),
  email: v.pipe(v.string("L'email est requis"), v.email("Email invalide")),
  password: v.pipe(
    v.string("Le mot de passe est requis"),
    v.minLength(8, "Le mot de passe doit contenir au moins 8 caractères")
  ),
  numero_passport: v.pipe(
    v.string("Le numéro de passeport est requis"),
    v.minLength(6, "Le numéro de passeport doit contenir au moins 6 caractères")
  ),
});

export type LoginInput = v.InferInput<typeof loginSchema>;
export type RegisterInput = v.InferInput<typeof registerSchema>;
