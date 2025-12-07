import { useAuthStore } from "@/stores/useAuth";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export default function DashboardPage() {
  const { user } = useAuthStore();

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Bienvenue, {user?.name} !</h1>
        <p className="text-muted-foreground">
          Tableau de bord AeroCast - Vue d'ensemble
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Prévisions actives
            </CardTitle>
            <span className="icon-[mdi-light--weather-cloudy] text-2xl text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">12</div>
            <p className="text-xs text-muted-foreground">+2 depuis hier</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Bagages suivis
            </CardTitle>
            <span className="icon-[mdi-light--bag-suitcase] text-2xl text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">245</div>
            <p className="text-xs text-muted-foreground">+19 cette semaine</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Alertes météo</CardTitle>
            <span className="icon-[mdi-light--alert] text-2xl text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">3</div>
            <p className="text-xs text-muted-foreground">
              Nécessitent attention
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Aéroports</CardTitle>
            <span className="icon-[mdi-light--airplane] text-2xl text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">8</div>
            <p className="text-xs text-muted-foreground">Stations actives</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
        <Card className="col-span-4">
          <CardHeader>
            <CardTitle>Activité récente</CardTitle>
            <CardDescription>
              Dernières actions sur la plateforme
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[1, 2, 3, 4].map((i) => (
                <div key={i} className="flex items-center gap-4">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10">
                    <span className="icon-[mdi-light--check] text-xl text-primary" />
                  </div>
                  <div className="flex-1">
                    <p className="text-sm font-medium">Action #{i}</p>
                    <p className="text-xs text-muted-foreground">
                      Il y a {i} heure{i > 1 ? "s" : ""}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card className="col-span-3">
          <CardHeader>
            <CardTitle>Météo du jour</CardTitle>
            <CardDescription>Conditions actuelles</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="text-center">
              <div className="text-5xl font-bold">22°C</div>
              <p className="text-muted-foreground">Partiellement nuageux</p>
            </div>
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Humidité</span>
                <span className="font-medium">65%</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Vent</span>
                <span className="font-medium">12 km/h</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Visibilité</span>
                <span className="font-medium">10 km</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
