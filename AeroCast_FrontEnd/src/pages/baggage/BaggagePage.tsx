import { QRCard } from "@/components/baggage/QRCard";
import type { Baggage } from "@/types";

// Mock data
const mockBaggage: Baggage = {
  id: "1",
  code: "BAG-2024-001",
  qrCode: "BAG-2024-001",
  flightNumber: "AF123",
  owner: "John Doe",
  weight: 23.5,
  status: "in_transit",
  route: [
    {
      station: "Enregistrement",
      time: "10:30",
      status: "delivered",
      location: "Comptoir 12, Terminal 2E",
    },
    {
      station: "Contrôle sécurité",
      time: "10:45",
      status: "delivered",
      location: "Zone de tri",
    },
    {
      station: "En cours de chargement",
      time: "11:20",
      status: "in_transit",
      location: "Aire de trafic A3",
    },
    {
      station: "En vol",
      status: "pending",
      location: "Vol AF123 vers JFK",
    },
    {
      station: "Arrivée",
      status: "pending",
      location: "Terminal 1, JFK",
    },
  ],
};

export default function BaggagePage() {
  return (
    <div className="container mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Suivi de bagage</h1>
        <p className="text-muted-foreground">
          Suivez en temps réel le parcours de votre bagage
        </p>
      </div>

      <div className="flex justify-center">
        <QRCard baggage={mockBaggage} />
      </div>
    </div>
  );
}
