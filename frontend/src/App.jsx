import { useState } from "react";
import axios from "axios";
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    Tooltip,
    CartesianGrid,
    ResponsiveContainer,
} from "recharts";

function App() {
    const [station, setStation] = useState("gabriel");
    const [aggregation, setAggregation] = useState("daily");

    const [startDate, setStartDate] =
        useState("2024-01-01T00:00:00");

    const [endDate, setEndDate] =
        useState("2024-01-10T00:00:00");

    const [records, setRecords] = useState([]);

    const fetchWeather = async () => {
        const response = await axios.get(
            `http://127.0.0.1:8001/api/antarctica/data/start/${startDate}/end/${endDate}/station/${station}?aggregation=${aggregation}`
        );

        setRecords(response.data.records);
    };

    return (
        <div style={{ padding: "2rem" }}>
            <h1>Antarctic Weather Intelligence</h1>

            <div>
                <select
                    value={station}
                    onChange={(e) => setStation(e.target.value)}
                >
                    <option value="gabriel">
                        Gabriel de Castilla
                    </option>

                    <option value="juan">
                        Juan Carlos I
                    </option>
                </select>

                <select
                    value={aggregation}
                    onChange={(e) =>
                        setAggregation(e.target.value)
                    }
                >
                    <option value="none">None</option>
                    <option value="daily">Daily</option>
                    <option value="monthly">Monthly</option>
                </select>

                <button onClick={fetchWeather}>
                    Load Data
                </button>
            </div>

            <hr />

            <ResponsiveContainer
                width="100%"
                height={400}
            >
                <LineChart data={records}>
                    <CartesianGrid strokeDasharray="3 3" />

                    <XAxis dataKey="datetime" />

                    <YAxis />

                    <Tooltip />

                    <Line
                        type="monotone"
                        dataKey="temperature"
                    />
                </LineChart>
            </ResponsiveContainer>

            <table border="1">
                <thead>
                <tr>
                    <th>Date</th>
                    <th>Temperature</th>
                    <th>Pressure</th>
                    <th>Wind</th>
                </tr>
                </thead>

                <tbody>
                {records.map((record) => (
                    <tr key={record.datetime}>
                        <td>{record.datetime}</td>
                        <td>{record.temperature}</td>
                        <td>{record.pressure}</td>
                        <td>{record.wind_speed}</td>
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    );
}

export default App;