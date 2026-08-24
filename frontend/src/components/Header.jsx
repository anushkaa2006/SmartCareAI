import { useTheme } from "../context/ThemeContext";

export function ThemeToggle({ light = false }) {
  const { dark, toggleTheme } = useTheme();
  return (
    <div className="theme-toggle" onClick={toggleTheme} style={light ? { color: "#fff" } : undefined}>
      <span>Dark mode</span>
      <div className={`switch ${dark ? "on" : ""}`}>
        <div className="knob" />
      </div>
    </div>
  );
}

/** Tall centered brand header used on Landing / Home / Result pages */
export function TallHeader({ title = "SMARTCARE ID", subtitle, showToggle = true, rightSlot }) {
  return (
    <div className="header-bar tall">
      <h1 className="brand-title">{title}</h1>
      {subtitle && <p className="brand-sub">{subtitle}</p>}
      {showToggle && (
        <div style={{ position: "absolute", right: 24, top: 20 }}>
          <ThemeToggle light />
        </div>
      )}
      {rightSlot}
    </div>
  );
}

/** Thin strip header with back button used on inner flow pages */
export function StripHeader({ onBack, showToggle = true }) {
  return (
    <div className="header-strip">
      <div>
        {onBack && (
          <button className="back-btn" style={{ color: "var(--text)" }} onClick={onBack}>
            ← Back
          </button>
        )}
      </div>
      <div className="brand">
        <span className="glyph">⚕</span>
        <span>SMARTCARE ID</span>
      </div>
      <div>{showToggle && <ThemeToggle />}</div>
    </div>
  );
}

export function Footer() {
  return (
    <div className="footer-note">
      © 2026 SmartCare ID • Secure • Reliable • AI Powered
    </div>
  );
}
