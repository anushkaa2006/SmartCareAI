import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { StripHeader } from "../components/Header";
import { InfoRow } from "../components/FormFields";
import { useFlow } from "../context/FlowContext";
import { getPatientById, getDepartments, departmentCheckIn } from "../api/client";

export default function PatientRecoveryPage() {
  const navigate = useNavigate();
  const { flow, updateFlow } = useFlow();

  const [patientIdInput, setPatientIdInput] = useState("");
  const [error, setError] = useState("");
  const [verifiedPatient, setVerifiedPatient] = useState(null);
  const [deptNames, setDeptNames] = useState(["Loading..."]);
  const [deptMap, setDeptMap] = useState({});
  const [selectedDept, setSelectedDept] = useState("");
  const [checkingIn, setCheckingIn] = useState(false);

  useEffect(() => {
    if (flow.mode === "REGISTRATION" && verifiedPatient) {
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
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [verifiedPatient]);

  async function verifyPatient() {
    setError("");
    const id = patientIdInput.trim();
    if (!id) {
      setError("Please enter Patient ID");
      return;
    }
    try {
      const patient = await getPatientById(id);
      if (!patient) {
        setError("Patient ID does not exist");
        return;
      }
      setVerifiedPatient(patient);
    } catch {
      setError("Patient ID does not exist");
    }
  }

  function continueToFaceUpdate() {
    const departmentId = deptMap[selectedDept];
    updateFlow({
      patient: verifiedPatient,
      updateMode: true,
      skipSummary: true,
      departmentId,
      departmentName: selectedDept,
    });
    navigate("/registration");
  }

  async function departmentCheckin() {
    setCheckingIn(true);
    try {
      const checkinResult = await departmentCheckIn({
        patientId: verifiedPatient.patientId,
        departmentId: flow.departmentId,
      });
      updateFlow({ checkinResult });
    } catch {
      updateFlow({
        checkinResult: {
          action: "NO_ACTIVE_VISIT",
          patientId: verifiedPatient.patientId,
          message: "Unable to verify department visit.",
        },
      });
    }
    navigate("/checkin-result");
  }

  return (
    <div className="app-shell">
      <StripHeader onBack={() => navigate("/")} />

      <div style={{ flex: 1, display: "flex", alignItems: "center", justifyContent: "center", padding: 20 }}>
        {!verifiedPatient ? (
          <div className="card" style={{ width: 700, padding: "40px 30px", textAlign: "center" }}>
            <h2 style={{ fontSize: 28 }}>Patient Not Recognized</h2>
            <p style={{ color: "var(--text-soft)" }}>Already have a Patient ID?</p>

            <input
              className="field-input"
              style={{ width: 350, height: 45, margin: "20px auto", display: "block", textAlign: "center" }}
              placeholder="Enter Patient ID"
              value={patientIdInput}
              onChange={(e) => setPatientIdInput(e.target.value)}
            />

            {error && <p className="error-text">{error}</p>}

            <button className="btn btn-primary" style={{ width: 250, height: 45, margin: "10px 0" }} onClick={verifyPatient}>
              Verify Patient
            </button>

            {flow.mode === "REGISTRATION" && (
              <>
                <p style={{ color: "var(--text-soft)", margin: "25px 0" }}>──────── OR ────────</p>
                <button
                  className="btn btn-primary"
                  style={{ width: 250, height: 45 }}
                  onClick={() => {
                    updateFlow({ patient: null, updateMode: false, skipSummary: false });
                    navigate("/registration");
                  }}
                >
                  Register as New Patient
                </button>
              </>
            )}
          </div>
        ) : (
          <div className="card" style={{ width: 700, padding: "30px", textAlign: "center" }}>
            <h2 style={{ fontSize: 28, color: "var(--success)" }}>✔ Existing Patient Verified</h2>

            <div className="card-flat" style={{ margin: "30px 0", textAlign: "left" }}>
              <InfoRow label="Patient ID" value={verifiedPatient.patientId} />
              <InfoRow label="Name" value={verifiedPatient.name} />
              <InfoRow label="Age" value={verifiedPatient.age} />
              <InfoRow label="Gender" value={verifiedPatient.gender} />
              <InfoRow label="Phone" value={verifiedPatient.phone} />
            </div>

            {flow.mode === "REGISTRATION" ? (
              <>
                <select
                  className="field-input"
                  style={{ width: 320, height: 42, margin: "0 auto 20px", display: "block" }}
                  value={selectedDept}
                  onChange={(e) => setSelectedDept(e.target.value)}
                >
                  {deptNames.map((n) => (
                    <option key={n} value={n}>
                      {n}
                    </option>
                  ))}
                </select>
                <button className="btn btn-primary" style={{ width: 180, height: 42 }} onClick={continueToFaceUpdate}>
                  Continue
                </button>
              </>
            ) : (
              <button className="btn btn-primary" style={{ width: 180, height: 42 }} onClick={departmentCheckin} disabled={checkingIn}>
                {checkingIn ? "Checking In..." : "Check In"}
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
