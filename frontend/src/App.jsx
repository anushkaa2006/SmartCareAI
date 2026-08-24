import { BrowserRouter, Routes, Route } from "react-router-dom";
import { ThemeProvider } from "./context/ThemeContext";
import { FlowProvider } from "./context/FlowContext";

import HomePage from "./pages/HomePage";
import DepartmentSelectionPage from "./pages/DepartmentSelectionPage";
import LandingPage from "./pages/LandingPage";
import IdentifyPatientPage from "./pages/IdentifyPatientPage";
import PatientRecoveryPage from "./pages/PatientRecoveryPage";
import RegistrationPage from "./pages/RegistrationPage";
import PaymentPage from "./pages/PaymentPage";
import DepartmentCheckInResultPage from "./pages/DepartmentCheckInResultPage";

export default function App() {
  return (
    <ThemeProvider>
      <FlowProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/department-select" element={<DepartmentSelectionPage />} />
            <Route path="/landing" element={<LandingPage />} />
            <Route path="/identify" element={<IdentifyPatientPage />} />
            <Route path="/recovery" element={<PatientRecoveryPage />} />
            <Route path="/registration" element={<RegistrationPage />} />
            <Route path="/payment" element={<PaymentPage />} />
            <Route path="/checkin-result" element={<DepartmentCheckInResultPage />} />
          </Routes>
        </BrowserRouter>
      </FlowProvider>
    </ThemeProvider>
  );
}
