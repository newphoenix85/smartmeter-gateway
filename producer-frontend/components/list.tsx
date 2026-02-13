
import { ISmartlandConsumerRow } from "@/types";
import { Chip, Table, TableBody, TableCell, TableColumn, TableHeader, TableRow } from "@heroui/react";
import { HousePlug, Zap, User, Calendar } from "lucide-react";
import { useEffect } from "react";

export const columns = [
    { name: "User ID", uid: "user_id" },
    { name: "Ablesetag", uid: "reading_date" },
    { name: "Zählerstand", uid: "reading_meter_number" },
    { name: "Zählernummer", uid: "meter_number" },
    { name: "Upload Datum", uid: "upload_date" }
];


export const ProducerList = ({ allDatas }: { allDatas: ISmartlandConsumerRow[] | undefined }) => {

    useEffect(() => {

    }, [allDatas]);


    return (
        <div className="w-full">
            {allDatas && allDatas.length > 0 ?
                <Table
                    aria-label="Producer data table"
                    classNames={{
                        wrapper: "bg-transparent shadow-none",
                        th: "bg-violet-500/10 text-violet-200 font-semibold",
                        td: "text-violet-100/90"
                    }}
                >
                    <TableHeader columns={columns}>
                        {(column) => (
                            <TableColumn key={column.uid} align="start">
                                {column.name}
                            </TableColumn>
                        )}
                    </TableHeader>
                    <TableBody items={allDatas}>
                        {(item) => (
                            <TableRow
                                key={item.key}
                                className="hover:bg-violet-500/5 transition-colors border-b border-violet-500/10"
                            >
                                <TableCell>
                                    <div className="flex flex-row gap-2 items-center">
                                        <div className="p-1.5 bg-violet-500/20 rounded-lg">
                                            <User size={14} className="text-violet-400" />
                                        </div>
                                        <span className="text-sm font-medium">{item.user_id || "N/A"}</span>
                                    </div>
                                </TableCell>
                                <TableCell>
                                    <div className="flex flex-row gap-2 items-center">
                                        <Calendar size={14} className="text-violet-400/70" />
                                        <span className="text-sm">{new Date(item.reading_date).toLocaleDateString('de-DE')}</span>
                                    </div>
                                </TableCell>
                                <TableCell>
                                    <Chip
                                        className="capitalize"
                                        radius="sm"
                                        size="sm"
                                        color="warning"
                                        startContent={<Zap size={16} />}
                                        variant="flat"
                                    >
                                        {item.reading_meter_number} kWh
                                    </Chip>
                                </TableCell>
                                <TableCell>
                                    <Chip
                                        className="capitalize"
                                        radius="sm"
                                        size="sm"
                                        color="primary"
                                        startContent={<HousePlug size={16} />}
                                        variant="flat"
                                    >
                                        {item.meter_number}
                                    </Chip>
                                </TableCell>
                                <TableCell>
                                    <div className="flex flex-row gap-2 items-center text-violet-300/60">
                                        <Calendar size={12} />
                                        <span className="text-xs">{new Date(item.upload_date).toLocaleString('de-DE')}</span>
                                    </div>
                                </TableCell>
                            </TableRow>
                        )}
                    </TableBody>
                </Table>

                :
                <div className="w-full flex justify-center p-10">
                    <span className="text-violet-300/70">Keine Daten verfügbar oder Laden fehlgeschlagen.</span>
                </div>
            }
        </div>
    )
}
