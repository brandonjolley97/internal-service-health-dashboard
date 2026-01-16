import { useEffect, useState } from 'react';
import type { Service } from "./api";
import { fetchServices } from './api';
import { ServiceCard } from "./components/ServiceCard";

export default function App() {

  const [services, setServices] = useState<Service[]>([]);
  const [loading, setLoading] = useState(true); 
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      try {
        setError(null);
        const data = await fetchServices();
        setServices(data);
      }
      catch (e) {
        setError(e instanceof Error ? e.message : "Failed to load services.");
      }
      finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  function handleUpdated(updated: Service){
    setServices((prev) => prev.map((s) => (s.id === updated.id ? updated : s)));
  }

  return (
    <div className="min-h-screen bg-slate-50 p-6">
      <div className="mx-auto max-w-6xl space-y-6">
        <header className="flex items-baseline justify-between gap-4">
          <h1 className="text-2xl font-bold text-slate-900">Service Health Dashboard</h1>
          <p className="text-sm text-slate-600">Internal admin view</p>
        </header>

        {loading && <p className="text-slate-700">Loading services…</p>}

        {error && (
          <div className="rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700">
            {error}
          </div>
        )}

        {!loading && !error && services.length === 0 && (
          <p className="text-slate-700"></p>
        )}

        {!loading && !error && services.length > 0 && (
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {services.map((s) => (
              <ServiceCard key={s.id} service={s} onUpdated={handleUpdated} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
