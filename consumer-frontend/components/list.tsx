import { getReadingDatas } from "@/app/actions";
import { ISmartlandSMGW, ISmartlandSMGWRow } from "@/types";
import { Chip, Table, TableBody, TableCell, TableColumn, TableHeader, TableRow } from "@heroui/react";
import { HousePlug, Zap } from "lucide-react";
import { useEffect, useState } from "react";




export const columns = [
    {name: "Ablesetag", uid: "readingDay"},
    {name: "Zählerstand", uid: "readingValue"},
    {name: "Zählernummer", uid: "meterId"}
  ];
  

export const ConsumerList = ({allDatas}:{allDatas: ISmartlandSMGWRow[] | undefined} ) => {

    useEffect(() => {
        
      }, [allDatas]);
    


    return (
        <div className="relative min-h-[30rem] w-full grow [container-type:inline-size] max-lg:mx-auto max-lg:max-w-sm gap-2 grid grid-cols-1 grid-rows-4 px-8">
            { allDatas ? 
                <Table aria-label="Example table with custom cells">
                    <TableHeader columns={columns}>
                        {(column) => (
                        <TableColumn key={column.uid} align={column.uid === "actions" ? "center" : "start"}>
                            {column.name}
                        </TableColumn>
                        )}
                    </TableHeader>
                    <TableBody items={allDatas}>
                        {(item) => (
                        <TableRow key={item.key}>
                            <TableCell>
                                <div className="flex flex-col">
                                    <p className="text-bold text-sm capitalize">{item.ts.toLocaleDateString()}</p>
                                </div>
                            </TableCell>
                            <TableCell>
                                <Chip className="capitalize" radius="sm" size="sm" color="warning" startContent={<Zap size={18} />} variant="flat">
                                    {item.value} kWh
                                </Chip>
                            </TableCell>
                            <TableCell>
                                <Chip className="capitalize" radius="sm" size="sm" color="warning" startContent={<HousePlug size={18} />} variant="flat">
                                    {item.meter_id}
                                </Chip>
                            </TableCell>
                        </TableRow>
                        )}
                    </TableBody>
                </Table>

            : 
            <span>Keine Daten verfügbar</span>
            }       
        </div>
    )
}