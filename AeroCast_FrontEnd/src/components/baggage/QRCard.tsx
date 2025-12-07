import { QRCodeSVG } from "qrcode.react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { Baggage, BaggageStation } from "@/types";

type QRCardProps = {
  baggage: Baggage;
};

export function QRCard({ baggage }: QRCardProps) {
  return (
    <Card className="w-full max-w-md">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>Bagage {baggage.code}</CardTitle>
          <StatusBadge status={baggage.status} />
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* QR Code */}
        <div className="flex flex-col items-center space-y-2">
          <div className="rounded-lg border-4 border-border p-4">
            <QRCodeSVG
              value={baggage.qrCode}
              size={200}
              level="H"
              includeMargin={false}
            />
          </div>
          <p className="text-center font-mono text-lg font-semibold">
            {baggage.code}
          </p>
        </div>

        {/* Informations */}
        <div className="space-y-2 text-sm">
          <div className="flex justify-between">
            <span className="text-muted-foreground">Vol:</span>
            <span className="font-semibold">{baggage.flightNumber}</span>
          </div>
          {baggage.weight && (
            <div className="flex justify-between">
              <span className="text-muted-foreground">Poids:</span>
              <span className="font-semibold">{baggage.weight} kg</span>
            </div>
          )}
        </div>

        {/* Timeline du trajet */}
        <BaggageTimeline route={baggage.route} />
      </CardContent>
    </Card>
  );
}

function StatusBadge({ status }: { status: string }) {
  const variants: Record<string, { variant: any; label: string }> = {
    pending: { variant: "secondary", label: "En attente" },
    in_transit: { variant: "default", label: "En transit" },
    delivered: { variant: "default", label: "Livré" },
    lost: { variant: "destructive", label: "Perdu" },
  };

  const { variant, label } = variants[status] || variants.pending;

  return <Badge variant={variant}>{label}</Badge>;
}

function BaggageTimeline({ route }: { route: BaggageStation[] }) {
  return (
    <div className="space-y-4">
      <h3 className="font-semibold">Suivi du parcours</h3>
      <div className="relative space-y-4">
        {route.map((station, index) => (
          <div key={index} className="relative flex items-start gap-4">
            {/* Ligne de connexion */}
            {index < route.length - 1 && (
              <div className="absolute left-[11px] top-8 h-full w-0.5 bg-border" />
            )}

            {/* Icône */}
            <div
              className={`relative z-10 flex h-6 w-6 items-center justify-center rounded-full border-2 ${
                station.status === "delivered"
                  ? "border-primary bg-primary"
                  : station.status === "in_transit"
                  ? "border-primary bg-background"
                  : "border-border bg-background"
              }`}
            >
              {station.status === "delivered" && (
                <span className="icon-[mdi-light--check] text-primary-foreground" />
              )}
              {station.status === "in_transit" && (
                <div className="h-2 w-2 animate-pulse rounded-full bg-primary" />
              )}
            </div>

            {/* Contenu */}
            <div className="flex-1 pb-4">
              <div className="flex items-center justify-between">
                <p className="font-medium">{station.station}</p>
                {station.time && (
                  <span className="text-xs text-muted-foreground">
                    {station.time}
                  </span>
                )}
              </div>
              {station.location && (
                <p className="text-sm text-muted-foreground">
                  {station.location}
                </p>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
