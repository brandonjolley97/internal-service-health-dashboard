import type {ServiceStatus} from "../api"

type StatusBadgeProps = {
    status: ServiceStatus;
};

export function StatusBadge({ status }: StatusBadgeProps) {
    const base = 
        "inline-flex items-center rounded-full" 
        "px-3 py-1.5 text-xs font-semibold ring-1 ring-inset";

    const variant = 
        status === "ONLINE" ? "bg-green-100 text-green-700 ring-green-600/20"
        : status === "OFFLINE" ? "bg-red-100 text-red-700 ring-red-600/20"
        : "bg-yellow-100 text-yellow-800 ring-yellow-600/20"; 

    return <span className={`${base} ${variant}`}>{status}</span>;
}