import { useNavigate } from "react-router-dom";
import { TallHeader, Footer } from "../components/Header";
import { InfoRow } from "../components/FormFields";
import { useFlow } from "../context/FlowContext";

const STATUS_MAP = {
  CHECK_IN_SUCCESS: { icon: "✅", title: "Department Check-In Successful", color: "var(--success)" },
  ALREADY_CHECKED_IN: { icon: "🟡", title: "Already Checked In", color: "var(--warning)" },
  WRONG_DEPARTMENT: { icon: "❌", title: "Wrong Department", color: "var(--danger)" },
};

export default function DepartmentCheckInResultPage() {
  const navigate = useNavigate();
  const { flow, resetFlow } = useFlow();
  const result = flow.checkinResult || {};

  const status = STATUS_MAP[result.action] || {
    icon: "❌",
    title: "No Active Visit Found",
    color: "var(--danger)",
  };

  function done() {
    resetFlow();
    navigate("/");
  }

  return (
    <div className="app-shell">
      <TallHeader title="SMARTCARE ID" subtitle="AI Healthcare Platform" showToggle={false} />

      <div style={{ flex: 1, display: "flex", alignItems: "center", justifyContent: "center", padding: 20 }}>
        <div className="card" style={{ width: 700, padding: "30px", textAlign: "center" }}>
          <div style={{ fontSize: 55 }}>{status.icon}</div>
          <h2 style={{ fontFamily: "var(--font-display)", fontSize: 28, color: status.color }}>{status.title}</h2>

          <div className="card-flat" style={{ margin: "30px 0", textAlign: "left" }}>
            <InfoRow label="Patient Name" value={result.patientName} />
            <InfoRow label="Patient ID" value={result.patientId} />
            <InfoRow label="Department" value={result.departmentName} />
            <InfoRow label="Queue Number" value={result.queueNumber} />
            <InfoRow label="Message" value={result.message} />
          </div>

          <button className="btn btn-primary" style={{ width: 220, height: 45 }} onClick={done}>
            Done
          </button>
        </div>
      </div>

      <Footer />
    </div>
  );
}
