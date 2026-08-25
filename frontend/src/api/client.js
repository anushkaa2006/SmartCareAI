import axios from "axios";

// Backend base URL - override with VITE_API_URL in .env
export const BASE_URL =
  import.meta.env.VITE_API_URL?.replace(/\/$/, "") || "https://smartcareai-production.up.railway.app";

const api = axios.create({ baseURL: BASE_URL, timeout: 15000 });

// ---------------- Departments ----------------
export const getDepartments = () => api.get("/departments").then((r) => r.data);

// ---------------- Patients ----------------
export const registerBasicPatient = (payload) =>
  api.post("/patients/register/basic", payload).then((r) => r.data);

export const saveFace = (payload) =>
  api.post("/patients/face/save", payload).then((r) => r.data);

export const updateFace = (payload) =>
  api.put("/patients/face/update", payload).then((r) => r.data);

export const getAllFaces = () => api.get("/patients/faces").then((r) => r.data);

export const getPatientById = (patientId) =>
  api.get(`/patients/${patientId}`).then((r) => r.data);

export const checkExistingPatient = (payload) =>
  api.post("/patients/check-existing", payload, {
    validateStatus: (s) => s === 200 || s === 204,
  });

// ---------------- Visits ----------------
export const createVisit = (payload) =>
  api.post("/visits/create", payload).then((r) => r.data);

export const departmentCheckIn = (payload) =>
  api.post("/visits/department/checkin", payload).then((r) => r.data);

// ---------------- Payment ----------------
export const validatePayment = (payload) =>
  api.post("/payment/validate", payload).then((r) => r.data);

export const savePayment = (payload) =>
  api.post("/payment/save", payload).then((r) => r.data);

export const getLatestPayment = (patientId, departmentId) =>
  api
    .get("/payment/latest", { params: { patientId, departmentId } })
    .then((r) => r.data);

export default api;
