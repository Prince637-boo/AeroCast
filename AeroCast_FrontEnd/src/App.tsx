import {
  createBrowserRouter,
  RouterProvider,
  Navigate,
} from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import RootLayout from "./layouts/RootLayout";
import DashboardLayout from "./layouts/DashboardLayout";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import DashboardPage from "./pages/DashboardPage";
import BaggagePage from "./pages/baggage/BaggagePage";
import { ProtectedRoute } from "./lib/routerGuard";

// Create QueryClient
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      retry: 1,
    },
  },
});

const router = createBrowserRouter([
  {
    path: "/",
    element: <RootLayout />,
    children: [
      // Guest routes (public)
      {
        index: true,
        element: <HomePage />,
      },
      {
        path: "login",
        element: <LoginPage />,
      },
      {
        path: "register",
        element: <RegisterPage />,
      },

      // Dashboard routes (protected)
      {
        path: "dashboard",
        element: (
          <ProtectedRoute>
            <DashboardLayout />
          </ProtectedRoute>
        ),
        children: [
          {
            index: true,
            element: <DashboardPage />,
          },
          {
            path: "bagages",
            children: [
              {
                path: "suivi",
                element: <BaggagePage />,
              },
              {
                path: "scanner",
                element: <div>Scanner Page (à implémenter)</div>,
              },
              {
                path: "incidents",
                element: <div>Incidents Page (à implémenter)</div>,
              },
            ],
          },
          {
            path: "meteo",
            children: [
              {
                path: "predictions",
                element: <div>Predictions Page (à implémenter)</div>,
              },
              {
                path: "alertes",
                element: <div>Alertes Page (à implémenter)</div>,
              },
              {
                path: "aeroports",
                element: <div>Aeroports Page (à implémenter)</div>,
              },
            ],
          },
          {
            path: "statistiques",
            element: <div>Statistiques Page (à implémenter)</div>,
          },
          {
            path: "settings",
            element: <div>Settings Page (à implémenter)</div>,
          },
          {
            path: "profile",
            element: <div>Profile Page (à implémenter)</div>,
          },
        ],
      },

      // Catch all - redirect to home
      {
        path: "*",
        element: <Navigate to="/" replace />,
      },
    ],
  },
]);

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}

export default App;
