const API_BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000";

export type ServiceStatus =
    | "ONLINE"
    | "OFFLINE"
    | "MAINTENANCE"
    | "DEGRADED";


export type Service = {
    id: number;
    name: string;
    description: string;
    status: ServiceStatus;
    last_updated: string;
    degraded_reason: string | null;
};

export async function fetchServices(): Promise<Service[]>{
    const res = await fetch(`${API_BASE}/services`);

    if(!res.ok) {
        const text = await res.text();
        throw new Error(`Failed to fetch services (${res.status}): ${text}`)
    }

    return res.json() as Promise<Service[]>;
}

export async function updateServiceStatus(id: number, status: ServiceStatus, reason?: string): Promise<Service>{
    const bodyContent: Record<string, unknown> = { status };
    if (reason !== undefined) bodyContent.reason = reason;

    const res = await fetch(`${API_BASE}/services/${id}/status`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(bodyContent)
    });
    
    if (!res.ok) {
        const text = await res.text();
        throw new Error(`Failed to update status (${res.status}): ${text}`);
    }

    return res.json() as Promise<Service>;
}
