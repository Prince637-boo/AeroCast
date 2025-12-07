# AeroCast Frontend - Architecture

## 🏗️ Stack Technique

- **React 19** + **TypeScript**
- **Vite** - Build tool
- **React Router** - Routing
- **TanStack Query** - Data fetching & caching
- **Zustand** - State management
- **Valibot** - Schema validation
- **React Hook Form** - Form management
- **Axios** - HTTP client
- **Shadcn/UI** - Component library
- **Tailwind CSS** - Styling
- **Iconify** - Icons

## 📁 Structure du Projet

```
src/
├── components/          # Composants réutilisables
│   ├── dashboard/      # Composants du dashboard
│   │   ├── DashboardSidebar.tsx
│   │   ├── DashboardHeader.tsx
│   │   └── sidebar.config.ts
│   ├── baggage/        # Composants bagages
│   │   └── QRCard.tsx
│   └── ui/             # Composants shadcn
├── layouts/            # Layouts de pages
│   ├── RootLayout.tsx
│   └── DashboardLayout.tsx
├── pages/              # Pages de l'application
│   ├── HomePage.tsx
│   ├── LoginPage.tsx
│   ├── RegisterPage.tsx
│   ├── DashboardPage.tsx
│   └── baggage/
│       └── BaggagePage.tsx
├── stores/             # Stores Zustand
│   └── useAuth.ts
├── service/            # Services API
│   ├── http/
│   │   └── instance.http.ts
│   ├── auth.service.ts
│   ├── meteo.service.ts
│   ├── bagages.service.ts
│   └── ...
├── lib/                # Utilitaires
│   ├── auth.ts
│   ├── apiMock.ts
│   ├── routerGuard.tsx
│   └── utils.ts
├── schemas/            # Schémas de validation
│   └── auth.schemas.ts
├── types/              # Types TypeScript
│   └── index.ts
└── styles/             # Styles globaux
    └── globals.css
```

## 🔐 Authentification

### Flow d'authentification

1. **Login/Register** : L'utilisateur soumet ses credentials
2. **Mock API** : Simulation d'appel API (à remplacer par vrais appels)
3. **Token JWT** : Stocké dans `sessionStorage`
4. **Zustand Store** : Gère l'état d'authentification
5. **Axios Interceptors** : Vérifie l'expiration avant chaque requête

### Protection des routes

- **ProtectedRoute** : HOC qui vérifie l'authentification
- **Loader** : Affiche un loader pendant la vérification
- **Redirect** : Redirige vers `/login` si non authentifié
- **redirectTo** : Query param pour redirection après login

### Expiration du token

- Vérification automatique avant chaque requête
- Toast notification lors de l'expiration
- Redirection vers login avec message

## 🎨 Composants UI

### Dashboard

- **Sidebar** : Navigation avec sous-menus
- **Header** : User menu + notifications
- **Layout** : Structure avec sidebar collapsible

### Configuration Sidebar

Modifier `src/components/dashboard/sidebar.config.ts` pour ajouter/modifier les menus.

## 📊 TanStack Query

### Configuration

```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      retry: 1,
    },
  },
});
```

### Utilisation dans les services

Chaque service expose des **keys** pour le cache :

```typescript
// Dans meteo.service.ts
static readonly keys = {
  all: ['meteo'] as const,
  predictions: (codeAeroport: string) =>
    [...this.keys.all, 'predictions', codeAeroport] as const,
}

// Utilisation
const { data } = useQuery({
  queryKey: MeteoService.keys.predictions('CDG'),
  queryFn: () => MeteoService.getPredictions('CDG')
})
```

## 🎯 Validation des Formulaires

### Valibot + React Hook Form

```typescript
// 1. Définir le schéma
export const loginSchema = v.object({
  email: v.pipe(v.string(), v.email()),
  password: v.pipe(v.string(), v.minLength(8)),
});

// 2. Utiliser dans le composant
const {
  register,
  handleSubmit,
  formState: { errors },
} = useForm({
  resolver: valibotResolver(loginSchema),
});
```

## 🔔 Notifications (Toast)

Utilisation de **Sonner** pour les notifications :

```typescript
import { toast } from "sonner";

// Success
toast.success("Titre", { description: "Message" });

// Error
toast.error("Erreur", { description: "Message d'erreur" });

// Info
toast.info("Information");
```

## 🎨 Icônes (Iconify)

Utilisation via classes Tailwind :

```tsx
<span className="icon-[mdi-light--home] text-2xl" />
```

Parcourir les icônes : [Iconify Icon Sets](https://icon-sets.iconify.design/)

## 🚀 Routes

### Routes publiques (`/`)

- `/` - Landing page
- `/login` - Connexion
- `/register` - Inscription

### Routes protégées (`/dashboard`)

- `/dashboard` - Vue d'ensemble
- `/dashboard/meteo/*` - Météo
- `/dashboard/bagages/*` - Bagages
- `/dashboard/statistiques` - Statistiques
- `/dashboard/settings` - Paramètres

## 🔧 Configuration

### Variables d'environnement

Créer `.env.local` :

```env
VITE_API_BASE_URL=http://localhost:3000/api
```

### Mock API

Actuellement, toutes les requêtes utilisent des **mock data** dans `src/lib/apiMock.ts`.

**Credentials de test :**

- Email: `admin@aerocast.com`
- Password: `password123`

## 📝 TODO

- [ ] Implémenter les pages manquantes (météo, statistiques, etc.)
- [ ] Remplacer les mock API par de vrais appels
- [ ] Ajouter la gestion des erreurs globale
- [ ] Implémenter le refresh token
- [ ] Ajouter des tests
- [ ] Optimiser les performances
- [ ] Ajouter le mode dark/light toggle
- [ ] Implémenter les WebSockets pour le temps réel

## 🎓 Bonnes Pratiques

1. **Types** : Toujours typer les composants et fonctions
2. **Services** : Toutes les requêtes passent par des services
3. **Keys TanStack** : Utiliser les keys définies dans les services
4. **Validation** : Valider les formulaires avec Valibot
5. **Toast** : Notifier les actions utilisateur
6. **Loading** : Afficher des loaders pendant les requêtes
7. **Error Handling** : Gérer les erreurs gracieusement

## 📚 Documentation

- [React Router](https://reactrouter.com/)
- [TanStack Query](https://tanstack.com/query/)
- [Zustand](https://zustand-demo.pmnd.rs/)
- [Valibot](https://valibot.dev/)
- [Shadcn/UI](https://ui.shadcn.com/)
- [Iconify](https://iconify.design/)
