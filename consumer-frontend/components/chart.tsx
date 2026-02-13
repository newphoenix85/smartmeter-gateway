'use client';

import { ISmartlandConsumerRow } from "@/types";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingUp } from "lucide-react";

interface EnergyChartProps {
    data: ISmartlandConsumerRow[];
}

export const EnergyChart = ({ data }: EnergyChartProps) => {
    // Transform data for recharts
    const chartData = data
        .map(item => ({
            date: new Date(item.reading_date).toLocaleDateString('de-DE', {
                day: '2-digit',
                month: '2-digit',
                hour: '2-digit',
                minute: '2-digit'
            }),
            timestamp: new Date(item.reading_date).getTime(),
            value: parseInt(item.reading_meter_number),
            user: item.user_id,
            meter: item.meter_number
        }))
        .sort((a, b) => a.timestamp - b.timestamp)
        .slice(-20); // Show last 20 data points

    // Get unique users for color coding
    const uniqueUsers = Array.from(new Set(chartData.map(d => d.user)));
    const colors = ['#8b5cf6', '#3b82f6', '#10b981', '#f59e0b', '#ef4444'];

    // Group data by user
    const userDataMap = new Map<string, typeof chartData>();
    uniqueUsers.forEach(user => {
        userDataMap.set(user, chartData.filter(d => d.user === user));
    });

    return (
        <div className="w-full bg-gradient-to-br from-violet-950/30 to-purple-900/20 backdrop-blur-sm rounded-2xl p-6 border border-violet-500/20 shadow-xl">
            <div className="flex items-center gap-3 mb-6">
                <div className="p-3 bg-violet-500/20 rounded-xl">
                    <TrendingUp className="w-6 h-6 text-violet-400" />
                </div>
                <div>
                    <h3 className="text-xl font-bold text-violet-100">Energieverbrauch Übersicht</h3>
                    <p className="text-sm text-violet-300/70">Letzte {chartData.length} Messungen</p>
                </div>
            </div>

            <ResponsiveContainer width="100%" height={400}>
                <LineChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                    <defs>
                        {uniqueUsers.map((user, idx) => (
                            <linearGradient key={user} id={`gradient-${user}`} x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor={colors[idx % colors.length]} stopOpacity={0.8} />
                                <stop offset="95%" stopColor={colors[idx % colors.length]} stopOpacity={0.2} />
                            </linearGradient>
                        ))}
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#8b5cf6" opacity={0.1} />
                    <XAxis
                        dataKey="date"
                        stroke="#a78bfa"
                        tick={{ fill: '#c4b5fd', fontSize: 12 }}
                        angle={-45}
                        textAnchor="end"
                        height={80}
                    />
                    <YAxis
                        stroke="#a78bfa"
                        tick={{ fill: '#c4b5fd', fontSize: 12 }}
                        label={{ value: 'kWh', angle: -90, position: 'insideLeft', fill: '#c4b5fd' }}
                    />
                    <Tooltip
                        contentStyle={{
                            backgroundColor: 'rgba(17, 24, 39, 0.95)',
                            border: '1px solid rgba(139, 92, 246, 0.3)',
                            borderRadius: '12px',
                            padding: '12px',
                            boxShadow: '0 10px 40px rgba(139, 92, 246, 0.3)'
                        }}
                        labelStyle={{ color: '#c4b5fd', fontWeight: 'bold', marginBottom: '8px' }}
                        itemStyle={{ color: '#e9d5ff' }}
                    />
                    <Legend
                        wrapperStyle={{ paddingTop: '20px' }}
                        iconType="line"
                    />
                    {uniqueUsers.map((user, idx) => (
                        <Line
                            key={user}
                            type="monotone"
                            dataKey="value"
                            data={userDataMap.get(user)}
                            name={`Kunde: ${user}`}
                            stroke={colors[idx % colors.length]}
                            strokeWidth={3}
                            dot={{ fill: colors[idx % colors.length], r: 4 }}
                            activeDot={{ r: 6, fill: colors[idx % colors.length] }}
                        />
                    ))}
                </LineChart>
            </ResponsiveContainer>

            <div className="mt-4 flex gap-4 flex-wrap">
                {uniqueUsers.map((user, idx) => (
                    <div key={user} className="flex items-center gap-2 px-3 py-1.5 bg-violet-500/10 rounded-lg border border-violet-500/20">
                        <div
                            className="w-3 h-3 rounded-full"
                            style={{ backgroundColor: colors[idx % colors.length] }}
                        />
                        <span className="text-xs text-violet-200">Kunde: {user}</span>
                    </div>
                ))}
            </div>
        </div>
    );
};
