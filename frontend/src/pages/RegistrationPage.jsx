import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { StripHeader } from "../components/Header";
import { Field, Dropdown, InfoRow } from "../components/FormFields";
import { useFlow } from "../context/FlowContext";
import { useCamera } from "../utils/useCamera";
import { getFaceDescriptor, descriptorToString, loadFaceModels } from "../utils/faceService";
import { INDIAN_STATES, GENDER_OPTIONS, CATEGORY_OPTIONS } from "../utils/constants";
import {
  getDepartments,
  checkExistingPatient,
  registerBasicPatient,
  saveFace,
  updateFace,
  validatePayment,
  createVisit,
  getLatestPayment,
} from "../api/client";

function calcAge(dobDdMmYyyy) {
  const parts = dobDdMmYyyy.split("/");
  if (parts.length !== 3) return "";
  const [d, m, y] = parts.map(Number);
  const birth = new Date(y, m - 1, d);
  if (isNaN(birth.getTime())) return "";
  const today = new Date();
  let age = today.getFullYear() - birth.getFullYear();
  const beforeBirthday =
    today.getMonth() < birth.getMonth() ||
    (today.getMonth() === birth.getMonth() && today.getDate() < birth.getDate());
  if (beforeBirthday) age--;
  return String(age);
}

export default function RegistrationPage() {
  const navigate = useNavigate();
  const { flow, updateFlow } = useFlow();
  const { videoRef, isActive, start, stop, captureCanvas } = useCamera();

  const updateMode = flow.updateMode;
  const existingPatient = flow.patient;

  const [step, setStep] = useState(updateMode && flow.skipSummary ? 2 : updateMode ? "summary" : 1);

  // ---- Step 1 form state ----
  const [fullName, setFullName] = useState("");
  const [gender, setGender] = useState("Select");
  const [category, setCategory] = useState("Select");
  const [dob, setDob] = useState("");
  const [age, setAge] = useState("");
  const [fatherName, setFatherName] = useState("");
  const [phone, setPhone] = useState("");
  const [state, setState] = useState("Select State");
  const [district, setDistrict] = useState("");
  const [address, setAddress] = useState("");
  const [pincode, setPincode] = useState("");
  const [department, setDepartment] = useState("Select Department");
  const [symptoms, setSymptoms] = useState("");
  const [deptNames, setDeptNames] = useState(["Select Department"]);
  const [deptMap, setDeptMap] = useState({});
  const [formError, setFormError] = useState("");

  // ---- Step 2 biometric state ----
  const [faceStatus, setFaceStatus] = useState({ text: "⏳ Face not captured yet", color: "var(--warning)" });
  const [descriptor, setDescriptor] = useState(null);
  const [capturedPreview, setCapturedPreview] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState("");

  useEffect(() => {
    loadFaceModels();
    getDepartments()
      .then((departments) => {
        const active = departments.filter((d) => (d.departmentStatus || "").toUpperCase() === "ACTIVE");
        const names = ["Select Department", ...active.map((d) => d.departmentName)];
        const map = {};
        active.forEach((d) => (map[d.departmentName] = d.departmentId));
        setDeptMap(map);
        setDeptNames(names);
      })
      .catch(() => {});
    return () => stop();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function handleDobBlur() {
    const a = calcAge(dob.trim());
    if (a) setAge(a);
  }

  async function validateAndNext() {
    setFormError("");
    const mandatory = [fullName, age, fatherName, phone, district, pincode, address];
    if (mandatory.some((v) => !v.trim())) {
      setFormError("Please fill all mandatory fields marked with *");
      return;
    }
    if (gender === "Select" || category === "Select") {
      setFormError("Please select valid options for gender & category");
      return;
    }
    if (state === "Select State") {
      setFormError("Please select state");
      return;
    }
    if (dob.split("/").length !== 3) {
      setFormError("Date of birth must be in DD/MM/YYYY format");
      return;
    }
    if (department === "Select Department") {
      setFormError("Please select a visiting department");
      return;
    }
    const phoneTrim = phone.trim();
    if (!/^\d+$/.test(phoneTrim) || phoneTrim.length !== 10) {
      setFormError("Invalid mobile number");
      return;
    }
    const pinTrim = pincode.trim();
    if (!/^\d+$/.test(pinTrim) || pinTrim.length !== 6) {
      setFormError("Invalid pincode");
      return;
    }

    try {
      const [d, m, y] = dob.trim().split("/");
      const payload = {
        name: fullName.trim(),
        fatherSpouseName: fatherName.trim(),
        dob: `${y}-${m}-${d}`,
        phone: phoneTrim,
      };
      const res = await checkExistingPatient(payload);

      if (res.status === 204) {
        setStep(2);
        return;
      }

      const patient = res.data;
      if (patient) {
        const proceed = window.confirm(
          `A patient with these details already exists.\nPatient ID: ${patient.patientId}\n\nDo you want to update the face for this patient instead of creating a new registration?`
        );
        if (proceed) {
          updateFlow({
            patient,
            updateMode: true,
            departmentId: deptMap[department],
            departmentName: department,
          });
          setStep("summary");
          return;
        }
      }
      setStep(2);
    } catch (err) {
      setFormError(err.message || "Unable to check existing patient.");
    }
  }

  // ---- Camera controls ----
  async function openCamera() {
    await start();
  }

  async function captureFace() {
    const canvas = captureCanvas();
    if (!canvas) return;
    setFaceStatus({ text: "Processing face data...", color: "var(--warning)" });

    const desc = await getFaceDescriptor(canvas);
    if (!desc) {
      setFaceStatus({ text: "No face detected", color: "var(--danger)" });
      return;
    }
    setDescriptor(desc);
    setCapturedPreview(canvas.toDataURL("image/jpeg"));
    stop();
    setFaceStatus({ text: "✓ Face captured successfully", color: "var(--success)" });
  }

  async function generateVisit(patientId, departmentId, departmentName) {
    const visit = await createVisit({ patientId, departmentId });
    return { ...visit, departmentName };
  }

  // ---- New patient submission ----
  async function registerNewPatient() {
    setSubmitting(true);
    setSubmitError("");
    try {
      const [d, m, y] = dob.trim().split("/");
      const formattedDob = `${y}-${m.padStart(2, "0")}-${d.padStart(2, "0")}`;

      const payload = {
        name: fullName.trim(),
        fatherSpouseName: fatherName.trim(),
        age: parseInt(age, 10),
        gender,
        category,
        dob: formattedDob,
        phone: phone.trim(),
        address: address.trim(),
        state: state.trim(),
        district: district.trim(),
        pincode: pincode.trim(),
        department,
      };

      const data = await registerBasicPatient(payload);
      const patientId = data.patientId;
      const departmentId = deptMap[department];

      const newPatient = {
        patientId,
        name: fullName.trim(),
        phone: phone.trim(),
        departmentId,
        departmentName: department,
      };

      if (descriptor) {
        try {
          await saveFace({
            patientId,
            imagePath: `captured_faces/${patientId}.jpg`,
            embeddingVector: descriptorToString(descriptor),
          });
        } catch (e) {
          console.warn("Face save failed:", e);
        }
      }

      const validation = await validatePayment({ patientId, departmentId });

      if (validation.action === "PAYMENT_REQUIRED") {
        updateFlow({ patient: newPatient, validation, alreadyPaid: false });
        navigate("/payment");
      } else {
        const visit = await generateVisit(patientId, departmentId, department);
        const payment = await getLatestPayment(patientId, departmentId);
        updateFlow({
          patient: newPatient,
          validation: { billingPolicy: "ALREADY_PAID", consultationFee: parseFloat(payment.amount) },
          visit,
          payment,
          alreadyPaid: true,
        });
        navigate("/payment");
      }
    } catch (err) {
      setSubmitError(err.response?.data?.message || err.message || "Registration failed.");
    } finally {
      setSubmitting(false);
    }
  }

  // ---- Existing patient (face update) submission ----
  async function updateExistingPatient() {
    setSubmitting(true);
    setSubmitError("");
    try {
      if (descriptor) {
        try {
          await updateFace({
            patientId: existingPatient.patientId,
            imagePath: `captured_faces/${existingPatient.patientId}.jpg`,
            embeddingVector: descriptorToString(descriptor),
          });
        } catch (e) {
          console.warn("Face update failed:", e);
        }
      }

      const departmentId = flow.departmentId;
      const departmentName = flow.departmentName;
      const validation = await validatePayment({ patientId: existingPatient.patientId, departmentId });

      const patientPayload = {
        patientId: existingPatient.patientId,
        name: existingPatient.name,
        departmentId,
        departmentName,
      };

      if (validation.action === "PAYMENT_REQUIRED") {
        updateFlow({ patient: patientPayload, validation, alreadyPaid: false });
        navigate("/payment");
      } else {
        const visit = await generateVisit(existingPatient.patientId, departmentId, departmentName);
        const payment = await getLatestPayment(existingPatient.patientId, departmentId);
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
      setSubmitError(err.response?.data?.message || err.message || "Unable to process request.");
    } finally {
      setSubmitting(false);
    }
  }

  function submitPatient() {
    if (updateMode) updateExistingPatient();
    else registerNewPatient();
  }

  const submitLabel = updateMode ? "Update Face & Generate Slip →" : "Complete Registration & Generate Slip →";

  return (
    <div className="app-shell">
      <StripHeader onBack={() => navigate(-1)} />

      {step !== "summary" && (
        <div className="stepper">
          <div className={`step-dot ${step === 1 ? "active" : ""}`}>1</div>
          <span className={`step-label ${step === 1 ? "active" : ""}`}>Patient details</span>
          <div className="step-line" />
          <div className={`step-dot ${step === 2 ? "active" : ""}`}>2</div>
          <span className={`step-label ${step === 2 ? "active" : ""}`}>Biometric enrollment</span>
        </div>
      )}

      <div style={{ flex: 1, padding: "8px 48px 24px" }}>
        {step === "summary" && existingPatient && (
          <div className="card" style={{ padding: 40, textAlign: "center", maxWidth: 700, margin: "20px auto" }}>
            <h2 style={{ color: "var(--success)" }}>✔ Existing Patient Verified</h2>
            <div className="card-flat" style={{ margin: "20px 0", textAlign: "left" }}>
              <InfoRow label="Patient ID" value={existingPatient.patientId} />
              <InfoRow label="Name" value={existingPatient.name} />
              <InfoRow label="Age" value={existingPatient.age} />
              <InfoRow label="Gender" value={existingPatient.gender} />
              <InfoRow label="Phone" value={existingPatient.phone} />
            </div>
            <button className="btn btn-primary" style={{ height: 45, width: 200 }} onClick={() => setStep(2)}>
              Continue →
            </button>
          </div>
        )}

        {step === 1 && (
          <div className="card" style={{ padding: "8px 36px 24px", maxWidth: 1100, margin: "0 auto" }}>
            <SectionTitle title="Personal Details" subtitle="Patient personal information" />
            <Grid>
              <Field label="Full Name *" value={fullName} onChange={setFullName} style={{ gridColumn: "span 3" }} />
              <Dropdown label="Gender *" value={gender} onChange={setGender} options={GENDER_OPTIONS} style={{ gridColumn: "span 2" }} />
              <Dropdown label="Category *" value={category} onChange={setCategory} options={CATEGORY_OPTIONS} style={{ gridColumn: "span 2" }} />

              <Field label="DOB * (DD/MM/YYYY)" value={dob} onChange={setDob} onBlur={handleDobBlur} placeholder="DD/MM/YYYY" style={{ gridColumn: "span 2" }} />
              <Field label="Age *" value={age} onChange={setAge} style={{ gridColumn: "span 1" }} />
              <Field label="Father / Spouse Name *" value={fatherName} onChange={setFatherName} style={{ gridColumn: "span 3" }} />
            </Grid>

            <hr style={{ border: "none", borderTop: "1px solid var(--border-soft)", margin: "14px 0" }} />
            <SectionTitle title="Contact & Address" subtitle="Basic contact information" />
            <Grid>
              <Field label="Mobile number *" value={phone} onChange={setPhone} style={{ gridColumn: "span 3" }} />
              <Dropdown label="State *" value={state} onChange={setState} options={INDIAN_STATES} style={{ gridColumn: "span 2" }} />
              <Field label="District *" value={district} onChange={setDistrict} style={{ gridColumn: "span 2" }} />

              <Field label="Full address *" value={address} onChange={setAddress} style={{ gridColumn: "span 5" }} />
              <Field label="Pincode *" value={pincode} onChange={setPincode} style={{ gridColumn: "span 2" }} />
            </Grid>

            <hr style={{ border: "none", borderTop: "1px solid var(--border-soft)", margin: "14px 0" }} />
            <Grid>
              <Dropdown label="Visiting Department *" value={department} onChange={setDepartment} options={deptNames} style={{ gridColumn: "span 3" }} />
              <Field label="Visit Reason (optional)" value={symptoms} onChange={setSymptoms} style={{ gridColumn: "span 4" }} />
            </Grid>

            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginTop: 12 }}>
              <span className="error-text">{formError}</span>
              <button className="btn btn-primary" style={{ height: 40 }} onClick={validateAndNext}>
                Continue →
              </button>
            </div>
          </div>
        )}

        {step === 2 && (
          <div className="card" style={{ maxWidth: 1000, margin: "0 auto", padding: "16px 36px 24px", display: "flex", flexDirection: "column" }}>
            <p style={{ fontFamily: "var(--font-display)", fontSize: 18, margin: "0 0 2px" }}>Biometric enrollment</p>
            <p style={{ fontSize: 12, color: "var(--text-faint)", margin: "0 0 8px" }}>
              Position the patient's face within the frame and capture a clear photo.
            </p>

            <div className="card-flat" style={{ padding: 14 }}>
              <div className="camera-box" style={{ height: 360 }}>
                {capturedPreview ? (
                  <img src={capturedPreview} alt="Captured face" style={{ width: "100%", height: "100%", objectFit: "contain" }} />
                ) : isActive ? (
                  <video ref={videoRef} muted playsInline style={{ transform: "scaleX(-1)" }} />
                ) : (
                  <span style={{ color: "var(--text-faint)" }}>◉ Camera offline</span>
                )}
              </div>
            </div>

            <div style={{ textAlign: "center", margin: "8px 0" }}>
              <span className="pill" style={{ background: "var(--primary-soft)", color: faceStatus.color }}>
                {faceStatus.text}
              </span>
            </div>

            <div style={{ display: "flex", gap: 8, justifyContent: "center", marginBottom: 12 }}>
              {!updateMode && step !== "summary" && (
                <button className="btn btn-outline" onClick={() => setStep(1)}>
                  ← Back
                </button>
              )}
              <button className="btn btn-ghost" onClick={openCamera}>
                ◉ Open camera
              </button>
              <button className="btn btn-primary" onClick={captureFace} disabled={!isActive}>
                ✓ Capture face
              </button>
            </div>

            {submitError && <p className="error-text" style={{ textAlign: "center" }}>{submitError}</p>}

            <div style={{ display: "flex", justifyContent: "flex-end" }}>
              <button className="btn btn-primary" style={{ height: 50 }} onClick={submitPatient} disabled={submitting}>
                {submitting ? "Processing..." : submitLabel}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function SectionTitle({ title, subtitle }) {
  return (
    <div style={{ display: "flex", gap: 12, margin: "6px 0" }}>
      <div style={{ width: 4, height: 24, borderRadius: 6, background: "var(--primary-soft)" }} />
      <div>
        <p className="section-title">{title}</p>
        <p className="section-sub">{subtitle}</p>
      </div>
    </div>
  );
}

function Grid({ children }) {
  return (
    <div style={{ display: "grid", gridTemplateColumns: "repeat(8, 1fr)", gap: "6px 10px" }}>
      {children}
    </div>
  );
}
