import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { TallHeader, Footer } from "../components/Header";
import { useFlow } from "../context/FlowContext";
import { useCamera } from "../utils/useCamera";
import { getFaceDescriptor, identifyFace, loadFaceModels } from "../utils/faceService";
import { departmentCheckIn } from "../api/client";

const SCAN_INTERVAL_MS = 1200;

export default function LandingPage() {
  const navigate = useNavigate();
  const { flow, updateFlow } = useFlow();
  const { videoRef, start, stop } = useCamera();

  const [status, setStatus] = useState("🟢 Waiting for Patient...");
  const [info, setInfo] = useState("Camera initializing...");
  const processingRef = useRef(false);
  const stoppedRef = useRef(false);
  const intervalRef = useRef(null);

  useEffect(() => {
    stoppedRef.current = false;
    loadFaceModels();
    start();
    intervalRef.current = setInterval(scanFace, SCAN_INTERVAL_MS);

    return () => {
      stoppedRef.current = true;
      clearInterval(intervalRef.current);
      stop();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function scanFace() {
    if (processingRef.current || stoppedRef.current) return;
    const video = videoRef.current;
    if (!video || !video.videoWidth) return;

    processingRef.current = true;
    setStatus("🟡 Checking Face...");
    setInfo("Comparing with registered patients...");

    try {
      const descriptor = await getFaceDescriptor(video);
      if (!descriptor) {
        setStatus("🟢 Waiting for Patient...");
        setInfo("No face detected yet.");
        processingRef.current = false;
        return;
      }

      const result = await identifyFace(descriptor);

      if (stoppedRef.current) return;

      if (result.found) {
        setStatus("🟢 Patient Identified");
        setInfo(`Patient ID : ${result.patientId}`);
        stoppedRef.current = true;
        clearInterval(intervalRef.current);
        stop();

        setTimeout(async () => {
          if (flow.mode === "REGISTRATION") {
            navigate("/identify", { state: { patientId: result.patientId } });
          } else {
            try {
              const checkinResult = await departmentCheckIn({
                patientId: result.patientId,
                departmentId: flow.departmentId,
              });
              updateFlow({ checkinResult });
            } catch {
              updateFlow({
                checkinResult: {
                  action: "NO_ACTIVE_VISIT",
                  patientId: result.patientId,
                  message: "Unable to verify department visit.",
                },
              });
            }
            navigate("/checkin-result");
          }
        }, 500);
      } else {
        setStatus("🔴 Patient Not Found");
        setInfo("Opening Patient Recovery...");
        stoppedRef.current = true;
        clearInterval(intervalRef.current);
        stop();

        setTimeout(() => navigate("/recovery"), 500);
      }
    } catch (err) {
      setInfo("Scan error, retrying...");
      console.error(err);
    } finally {
      processingRef.current = false;
    }
  }

  return (
    <div className="app-shell">
      <TallHeader title="SMARTCARE ID" subtitle="AI Face Recognition Patient Identification System" />

      <div style={{ flex: 1, display: "flex", gap: 40, padding: "20px 80px", flexWrap: "wrap" }}>
        <div style={{ flex: 1, minWidth: 320 }}>
          <span className="pill" style={{ background: "var(--primary-soft)", color: "var(--primary)" }}>
            ⚡ Powered by AI Face Recognition
          </span>

          <h1 style={{ fontFamily: "var(--font-display)", fontSize: 48, margin: "16px 0 0" }}>Healthcare,</h1>
          <h1 style={{ fontFamily: "var(--font-display)", fontSize: 48, margin: 0, color: "var(--primary)" }}>
            reimagined.
          </h1>

          <p style={{ color: "var(--text-soft)", fontSize: 15, margin: "14px 0 28px" }}>
            Smart patient identification and queue management
            <br />
            that feels effortless — for everyone.
          </p>

          {[
            ["🤖", "AI Face Recognition"],
            ["⏱", "Real-time Queue Management"],
            ["🔒", "Secure Patient Records"],
          ].map(([icon, text]) => (
            <div key={text} style={{ display: "flex", alignItems: "center", gap: 10, margin: "4px 0", color: "var(--text-faint)" }}>
              <span>{icon}</span>
              <span>{text}</span>
            </div>
          ))}

          <div className="card" style={{ marginTop: 30, textAlign: "center", padding: "20px 0" }}>
            <p style={{ color: "var(--primary)", fontFamily: "var(--font-display)", fontSize: 15, margin: 0 }}>
              SYSTEM STATUS
            </p>
            <p style={{ fontSize: 18, margin: "10px 0 5px", color: "var(--success)" }}>{status}</p>
            <p style={{ fontSize: 13, color: "var(--text-soft)", margin: 0 }}>{info}</p>
          </div>
        </div>

        <div style={{ width: 480, minWidth: 320 }}>
          <div className="card" style={{ height: 500, display: "flex", flexDirection: "column", alignItems: "center", padding: 20 }}>
            <p style={{ fontFamily: "var(--font-display)", fontSize: 18 }}>Live Patient Scanner</p>
            <div className="camera-box" style={{ width: "100%", flex: 1 }}>
              <video ref={videoRef} muted playsInline style={{ transform: "scaleX(-1)" }} />
            </div>
          </div>
        </div>
      </div>

      <Footer />
    </div>
  );
}
