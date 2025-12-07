import { Link, useNavigate } from "react-router-dom";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldLabel,
} from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { useForm } from "react-hook-form";
import { valibotResolver } from "@hookform/resolvers/valibot";
import { registerSchema, type RegisterInput } from "@/schemas/auth.schemas";
import { mockRegister } from "@/lib/apiMock";
import { useAuthStore } from "@/stores/useAuth";
import { useState } from "react";

export function SignupForm({ ...props }: React.ComponentProps<typeof Card>) {
  const navigate = useNavigate();
  const { setAuth } = useAuthStore();
  const [error, setError] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterInput>({
    resolver: valibotResolver(registerSchema),
  });

  const onSubmit = async (data: RegisterInput) => {
    setIsLoading(true);
    setError("");

    try {
      // Mock API call
      const response = await mockRegister(data);
      setAuth(response.token, response.user);

      toast.success("Compte créé avec succès !", {
        description: `Bienvenue sur AeroCast, ${response.user.name}`,
      });

      // Redirect to dashboard
      navigate("/dashboard");
    } catch (err) {
      const message =
        err instanceof Error ? err.message : "Erreur lors de l'inscription";
      setError(message);
      toast.error("Erreur d'inscription", {
        description: message,
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card {...props}>
      <CardHeader>
        <CardTitle>Créer un compte</CardTitle>
        <CardDescription>
          Rejoignez AeroCast pour suivre vos prévisions météo personnalisées
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit(onSubmit)}>
          <FieldGroup>
            {error && (
              <div className="rounded-md bg-destructive/10 p-3 text-sm text-destructive">
                {error}
              </div>
            )}

            <Field>
              <FieldLabel htmlFor="name">Nom complet</FieldLabel>
              <Input
                id="name"
                type="text"
                placeholder="Jean Dupont"
                {...register("name")}
              />
              {errors.name && (
                <FieldDescription className="text-destructive">
                  {errors.name.message}
                </FieldDescription>
              )}
            </Field>

            <Field>
              <FieldLabel htmlFor="email">Email</FieldLabel>
              <Input
                id="email"
                type="email"
                placeholder="jean@exemple.com"
                {...register("email")}
              />
              {errors.email && (
                <FieldDescription className="text-destructive">
                  {errors.email.message}
                </FieldDescription>
              )}
              <FieldDescription>
                Nous utiliserons cet email pour vous contacter.
              </FieldDescription>
            </Field>

            <Field>
              <FieldLabel htmlFor="password">Mot de passe</FieldLabel>
              <Input id="password" type="password" {...register("password")} />
              {errors.password && (
                <FieldDescription className="text-destructive">
                  {errors.password.message}
                </FieldDescription>
              )}
              <FieldDescription>Minimum 8 caractères.</FieldDescription>
            </Field>

            <Field>
              <FieldLabel htmlFor="numero_passport">
                Numéro de passeport
              </FieldLabel>
              <Input
                id="numero_passport"
                type="text"
                placeholder="ABC123456"
                {...register("numero_passport")}
              />
              {errors.numero_passport && (
                <FieldDescription className="text-destructive">
                  {errors.numero_passport.message}
                </FieldDescription>
              )}
            </Field>

            <FieldGroup>
              <Field>
                <Button type="submit" className="w-full" disabled={isLoading}>
                  {isLoading ? "Création..." : "Créer mon compte"}
                </Button>
                <Button variant="outline" type="button" className="w-full">
                  S&apos;inscrire avec Google
                </Button>
                <FieldDescription className="px-6 text-center">
                  Vous avez déjà un compte ?{" "}
                  <Link to="/login" className="text-primary hover:underline">
                    Se connecter
                  </Link>
                </FieldDescription>
              </Field>
            </FieldGroup>
          </FieldGroup>
        </form>
      </CardContent>
    </Card>
  );
}
