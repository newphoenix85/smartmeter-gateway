import { ISmartlandSMGWRow } from "@/types";
import { Card, CardHeader, Chip } from "@heroui/react";
import { Calendar, Cctv, HousePlug, Zap } from "lucide-react";
import { useEffect } from "react";
import { subtitle } from "./primitives";


export const ConsumerDeatils = ({lastData}: {lastData: ISmartlandSMGWRow | undefined}) => {
    

    useEffect(() => {
        
      }, [lastData]);

    const getNextReadingDate = (readingDate: Date): Date => {
        const dateInFuture = readingDate 
       return new Date(dateInFuture.setFullYear(new Date().getFullYear() + 1))
    }

    return (
        <div className="relative min-h-[30rem] w-full grow [container-type:inline-size] max-lg:mx-auto max-lg:max-w-sm gap-2 grid grid-cols-1 grid-rows-4 px-8">
            { lastData ? <>
            <Card className="col-span-12 sm:col-span-4 dark:bg-zinc-950 bg-zinc-50">
                <CardHeader className="absolute z-10 top-1 flex-col !items-start">
                <h4 className={subtitle({ color: "yellow" })}>Nächster Ablesetermin</h4>
                <Chip radius="sm" size="lg" color="warning" startContent={<Cctv size={18} />} variant="bordered">
                {getNextReadingDate(lastData.ts).toLocaleDateString()}
                </Chip>
                </CardHeader>
            </Card>
            <Card className="col-span-12 sm:col-span-4 dark:bg-zinc-950 bg-zinc-50">
                <CardHeader className="absolute z-10 top-1 flex-col !items-start">
                <h4 className={subtitle({ color: "yellow" })}>Letztes Ablesedatum</h4>
                <Chip radius="sm" size="lg" color="warning" startContent={<Calendar size={18} />} variant="bordered">
                    {lastData.ts.toLocaleDateString()}
                </Chip>
                </CardHeader>
            </Card>
            <Card className="col-span-12 sm:col-span-4 dark:bg-zinc-950 bg-zinc-50">
                <CardHeader className="absolute z-10 top-1 flex-col !items-start">
                <h4 className={subtitle({ color: "yellow" })}>Letzter Zählerstand</h4>
                <Chip radius="sm" size="lg" color="warning" startContent={<Zap size={18} />} variant="bordered">
                    {lastData.value} kWh
                </Chip>
                </CardHeader>
            </Card>
            <Card className="col-span-12 sm:col-span-4 dark:bg-zinc-950 bg-zinc-50">
                <CardHeader className="absolute z-10 top-1 flex-col items-start">
                    <h4 className={subtitle({ color: "yellow" })}>Zählernummer</h4>
                    <Chip radius="sm" size="lg" color="warning" startContent={<HousePlug size={18} />} variant="bordered">
                    {lastData.meter_id}
                    </Chip>
                </CardHeader>
            </Card>
          </>
            : 
            <span>Keine Daten verfügbar</span>
            }       
        </div>
    )
}