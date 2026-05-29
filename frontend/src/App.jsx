import { useMemo, useState } from "react";
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

const API_BASE_URL =
    import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8001";

const metricLabels = {
    temperature: "Temperature (°C)",
    pressure: "Pressure (hPa)",
    wind_speed: "Wind Speed (m/s)",
};

const stations = {
    gabriel: "Gabriel de Castilla",
    juan: "Juan Carlos I",
};

function App() {
    const [station, setStation] = useState("gabriel");
    const [aggregation, setAggregation] = useState("daily");
    const [metric, setMetric] = useState("temperature");

    const [startDate, setStartDate] = useState("2024-01-01T00:00");
    const [endDate, setEndDate] = useState("2024-01-10T00:00");

    const [records, setRecords] = useState([]);
    const [metadata, setMetadata] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const chartData = useMemo(() => {
        return records.filter(
            (record) => record[metric] !== null && record[metric] !== undefined
        );
    }, [records, metric]);

    const selectedMetricLabel = metricLabels[metric];

    const fetchWeather = async () => {
        setLoading(true);
        setError("");
        setRecords([]);
        setMetadata(null);

        try {
            const response = await axios.get(
                `${API_BASE_URL}/api/antarctica/data/start/${startDate}:00/end/${endDate}:00/station/${station}`,
                {
                    params: {
                        aggregation,
                        fields: metric,
                    },
                }
            );

            setRecords(response.data.records || []);
            setMetadata({
                station: response.data.station,
                stationId: response.data.station_id,
                aggregation: response.data.aggregation,
                cacheStatus: response.data.cache_status,
                cacheAgeMinutes: response.data.cache_age_minutes,
                recordsCount: response.data.records_count,
                startDate: response.data.start_date,
                endDate: response.data.end_date,
            });
        } catch (err) {
            const message =
                err.response?.data?.detail ||
                "Could not fetch weather data. Check that the backend is running.";
            setError(message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <main style={styles.page}>
            <section style={styles.hero}>
                <div>
                    <h1 style={styles.title}>Antarctic Weather Intelligence</h1>
                    <p style={styles.subtitle}>
                        Historical Antarctic weather analytics platform with aggregation,
                        SQLite caching, timezone handling and interactive visualizations.
                    </p>
                </div>

                <div style={styles.heroBadge}>
                    Personal Project
                </div>
            </section>

            <section style={styles.card}>
                <div style={styles.cardHeader}>
                    <div>
                        <h2 style={styles.sectionTitle}>Weather Data Explorer</h2>
                        <p style={styles.sectionSubtitle}>
                            Select station, time range, aggregation level and metric.
                        </p>
                    </div>
                </div>

                <div style={styles.controls}>
                    <label style={styles.field}>
                        Station
                        <select
                            style={styles.input}
                            value={station}
                            onChange={(event) => setStation(event.target.value)}
                        >
                            {Object.entries(stations).map(([value, label]) => (
                                <option key={value} value={value}>
                                    {label}
                                </option>
                            ))}
                        </select>
                    </label>

                    <label style={styles.field}>
                        Aggregation
                        <select
                            style={styles.input}
                            value={aggregation}
                            onChange={(event) => setAggregation(event.target.value)}
                        >
                            <option value="none">None</option>
                            <option value="hourly">Hourly</option>
                            <option value="daily">Daily</option>
                            <option value="monthly">Monthly</option>
                        </select>
                    </label>

                    <label style={styles.field}>
                        Metric
                        <select
                            style={styles.input}
                            value={metric}
                            onChange={(event) => setMetric(event.target.value)}
                        >
                            <option value="temperature">Temperature</option>
                            <option value="pressure">Pressure</option>
                            <option value="wind_speed">Wind Speed</option>
                        </select>
                    </label>

                    <label style={styles.field}>
                        Start date
                        <input
                            style={styles.input}
                            type="datetime-local"
                            value={startDate}
                            onChange={(event) => setStartDate(event.target.value)}
                        />
                    </label>

                    <label style={styles.field}>
                        End date
                        <input
                            style={styles.input}
                            type="datetime-local"
                            value={endDate}
                            onChange={(event) => setEndDate(event.target.value)}
                        />
                    </label>

                    <button
                        style={{
                            ...styles.button,
                            opacity: loading ? 0.7 : 1,
                            cursor: loading ? "not-allowed" : "pointer",
                        }}
                        onClick={fetchWeather}
                        disabled={loading}
                    >
                        {loading ? "Fetching..." : "Fetch Weather Data"}
                    </button>
                </div>

                {error && <p style={styles.error}>{error}</p>}
            </section>

            {metadata && (
                <section style={styles.summaryGrid}>
                    <SummaryCard label="Station" value={metadata.station} />
                    <SummaryCard
                        label="Aggregation"
                        value={metadata.aggregation.toUpperCase()}
                    />
                    <SummaryCard
                        label="Cache"
                        value={metadata.cacheStatus.toUpperCase()}
                    />
                    <SummaryCard
                        label="Cache age"
                        value={`${metadata.cacheAgeMinutes ?? 0} min`}
                    />
                    <SummaryCard label="Records" value={metadata.recordsCount} />
                </section>
            )}

            <section style={styles.card}>
                <div style={styles.cardHeader}>
                    <div>
                        <h2 style={styles.sectionTitle}>{selectedMetricLabel}</h2>
                        <p style={styles.sectionSubtitle}>
                            Visual trend for {stations[station]} using {aggregation} aggregation.
                        </p>
                    </div>
                </div>

                {records.length === 0 && !loading ? (
                    <div style={styles.emptyState}>
                        <strong>No data loaded yet</strong>
                        <span>Select your filters and fetch weather data.</span>
                    </div>
                ) : (
                    <div style={styles.chartWrapper}>
                        <ResponsiveContainer width="100%" height={380}>
                            <LineChart data={chartData}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="datetime" />
                                <YAxis />
                                <Tooltip />
                                <Line
                                    type="monotone"
                                    dataKey={metric}
                                    strokeWidth={3}
                                    dot={false}
                                />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                )}
            </section>

            {records.length > 0 && (
                <section style={styles.card}>
                    <div style={styles.cardHeader}>
                        <div>
                            <h2 style={styles.sectionTitle}>Dataset</h2>
                            <p style={styles.sectionSubtitle}>
                                Returned API records for the selected metric.
                            </p>
                        </div>
                    </div>

                    <div style={styles.tableWrapper}>
                        <table style={styles.table}>
                            <thead>
                            <tr>
                                <th style={styles.th}>Date</th>
                                <th style={styles.th}>{selectedMetricLabel}</th>
                                <th style={styles.th}>Records count</th>
                            </tr>
                            </thead>

                            <tbody>
                            {records.map((record) => (
                                <tr key={record.datetime}>
                                    <td style={styles.td}>{record.datetime}</td>
                                    <td style={styles.td}>{record[metric] ?? "-"}</td>
                                    <td style={styles.td}>
                                        {record.records_count ?? "-"}
                                    </td>
                                </tr>
                            ))}
                            </tbody>
                        </table>
                    </div>
                </section>
            )}
        </main>
    );
}

function SummaryCard({ label, value }) {
    return (
        <div style={styles.summaryCard}>
            <span style={styles.summaryLabel}>{label}</span>
            <strong style={styles.summaryValue}>{value}</strong>
        </div>
    );
}

const styles = {
    page: {
        minHeight: "100vh",
        padding: "2rem",
        background:
            "linear-gradient(135deg, #f8fbff 0%, #eef4fb 45%, #e8f0f8 100%)",
        color: "#0f172a",
        fontFamily: "Inter, system-ui, Arial, sans-serif",
    },
    hero: {
        display: "flex",
        justifyContent: "space-between",
        gap: "1rem",
        alignItems: "flex-start",
        marginBottom: "1.5rem",
    },
    title: {
        margin: 0,
        fontSize: "clamp(2rem, 5vw, 3.5rem)",
        lineHeight: 1,
        letterSpacing: "-0.04em",
    },
    subtitle: {
        marginTop: "0.8rem",
        color: "#475569",
        maxWidth: "780px",
        fontSize: "1.05rem",
        lineHeight: 1.6,
    },
    heroBadge: {
        padding: "0.7rem 1rem",
        borderRadius: "999px",
        background: "#dbeafe",
        color: "#1d4ed8",
        fontWeight: 800,
        whiteSpace: "nowrap",
    },
    card: {
        background: "rgba(255, 255, 255, 0.95)",
        borderRadius: "22px",
        padding: "1.5rem",
        marginBottom: "1.25rem",
        boxShadow: "0 18px 45px rgba(15, 23, 42, 0.08)",
        border: "1px solid rgba(226, 232, 240, 0.9)",
    },
    cardHeader: {
        display: "flex",
        justifyContent: "space-between",
        marginBottom: "1.2rem",
    },
    sectionTitle: {
        margin: 0,
        fontSize: "1.35rem",
    },
    sectionSubtitle: {
        margin: "0.3rem 0 0",
        color: "#64748b",
    },
    controls: {
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit, minmax(190px, 1fr))",
        gap: "1rem",
        alignItems: "end",
    },
    field: {
        display: "flex",
        flexDirection: "column",
        gap: "0.4rem",
        fontSize: "0.9rem",
        fontWeight: 700,
        color: "#1e293b",
    },
    input: {
        padding: "0.8rem",
        borderRadius: "12px",
        border: "1px solid #cbd5e1",
        fontSize: "0.95rem",
        background: "#ffffff",
        color: "#0f172a",
    },
    button: {
        padding: "0.88rem 1rem",
        border: "none",
        borderRadius: "12px",
        background: "#2563eb",
        color: "#ffffff",
        fontWeight: 800,
        fontSize: "0.95rem",
        boxShadow: "0 12px 24px rgba(37, 99, 235, 0.25)",
    },
    error: {
        marginTop: "1rem",
        padding: "0.9rem",
        borderRadius: "12px",
        background: "#fee2e2",
        color: "#991b1b",
        fontWeight: 700,
    },
    summaryGrid: {
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit, minmax(170px, 1fr))",
        gap: "1rem",
        marginBottom: "1.25rem",
    },
    summaryCard: {
        background: "#ffffff",
        borderRadius: "18px",
        padding: "1.15rem",
        boxShadow: "0 14px 32px rgba(15, 23, 42, 0.07)",
        border: "1px solid #e2e8f0",
        display: "flex",
        flexDirection: "column",
        gap: "0.35rem",
    },
    summaryLabel: {
        color: "#64748b",
        fontSize: "0.78rem",
        textTransform: "uppercase",
        letterSpacing: "0.08em",
        fontWeight: 700,
    },
    summaryValue: {
        fontSize: "1.15rem",
    },
    chartWrapper: {
        width: "100%",
        height: "380px",
    },
    emptyState: {
        minHeight: "220px",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        gap: "0.5rem",
        color: "#64748b",
        border: "1px dashed #cbd5e1",
        borderRadius: "16px",
    },
    tableWrapper: {
        overflowX: "auto",
        borderRadius: "14px",
        border: "1px solid #e2e8f0",
    },
    table: {
        width: "100%",
        borderCollapse: "collapse",
        background: "#ffffff",
    },
    th: {
        textAlign: "left",
        padding: "0.9rem",
        background: "#eff6ff",
        borderBottom: "1px solid #dbeafe",
        color: "#1e3a8a",
        fontSize: "0.85rem",
        textTransform: "uppercase",
        letterSpacing: "0.05em",
    },
    td: {
        padding: "0.9rem",
        borderBottom: "1px solid #f1f5f9",
        color: "#334155",
    },
};

export default App;