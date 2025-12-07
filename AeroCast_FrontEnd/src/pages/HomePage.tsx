import { Link } from "react-router-dom";
import { Cloud, CloudRain, Sun, Wind, MapPin } from "lucide-react";

export default function HomePage() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-b from-primary/10 via-background to-background">
        <div className="container mx-auto px-6 py-24 lg:py-32">
          <div className="flex flex-col items-center text-center">
            <div className="mb-8 flex items-center gap-2">
              <Cloud className="h-12 w-12 text-primary" />
              <h1 className="text-5xl font-bold tracking-tight lg:text-7xl">
                AeroCast
              </h1>
            </div>
            <p className="mb-4 text-xl text-muted-foreground lg:text-2xl max-w-2xl">
              Votre assistant météorologique intelligent
            </p>
            <p className="mb-12 text-lg text-muted-foreground max-w-xl">
              Obtenez des prévisions précises en temps réel pour planifier vos
              journées en toute confiance
            </p>
            <div className="flex flex-col sm:flex-row gap-4">
              <Link
                to="/dashboard"
                className="inline-flex items-center justify-center rounded-lg bg-primary px-8 py-3 text-lg font-semibold text-primary-foreground hover:bg-primary/90 transition-colors"
              >
                Voir la météo
              </Link>
              <Link
                to="/login"
                className="inline-flex items-center justify-center rounded-lg border border-border px-8 py-3 text-lg font-semibold hover:bg-accent transition-colors"
              >
                Se connecter
              </Link>
            </div>
          </div>
        </div>

        {/* Decorative elements */}
        <div className="absolute top-20 left-10 opacity-20">
          <Sun className="h-24 w-24 text-chart-3 animate-pulse" />
        </div>
        <div className="absolute bottom-20 right-10 opacity-20">
          <CloudRain className="h-20 w-20 text-chart-2 animate-bounce" />
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 bg-muted/30">
        <div className="container mx-auto px-6">
          <h2 className="text-3xl font-bold text-center mb-4">
            Fonctionnalités
          </h2>
          <p className="text-center text-muted-foreground mb-16 max-w-2xl mx-auto">
            Tout ce dont vous avez besoin pour rester informé des conditions
            météorologiques
          </p>
          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-4">
            <div className="flex flex-col items-center text-center p-6 rounded-lg bg-card border border-border hover:shadow-lg transition-shadow">
              <div className="mb-4 rounded-full bg-primary/10 p-4">
                <Cloud className="h-8 w-8 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-2">
                Prévisions précises
              </h3>
              <p className="text-muted-foreground">
                Données météo en temps réel mises à jour toutes les heures
              </p>
            </div>

            <div className="flex flex-col items-center text-center p-6 rounded-lg bg-card border border-border hover:shadow-lg transition-shadow">
              <div className="mb-4 rounded-full bg-chart-2/10 p-4">
                <MapPin className="h-8 w-8 text-chart-2" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Multi-localisation</h3>
              <p className="text-muted-foreground">
                Suivez la météo de plusieurs villes simultanément
              </p>
            </div>

            <div className="flex flex-col items-center text-center p-6 rounded-lg bg-card border border-border hover:shadow-lg transition-shadow">
              <div className="mb-4 rounded-full bg-chart-3/10 p-4">
                <Wind className="h-8 w-8 text-chart-3" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Alertes météo</h3>
              <p className="text-muted-foreground">
                Recevez des notifications en cas de conditions extrêmes
              </p>
            </div>

            <div className="flex flex-col items-center text-center p-6 rounded-lg bg-card border border-border hover:shadow-lg transition-shadow">
              <div className="mb-4 rounded-full bg-chart-4/10 p-4">
                <Sun className="h-8 w-8 text-chart-4" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Prévisions 7 jours</h3>
              <p className="text-muted-foreground">
                Planifiez vos activités avec des prévisions détaillées
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24">
        <div className="container mx-auto px-6">
          <div className="rounded-2xl bg-gradient-to-r from-primary/20 via-accent/20 to-primary/20 p-12 text-center">
            <h2 className="text-3xl font-bold mb-4">
              Prêt à découvrir la météo ?
            </h2>
            <p className="text-lg text-muted-foreground mb-8 max-w-2xl mx-auto">
              Commencez dès maintenant à suivre les conditions météorologiques
              de votre région
            </p>
            <Link
              to="/dashboard"
              className="inline-flex items-center justify-center rounded-lg bg-primary px-8 py-3 text-lg font-semibold text-primary-foreground hover:bg-primary/90 transition-colors"
            >
              Commencer maintenant
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border py-8">
        <div className="container mx-auto px-6 text-center text-sm text-muted-foreground">
          <p>© 2025 AeroCast. Tous droits réservés.</p>
        </div>
      </footer>
    </div>
  );
}
