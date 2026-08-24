export function Field({ label, value, onChange, placeholder, style, ...rest }) {
  return (
    <div style={style}>
      <label className="field-label">{label}</label>
      <input
        className="field-input"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        {...rest}
      />
    </div>
  );
}

export function Dropdown({ label, value, onChange, options, style }) {
  return (
    <div style={style}>
      <label className="field-label">{label}</label>
      <select className="field-input" value={value} onChange={(e) => onChange(e.target.value)}>
        {options.map((opt) => (
          <option key={opt} value={opt}>
            {opt}
          </option>
        ))}
      </select>
    </div>
  );
}

export function InfoRow({ label, value }) {
  return (
    <div className="info-row">
      <div className="label">{label} :</div>
      <div className="value">{value ?? "-"}</div>
    </div>
  );
}

export function SectionTitle({ title, subtitle }) {
  return (
    <div style={{ display: "flex", alignItems: "flex-start", gap: 12, margin: "8px 0" }}>
      <div style={{ width: 4, height: 24, borderRadius: 6, background: "var(--primary-soft)" }} />
      <div>
        <p className="section-title">{title}</p>
        {subtitle && <p className="section-sub">{subtitle}</p>}
      </div>
    </div>
  );
}
