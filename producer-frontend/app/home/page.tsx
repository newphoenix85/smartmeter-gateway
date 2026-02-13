"use client"

import { title } from "@/components/primitives";
import { getReadingDatas } from "../actions";
import { useEffect, useState } from "react";
import { ISmartlandConsumerRow } from "@/types";
import { ProducerList } from "@/components/list";
import { EnergyChart } from "@/components/chart";
import { BarChart3, Database } from "lucide-react";



export default function HomePage() {

  const [data, setData] = useState<ISmartlandConsumerRow[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const result = await getReadingDatas();
        // result should be an array of objects now (handled in actions.ts)

        const rowsData: ISmartlandConsumerRow[] = []
        if (Array.isArray(result)) {
          for (let index = 0; index < result.length; index++) {
            const element = result[index];
            const row: ISmartlandConsumerRow = {
              key: index,
              id: element.id,
              reading_date: element.ts, // Mapping from backend model
              meter_number: element.meter_id, // Mapping from backend model
              reading_meter_number: element.value, // Mapping from backend model
              upload_date: element.receive_ts, // Mapping from backend model
              user_id: element.user_id
            }
            rowsData.push(row)
          }
        }
        setData(rowsData);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);


  return (
    <section className="flex flex-col items-center justify-center gap-8 py-8 md:py-10 w-full px-6">
      <div className="inline-block max-w-4xl text-center justify-center">
        <span className={title({ color: "violet" })}>Operator View (All Data)</span>
        <br />
        <div className="mt-4 text-violet-300/70 flex items-center justify-center gap-2">
          <div className="px-3 py-1.5 bg-violet-500/20 rounded-lg border border-violet-500/30">
            <span className="text-sm">🔒 Sicherheitsstufe: Hoch (Privilegierter Zugriff)</span>
          </div>
        </div>
      </div>

      {/* Statistics Cards */}
      <div className="w-full max-w-7xl grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        <div className="bg-gradient-to-br from-violet-950/40 to-purple-900/30 backdrop-blur-sm rounded-xl p-6 border border-violet-500/20">
          <div className="flex items-center gap-3">
            <Database className="w-8 h-8 text-violet-400" />
            <div>
              <p className="text-sm text-violet-300/70">Gesamt Messungen</p>
              <p className="text-2xl font-bold text-violet-100">{data.length}</p>
            </div>
          </div>
        </div>
        <div className="bg-gradient-to-br from-blue-950/40 to-blue-900/30 backdrop-blur-sm rounded-xl p-6 border border-blue-500/20">
          <div className="flex items-center gap-3">
            <BarChart3 className="w-8 h-8 text-blue-400" />
            <div>
              <p className="text-sm text-blue-300/70">Aktive Kunden</p>
              <p className="text-2xl font-bold text-blue-100">
                {new Set(data.map(d => d.user_id)).size}
              </p>
            </div>
          </div>
        </div>
        <div className="bg-gradient-to-br from-green-950/40 to-green-900/30 backdrop-blur-sm rounded-xl p-6 border border-green-500/20">
          <div className="flex items-center gap-3">
            <BarChart3 className="w-8 h-8 text-green-400" />
            <div>
              <p className="text-sm text-green-300/70">Letzter Wert</p>
              <p className="text-2xl font-bold text-green-100">
                {data.length > 0 ? `${data[0].reading_meter_number} kWh` : 'N/A'}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Chart Section */}
      {!loading && data.length > 0 && (
        <div className="w-full max-w-7xl">
          <EnergyChart data={data} />
        </div>
      )}

      {/* Table Section */}
      <div className="w-full max-w-7xl">
        <div className="bg-gradient-to-br from-violet-950/20 to-purple-900/10 backdrop-blur-sm rounded-2xl p-6 border border-violet-500/20">
          <h3 className="text-xl font-bold text-violet-100 mb-4">Detaillierte Messdaten</h3>
          <ProducerList allDatas={data} />
        </div>
      </div>

    </section>
  );
}
