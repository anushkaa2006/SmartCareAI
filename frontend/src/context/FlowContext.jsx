import { createContext, useContext, useState, useCallback } from "react";

const FlowContext = createContext(null);

const initialState = {
  mode: "REGISTRATION", // REGISTRATION | DEPARTMENT
  departmentId: null,
  departmentName: null,

  patient: null, // { patientId, name, departmentId, departmentName, ... }
  updateMode: false,
  skipSummary: false,

  validation: null, // payment validation response
  payment: null,
  visit: null,
  alreadyPaid: false,

  checkinResult: null, // department check-in response
};

export function FlowProvider({ children }) {
  const [flow, setFlow] = useState(initialState);

  const updateFlow = useCallback((patch) => {
    setFlow((prev) => ({ ...prev, ...patch }));
  }, []);

  const resetFlow = useCallback(() => setFlow(initialState), []);

  return (
    <FlowContext.Provider value={{ flow, updateFlow, resetFlow }}>
      {children}
    </FlowContext.Provider>
  );
}

export function useFlow() {
  return useContext(FlowContext);
}
