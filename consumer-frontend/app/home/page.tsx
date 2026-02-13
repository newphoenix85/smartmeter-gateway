"use client"

import { ConsumerDeatils } from "@/components/details";
import { ConsumerList } from "@/components/list";
import { subtitle } from "@/components/primitives";
import { Button, Image } from "@heroui/react";
import { useEffect, useState } from "react";
import { getLastData, getReadingDatas, testProducer } from "../actions";
import { ISmartlandSMGW, ISmartlandSMGWRow } from "@/types";

import { EnergyChart } from "@/components/chart";
import { BarChart3, Database, TrendingUp } from "lucide-react";




export default function HomePage() {
  const [newValues, setNewValues] = useState<boolean>(false);
  const [lastData, setLastData] = useState<ISmartlandSMGWRow | undefined>()
  const [allData, setAllData] = useState<ISmartlandSMGWRow[] | undefined>()


  const parseResult = (result: string): ISmartlandSMGWRow | undefined => {
    const parseOne = JSON.parse(result)
    let returnObj: ISmartlandSMGWRow | undefined
    if (Object.keys(parseOne).length > 0) {
      const transformJSON: ISmartlandSMGW = JSON.parse(parseOne)
      returnObj = {
        key: 0,
        id: transformJSON.id,
        user_id: transformJSON.user_id,
        ts: new Date(transformJSON.ts),
        meter_id: transformJSON.meter_id,
        value: transformJSON.value,
        unit: transformJSON.unit,
        obis: transformJSON.obis,
        receive_ts: new Date(transformJSON.receive_ts)
      }
    }
    return returnObj
  }

  const parseResponse = (result: string) => {
    const returnArray: ISmartlandSMGWRow[] = []
    const parseFirstLevelJSON: [] = JSON.parse(result)
    const lenghtFirstLevel = parseFirstLevelJSON.length
    for (let index = 0; index < lenghtFirstLevel; index++) {
      const element = parseFirstLevelJSON[index];
      const nextLevel: ISmartlandSMGW = JSON.parse(element)
      returnArray.push({
        key: index,
        id: nextLevel.id,
        user_id: nextLevel.user_id,
        ts: new Date(nextLevel.ts),
        meter_id: nextLevel.meter_id,
        value: nextLevel.value,
        unit: nextLevel.unit,
        obis: nextLevel.obis,
        receive_ts: new Date(nextLevel.receive_ts)
      })

    }
    return returnArray

  }


  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await getLastData();
        setLastData(parseResult(result))
      } catch (error) {
        console.error('Error fetching last data:', error);
      }
    };
    fetchData();

    const fetchAllData = async () => {
      try {
        const result = await getReadingDatas();
        setAllData(parseResponse(result))
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchAllData();
    setNewValues(false);
  }, [newValues])

  // Transform data for chart
  const chartData = allData?.map((item, idx) => ({
    key: idx,
    id: item.id,
    reading_date: item.ts.toISOString(),
    meter_number: item.meter_id,
    reading_meter_number: item.value.toString(),
    upload_date: item.receive_ts.toISOString(),
    user_id: item.user_id
  })) || [];


  return (
    <section className="flex w-full flex-col items-stretch gap-6 px-6 py-8">
      {/* Statistics Cards */}
      <div className="w-full grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-gradient-to-br from-violet-950/40 to-purple-900/30 backdrop-blur-sm rounded-xl p-6 border border-violet-500/20">
          <div className="flex items-center gap-3">
            <Database className="w-8 h-8 text-violet-400" />
            <div>
              <p className="text-sm text-violet-300/70">Gesamt Messungen</p>
              <p className="text-2xl font-bold text-violet-100">{allData?.length || 0}</p>
            </div>
          </div>
        </div>
        <div className="bg-gradient-to-br from-blue-950/40 to-blue-900/30 backdrop-blur-sm rounded-xl p-6 border border-blue-500/20">
          <div className="flex items-center gap-3">
            <TrendingUp className="w-8 h-8 text-blue-400" />
            <div>
              <p className="text-sm text-blue-300/70">Aktueller Wert</p>
              <p className="text-2xl font-bold text-blue-100">
                {lastData ? `${lastData.value} ${lastData.unit}` : 'N/A'}
              </p>
            </div>
          </div>
        </div>
        <div className="bg-gradient-to-br from-green-950/40 to-green-900/30 backdrop-blur-sm rounded-xl p-6 border border-green-500/20">
          <div className="flex items-center gap-3">
            <BarChart3 className="w-8 h-8 text-green-400" />
            <div>
              <p className="text-sm text-green-300/70">Zählernummer</p>
              <p className="text-2xl font-bold text-green-100">
                {lastData?.meter_id || 'N/A'}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Chart Section */}
      {chartData.length > 0 && (
        <div className="w-full">
          <EnergyChart data={chartData} />
        </div>
      )}

      <div className="w-full mt-2 -mb-3">
        <div className="grid gap-4 w-full">
          <div className="relative w-full">
            <div className="absolute inset-px rounded-lg bg-white dark:bg-zinc-900 w-full"></div>
            <div className="relative flex h-full flex-col overflow-hidden rounded-[calc(theme(borderRadius.lg)+1px)] px-2 py-4 w-full">
              <ConsumerDeatils lastData={lastData} />
            </div>
            <div className="pointer-events-none absolute inset-px rounded-lg shadow ring-1 ring-black/5 w-full"></div>
          </div>
          <div className="relative w-full flex justify-center items-center">
            <div className="px-8 pt-8 sm:px-10 sm:pt-10 flex flex-col items-center justify-center gap-4 text-center">
              <div className="p-4 rounded-lg bg-yellow-500/10 border border-yellow-500/20">
                <p className="text-yellow-200 text-sm">
                  <strong>Hinweis:</strong> Die manuelle Dateneingabe wurde aus Sicherheitsgründen deaktiviert.
                  Ihre Zählerstände werden nun vollautomatisch über das Smart Meter Gateway übertragen.
                </p>
              </div>
            </div>
            <div className="pointer-events-none absolute inset-px rounded-lg shadow ring-1 ring-black/5 w-full"></div>
          </div>


          <div className="relative w-full">
            <div className="relative flex flex-col overflow-hidden rounded-[calc(theme(borderRadius.lg)+1px)] w-full">
              <div className="px-8 pb-3 pt-8 sm:px-10 sm:pb-0 sm:pt-10 w-full">
                <span className={subtitle({ color: "yellow" })}>Ihre letzten Zählerstände&nbsp;</span>
              </div>
              <div className="relative min-h-[30rem] w-full grow">
                <ConsumerList allDatas={allData} />
              </div>
            </div>
            <div className="pointer-events-none absolute inset-px rounded-lg shadow ring-1 ring-black/5 w-full"></div>
          </div>
        </div>
      </div>
      <br></br>

    </section>
  );
}
