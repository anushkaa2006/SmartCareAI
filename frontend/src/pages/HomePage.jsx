import { useNavigate } from "react-router-dom";
import { TallHeader } from "../components/Header";
import { useFlow } from "../context/FlowContext";

export default function HomePage() {
  const navigate = useNavigate();
  const { updateFlow, resetFlow } = useFlow();

  const openRegistration = () => {
    resetFlow();
    updateFlow({ mode: "REGISTRATION" });
    navigate("/landing");
  };

  const openDepartment = () => {
    resetFlow();
    updateFlow({ mode: "DEPARTMENT" });
    navigate("/department-select");
  };

  return (
    <div className="app-shell">
      <TallHeader title="SMARTCARE ID" subtitle="AI Healthcare Platform" showToggle={false} />

      <div style={{ flex: 1, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", padding: "40px 20px" }}>
        <h2 style={{ fontFamily: "var(--font-display)", fontSize: 34, margin: "20px 0 10px" }}>Choose Workflow</h2>
        <p style={{ color: "var(--text-soft)", marginBottom: 40 }}>Select the required operation</p>

        <div style={{ display: "flex", gap: 25, flexWrap: "wrap", justifyContent: "center" }}>
          <div className="card" style={{ width: 340, minHeight: 300, textAlign: "center", padding: "30px 20px" }}>
            <div style={{ fontSize: 48 }}>📝</div>
            <h3 style={{ fontSize: 22 }}>Registration Desk</h3>
            <p style={{ color: "var(--text-soft)" }}>New Registration<br />Existing Patient<br />Payment</p>
            <button className="btn btn-primary" style={{ width: 180, height: 42 }} onClick={openRegistration}>
              Open
            </button>
          </div>

          <div className="card" style={{ width: 340, minHeight: 300, textAlign: "center", padding: "30px 20px" }}>
            <div style={{ fontSize: 48 }}>🏥</div>
            <h3 style={{ fontSize: 22 }}>Department Check-In</h3>
            <p style={{ color: "var(--text-soft)" }}>Department Arrival<br />Queue Update<br />Patient Verification</p>
            <button className="btn btn-primary" style={{ width: 180, height: 42 }} onClick={openDepartment}>
              Open
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
