import { SignupForm } from "@/components/signup-form";

const RegisterPage = () => {
  return (
    <div className="flex min-h-screen items-center justify-center p-6 bg-gradient-to-br from-primary/5 via-background to-accent/5">
      <div className="w-full max-w-md">
        <h1 className="text-3xl font-bold mb-6 text-center">Créer un compte</h1>
        <SignupForm className="w-full max-w-lg" />
      </div>
    </div>
  );
};

export default RegisterPage;
