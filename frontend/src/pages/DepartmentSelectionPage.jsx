import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getDepartments } from "../api/client";
import { useFlow } from "../context/FlowContext";

export default function DepartmentSelectionPage() {
  const navigate = useNavigate();
  const { updateFlow } = useFlow();

  const [names, setNames] = useState(["Loading..."]);
  const [map, setMap] = useState({});
  const [selected, setSelected] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    getDepartments()
      .then((departments) => {
        const active = departments.filter((d) => d.departmentStatus === "ACTIVE");
        const nameList = active.map((d) => d.departmentName);
        const m = {};
        active.forEach((d) => (m[d.departmentName] = d.departmentId));
        setMap(m);
        setNames(nameList.length ? nameList : ["No Active Department"]);
        setSelected(nameList[0] || "No Active Department");
      })
      .catch(() => setError("Unable to load departments."));
  }, []);

  const continueClicked = () => {
    const departmentId = map[selected];
    if (!departmentId) {
      setError("Please select a department.");
      return;
    }
    updateFlow({ departmentId, departmentName: selected });
    navigate("/landing");
  };

  return (
    <div className="app-shell">
      <div className="header-bar" style={{ height: 70 }}>
        <button className="back-btn" onClick={() => navigate("/")}>
          ← Back
        </button>
        <h2 style={{ color: "#fff", fontFamily: "var(--font-display)", fontSize: 24, margin: 0 }}>
          Department Check-In
        </h2>
        <div style={{ width: 90 }} />
      </div>

      <div style={{ flex: 1, display: "flex", alignItems: "center", justifyContent: "center" }}>
        <div className="card" style={{ width: 500, padding: "40px 30px", textAlign: "center" }}>
          <h2 style={{ fontSize: 28 }}>Select Department</h2>
          <p style={{ color: "var(--text-soft)" }}>Choose the department for patient check-in</p>

          <select
            className="field-input"
            style={{ width: 320, height: 42, margin: "35px auto", display: "block" }}
            value={selected}
            onChange={(e) => setSelected(e.target.value)}
          >
            {names.map((n) => (
              <option key={n} value={n}>
                {n}
              </option>
            ))}
          </select>

          {error && <p className="error-text">{error}</p>}

          <button className="btn btn-primary" style={{ width: 220, height: 45 }} onClick={continueClicked}>
            Continue
          </button>
        </div>
      </div>
    </div>
  );
}
