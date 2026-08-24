import { useState } from "react";
import { useNavigate } from "react-router-dom";
import QRCode from "qrcode";
import jsPDF from "jspdf";
import { StripHeader } from "../components/Header";
import { useFlow } from "../context/FlowContext";
import { savePayment, createVisit } from "../api/client";

const PAYMENT_MODES = [
  ["CASH", "💵 Cash"],
  ["UPI", "📱 UPI"],
  ["CARD", "💳 Card"],
];

export default function PaymentPage() {
  const navigate = useNavigate();
  const { flow, updateFlow, resetFlow } = useFlow();
  const { patient, validation, alreadyPaid } = flow;

  const [paymentMode, setPaymentMode] = useState("CASH");
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState("");
  const [receipt, setReceipt] = useState(null); // { payment, visit, qrDataUrl }

  if (!patient || !validation) {
    navigate("/");
    return null;
  }

  const amount = parseFloat(validation.consultationFee);
  const isAlreadyPaid = validation.billingPolicy === "ALREADY_PAID";

  async function buildQrCode(payment, visit) {
    const qrData = `SMARTCARE ID
Patient ID : ${visit.patientId}
Patient Name : ${patient.name}
Visit ID : ${visit.visitId}
Department : ${patient.departmentName}
Queue Number : Q-${visit.queueNumber}
Payment ID : ${payment.paymentId}
Receipt No : ${payment.receiptNumber}
Amount : ₹ ${payment.amount}
Status : ${payment.paymentStatus}
Valid Till : ${payment.validTill}`;
    return QRCode.toDataURL(qrData, { errorCorrectionLevel: "M", margin: 2, width: 260 });
  }

  async function confirmPayment() {
    setError("");
    setProcessing(true);
    try {
      if (isAlreadyPaid) {
        const payment = flow.payment;
        const visit = flow.visit;
        const qrDataUrl = await buildQrCode(payment, visit);
        setReceipt({ payment, visit, qrDataUrl });
        return;
      }

      const payload = {
        patientId: patient.patientId,
        departmentId: patient.departmentId,
        amount,
        paymentMode,
      };
      const payment = await savePayment(payload);

      const visitRaw = await createVisit({ patientId: patient.patientId, departmentId: patient.departmentId });
      const visit = { ...visitRaw, departmentName: patient.departmentName };

      const qrDataUrl = await buildQrCode(payment, visit);
      setReceipt({ payment, visit, qrDataUrl });
    } catch (err) {
      setError(err.response?.data?.message || err.message || "Unable to save payment.");
    } finally {
      setProcessing(false);
    }
  }

  function generatePdfSlip() {
    if (!receipt) return;
    const { payment, visit, qrDataUrl } = receipt;
    const doc = new jsPDF();

    doc.setFontSize(20);
    doc.text("SMARTCARE ID", 20, 20);
    doc.setFontSize(14);
    doc.text("Patient Receipt", 20, 30);

    doc.setFontSize(11);
    const lines = [
      `Patient ID: ${patient.patientId}`,
      `Visit ID: ${visit.visitId}`,
      `Department: ${patient.departmentName}`,
      `Queue Number: Q-${visit.queueNumber}`,
      "",
      `Payment ID: ${payment.paymentId}`,
      `Receipt No: ${payment.receiptNumber}`,
      `Amount: Rs. ${payment.amount}`,
      `Status: ${payment.paymentStatus}`,
      `Valid Till: ${payment.validTill}`,
    ];
    let y = 46;
    lines.forEach((line) => {
      doc.text(line, 20, y);
      y += 8;
    });

    doc.addImage(qrDataUrl, "PNG", 20, y + 4, 45, 45);
    doc.save(`${patient.patientId}_Slip.pdf`);
  }

  function finishRegistration() {
    resetFlow();
    navigate("/");
  }

  return (
    <div className="app-shell">
      <StripHeader onBack={() => navigate(-1)} />

      <div style={{ flex: 1, display: "flex", gap: 30, padding: "30px 40px", flexWrap: "wrap" }}>
        <div style={{ flex: 1, minWidth: 340 }}>
          <div className="card" style={{ marginBottom: 20 }}>
            <p style={{ fontFamily: "var(--font-display)", fontSize: 20, padding: "20px 24px 20px" }}>
              👤 Patient Information
            </p>
            {[
              ["Patient ID", patient.patientId],
              ["Patient Name", patient.name],
              ["Department", patient.departmentName],
              ["Billing Policy", (validation.billingPolicy || "").replace(/_/g, " ")],
            ].map(([label, value]) => (
              <div key={label} style={{ display: "flex", padding: "8px 30px" }}>
                <span style={{ width: 140, fontFamily: "var(--font-display)", fontSize: 14, color: "var(--text-soft)" }}>{label}</span>
                <span>{value}</span>
              </div>
            ))}
          </div>

          {!isAlreadyPaid && (
            <div className="card">
              <p style={{ fontFamily: "var(--font-display)", fontSize: 20, padding: "20px 24px 20px" }}>
                💳 Payment Method
              </p>
              <div style={{ padding: "0 30px 20px" }}>
                {PAYMENT_MODES.map(([key, label]) => (
                  <label key={key} style={{ display: "flex", alignItems: "center", gap: 10, padding: "10px 0", cursor: "pointer" }}>
                    <input type="radio" name="paymentMode" checked={paymentMode === key} onChange={() => setPaymentMode(key)} />
                    {label}
                  </label>
                ))}
              </div>
            </div>
          )}
        </div>

        <div style={{ width: 320 }}>
          <div className="card" style={{ background: "var(--primary-soft)", textAlign: "center", padding: "30px 0" }}>
            <p style={{ fontFamily: "var(--font-display)", fontSize: 18, color: "var(--primary)" }}>Consultation Fee</p>
            <p style={{ fontFamily: "var(--font-display)", fontSize: 38, color: "var(--primary)", margin: 0 }}>₹ {amount}</p>
          </div>

          <div className="card" style={{ margin: "20px 0" }}>
            <p style={{ fontFamily: "var(--font-display)", fontSize: 18, padding: "18px 20px 10px" }}>Receipt Summary</p>
            {[
              ["Consultation Fee", `₹ ${amount.toFixed(2)}`],
              ["Discount", "₹ 0"],
              ["Total", `₹ ${amount.toFixed(2)}`],
            ].map(([label, value]) => (
              <div key={label} style={{ display: "flex", justifyContent: "space-between", padding: "8px 20px" }}>
                <span style={{ color: "var(--text-soft)" }}>{label}</span>
                <span style={{ fontFamily: "var(--font-display)" }}>{value}</span>
              </div>
            ))}
          </div>

          {error && <p className="error-text">{error}</p>}

          <div style={{ display: "flex", gap: 8 }}>
            <button className="btn btn-danger" style={{ width: 130 }} onClick={() => navigate(-1)}>
              Cancel
            </button>
            <button className="btn btn-primary" style={{ flex: 1 }} onClick={confirmPayment} disabled={processing}>
              {processing ? "Processing..." : isAlreadyPaid ? "Continue" : "Confirm Payment"}
            </button>
          </div>
        </div>
      </div>

      {receipt && (
        <div className="modal-overlay">
          <div className="modal-card" style={{ textAlign: "center" }}>
            <div
              style={{
                width: 70,
                height: 70,
                borderRadius: "50%",
                background: "var(--primary-soft)",
                color: "var(--primary)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: 30,
                margin: "0 auto 15px",
              }}
            >
              ✓
            </div>
            <h2 style={{ fontFamily: "var(--font-display)" }}>
              {receipt.payment.paymentStatus === "ALREADY PAID"
                ? "Visit Generated Successfully"
                : "Registration Completed Successfully"}
            </h2>

            <div className="card" style={{ textAlign: "left", marginTop: 15 }}>
              <div style={{ textAlign: "center", padding: "20px 0 10px" }}>
                <img src={receipt.qrDataUrl} alt="Visit QR code" width={180} height={180} />
              </div>
              {[
                ["Patient ID", patient.patientId],
                ["Patient Name", patient.name],
                ["Visit ID", receipt.visit.visitId],
                ["Queue Number", `Q-${receipt.visit.queueNumber}`],
                ["Department", patient.departmentName],
                ["Payment ID", receipt.payment.paymentId],
                ["Receipt No", receipt.payment.receiptNumber],
                ["Amount", `₹ ${receipt.payment.amount}`],
                ["Status", receipt.payment.paymentStatus],
                ["Valid Till", receipt.payment.validTill],
              ].map(([label, value]) => (
                <div key={label} style={{ display: "flex", justifyContent: "space-between", padding: "5px 25px" }}>
                  <span style={{ fontFamily: "var(--font-display)", fontSize: 13, color: "var(--text-soft)" }}>{label}</span>
                  <span style={{ fontSize: 13 }}>{value}</span>
                </div>
              ))}
              <div style={{ height: 15 }} />
            </div>

            <div style={{ display: "flex", flexDirection: "column", gap: 10, marginTop: 20 }}>
              <button className="btn btn-primary" style={{ height: 45 }} onClick={generatePdfSlip}>
                Generate & Print Slip
              </button>
              <button className="btn btn-outline" style={{ height: 45 }} onClick={finishRegistration}>
                Done
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
