import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { StripHeader } from "../components/Header";
import { InfoRow } from "../components/FormFields";
import { useFlow } from "../context/FlowContext";
import {
  getPatientById,
  getDepartments,
  validatePayment,
  getLatestPayment,
  createVisit,
} from "../api/client";

export default function IdentifyPatientPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const { updateFlow } = useFlow();

  const patientId = location.state?.patientId;

  const [patient, setPatient] = useState(null);
  const [status, setStatus] = useState({ text: "Waiting for face scan...", color: "var(--warning)" });
  const [deptNames, setDeptNames] = useState(["Loading..."]);
  const [deptMap, setDeptMap] = useState({});
  const [selectedDept, setSelectedDept] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    getDepartments()
      .then((departments) => {
        const active = departments.filter((d) => (d.departmentStatus || "").toUpperCase() === "ACTIVE");
        const names = active.map((d) => d.departmentName);
        const map = {};
        active.forEach((d) => (map[d.departmentName] = d.departmentId));
        setDeptMap(map);
        setDeptNames(names.length ? names : ["No Departments"]);
        setSelectedDept(names[0] || "No Departments");
      })
      .catch(() => {});

    if (patientId) {
      getPatientById(patientId)
        .then((p) => {
          setPatient(p);
          setStatus({ text: "✅ Registered Patient", color: "var(--success)" });
        })
        .catch(() => setError("Unable to fetch patient details"));
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [patientId]);

  async function generateVisit(pid, departmentId, departmentName) {
    const visit = await createVisit({ patientId: pid, departmentId });
    return { ...visit, departmentName };
  }

  async function handleContinue() {
    setError("");
    const departmentId = deptMap[selectedDept];
    if (!departmentId) {
      setError("Please select a department.");
      return;
    }

    setBusy(true);
    try {
      const data = await validatePayment({ patientId: patient.patientId, departmentId });

      const patientPayload = {
        patientId: patient.patientId,
        name: patient.name,
        departmentId,
        departmentName: selectedDept,
      };

      if (data.action === "PAYMENT_REQUIRED") {
        updateFlow({ patient: patientPayload, validation: data, alreadyPaid: false });
        navigate("/payment");
      } else {
        const visit = await generateVisit(patient.patientId, departmentId, selectedDept);
        const payment = await getLatestPayment(patient.patientId, departmentId);

        updateFlow({
          patient: patientPayload,
          validation: { billingPolicy: "ALREADY_PAID", consultationFee: parseFloat(payment.amount) },
          visit,
          payment,
          alreadyPaid: true,
        });
        navigate("/payment");
      }
    } catch (err) {
      setError(err.response?.data?.message || "Unable to validate payment.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="app-shell">
      <StripHeader onBack={() => navigate("/")} />

      <div style={{ flex: 1, padding: "40px 50px", maxWidth: 700 }}>
        <p style={{ color: "var(--text-faint)", fontFamily: "var(--font-display)", fontSize: 14, margin: 0 }}>
          Scan Status
        </p>
        <p style={{ fontFamily: "var(--font-display)", fontSize: 24, color: status.color, margin: "0 0 30px" }}>
          {status.text}
        </p>

        <div className="card" style={{ marginBottom: 20 }}>
          <p style={{ fontFamily: "var(--font-display)", fontSize: 20, padding: "20px 24px 15px" }}>
            👤 Patient Information
          </p>
          <div style={{ padding: "0 6px 20px" }}>
            <InfoRow label="Patient ID" value={patient?.patientId} />
            <InfoRow label="Name" value={patient?.name} />
            <InfoRow label="Age" value={patient?.age} />
            <InfoRow label="Gender" value={patient?.gender} />
            <InfoRow label="Phone" value={patient?.phone} />
          </div>
        </div>

        <div className="card">
          <p style={{ fontFamily: "var(--font-display)", fontSize: 20, padding: "20px 24px 15px" }}>
            🏥 Select Department
          </p>
          <div style={{ padding: "0 24px 24px" }}>
            <select
              className="field-input"
              style={{ width: 350, height: 45, marginBottom: 16 }}
              value={selectedDept}
              onChange={(e) => setSelectedDept(e.target.value)}
            >
              {deptNames.map((n) => (
                <option key={n} value={n}>
                  {n}
                </option>
              ))}
            </select>
            {error && <p className="error-text">{error}</p>}
            <div>
              <button className="btn btn-primary" style={{ width: 220, height: 45 }} onClick={handleContinue} disabled={busy || !patient}>
                {busy ? "Processing..." : "Continue →"}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
