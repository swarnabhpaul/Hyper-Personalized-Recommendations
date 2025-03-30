import { PieData } from "../types/charts"
import PieChart from "./PieChart"

interface PieChartDisplayProps {
    heading: string, description?: string, pieData1?: PieData[], pieData2?: PieData[]
}

function PieChartDisplay({ heading, description, pieData1, pieData2}: PieChartDisplayProps) {
  return (
    <div className="portal-graphs">
        <h2>{heading}</h2>
        {description && <p>{description}</p>}
        {pieData1 && <PieChart pieData={pieData1}/>}
        {pieData2 && <PieChart pieData={pieData2}/>}
    </div>
  )
}

export default PieChartDisplay