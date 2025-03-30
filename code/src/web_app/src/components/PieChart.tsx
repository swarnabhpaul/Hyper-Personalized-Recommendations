import { ResponsiveContainer } from "recharts"
import { Cell, Legend, Pie, PieChart as PieChartRecharts, Tooltip } from "recharts"
import { PieData } from "../types/charts"

function PieChart({pieData}: {pieData: PieData[]}) {
  return (
    <ResponsiveContainer width="100%" height="40%">
        <PieChartRecharts className="pie-chart">
            <Pie
                data={pieData}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius="60%"
                fill="#8884d8"
                label={({value}) => `$${value}`}
            >
                {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color}/>
                ))}
            </Pie>
            <Tooltip formatter={(value) => `$${value}`}/>
            <Legend />
        </PieChartRecharts>
    </ResponsiveContainer>
  )
}

export default PieChart