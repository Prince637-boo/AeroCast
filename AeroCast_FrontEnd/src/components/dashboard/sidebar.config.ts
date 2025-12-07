export type SidebarItem = {
  title: string;
  href: string;
  icon: string;
  badge?: string | number;
  items?: SidebarItem[];
};

export const sidebarConfig: SidebarItem[] = [
  {
    title: "Dashboard",
    href: "/dashboard",
    icon: "mdi-light--view-dashboard",
  },
  {
    title: "Météo",
    href: "/dashboard/meteo",
    icon: "mdi-light--weather-cloudy",
    items: [
      {
        title: "Prévisions",
        href: "/dashboard/meteo/predictions",
        icon: "mdi-light--chart-line",
      },
      {
        title: "Alertes",
        href: "/dashboard/meteo/alertes",
        icon: "mdi-light--alert",
      },
      {
        title: "Aéroports",
        href: "/dashboard/meteo/aeroports",
        icon: "mdi-light--airplane",
      },
    ],
  },
  {
    title: "Bagages",
    href: "/dashboard/bagages",
    icon: "mdi-light--bag-suitcase",
    items: [
      {
        title: "Suivi",
        href: "/dashboard/bagages/suivi",
        icon: "mdi-light--map-marker",
      },
      {
        title: "Scanner",
        href: "/dashboard/bagages/scanner",
        icon: "mdi-light--qrcode-scan",
      },
      {
        title: "Incidents",
        href: "/dashboard/bagages/incidents",
        icon: "mdi-light--alert-circle",
      },
    ],
  },
  {
    title: "Statistiques",
    href: "/dashboard/statistiques",
    icon: "mdi-light--chart-bar",
  },
  {
    title: "Paramètres",
    href: "/dashboard/settings",
    icon: "mdi-light--cog",
  },
];
