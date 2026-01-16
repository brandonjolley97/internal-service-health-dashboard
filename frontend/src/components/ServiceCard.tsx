import type {Service, ServiceStatus} from "../api";
import { useMemo, useState } from "react";
import { updateServiceStatus } from "../api";
import { StatusBadge } from "./StatusBadge";

type ServiceCardProps = {
    service: Service;
    onUpdated: (updatedService: Service) => void;
};

const ALL_STATUSES: ServiceStatus[] = ["ONLINE","OFFLINE","MAINTENANCE","DEGRADED"];

export function ServiceCard({ service, onUpdated }: ServiceCardProps){

    const [selectedStatus, setSelectedStatus] = useState<ServiceStatus>(service.status);
    const [reason, setReason] = useState<string>(service.degraded_reason ?? "");
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const requiresReason = selectedStatus === "DEGRADED";
    const onlineDisabled = service.status === "OFFLINE";

    const canSave = useMemo(() => {
        if (saving) return false;
        if (requiresReason && reason.trim().length === 0) return false;
        if (selectedStatus === service.status){
            if (requiresReason && (service.degraded_reason ?? "") !== reason) return true;
            return false;
        }

        return true;
    }, [saving, requiresReason, reason, selectedStatus, service.status, service.degraded_reason]);

    async function handleSave() {
        console.log("handleSave start", { id: service.id, selectedStatus, requiresReason, reason });

        setError(null);
        setSaving(true);

        try {
            const payloadReason = requiresReason ? reason : undefined;

            console.log("calling updateServiceStatus", { payloadReason });
            const updated = await updateServiceStatus(service.id, selectedStatus, payloadReason);
            console.log("updateServiceStatus success", updated);

            onUpdated(updated);

            setSelectedStatus(updated.status);
            setReason(updated.degraded_reason ?? "");
        }
        catch (e) {
            console.error("handleSave error", e);
            const msg = e instanceof Error ? e.message : "Failed to update service.";
            setError(msg);
        }
        finally {
            setSaving(false)
            console.log("handleSave end");
        }
    }

    return (
        <div className="rounded-2xl border border-slate-200/70 bg-white p-4 shadow-sm transition-shadow hover:shadow-md">
            {/* This div contains service information and the status badge */}
            <div className="flex items-start justify-between gap-3">
                <div className="min-w-0">
                    <h2 className="truncate text-base font-semibold text-slate-900">{service.name}</h2>
                    <p className="mt-1 line-clamp-2 text-sm text-slate-600">{service.description}</p>
                </div>
                <StatusBadge status={service.status} />
            </div>

            {/* This div contains the status dropdown */}
            <div>
                <label className="block text-xs font-medium text-slate-700">Set status</label>
                <select 
                    className="mt-1 w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-slate-400"
                    value={selectedStatus}
                    onChange={(e) => {
                        setSelectedStatus(e.target.value as ServiceStatus);
                        setError(null);
                    
                    }}
                >
                    {ALL_STATUSES.map((s) => (
                        <option key={s} value={s} disabled={s === "ONLINE" && onlineDisabled}>{s}</option>
                    ))}
                </select>

                {/* This adds note under the dropdown if the current status is OFFLINE */}
                {onlineDisabled && (
                    <p className="mt-1 text-xs text-slate-500">OFFLINE services must go to MAINTENANCE before ONLINE.</p>
                )}
            </div>

            {/* This adds an input field for the degraded reason if DEGRADED is the selected status on the dropdown. */}
            {requiresReason && (
                <div className="mt-3">
                    <label className="block text-xs font-medium text-slate-700"> Reason (required) </label>
                    <input
                        className="mt-1 w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-slate-400"
                        value={reason}
                        onChange={(e) => setReason(e.target.value)}
                        placeholder="Describe"
                    />
                    {reason.trim().length === 0 && (
                        <p className="mt-1 text-xs text-red-600">Enter a reason for changing the status.</p>
                    )}
                </div>
            )}
            
            {/* This div contains the save button and displays the date/time of the last update */}
            <div className="mt-4 flex items-center justify-between gap-3">

                <p className="text-xs text-slate-500">
                    Last updated:{" "}
                    <span className="font-medium">
                        {new Date(service.last_updated).toLocaleString()}
                    </span>
                </p>

                <button
                    className="rounded-lg bg-slate-900 px-3 py-2 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-50"
                    disabled={!canSave}
                    onClick={handleSave}
                >
                    {saving ? "Saving..." : "Save"}
                </button>
            </div>

            {/* Displays errors for ease of debugging */}
            {error && (
                <div className="mt-3 rounded-lg border border-red-200 bg-red-50 p-2 text-sm text-red-700">
                    {error}
                </div>
            )}

        </div>
    );
}