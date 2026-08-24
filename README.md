# SmartCare ID — AI Healthcare Check-In Platform

SmartCare ID is a hospital patient registration and check-in system that uses
face recognition to identify returning patients, route them to departments,
manage visits, and handle payment validation.

## Architecture

| Component | Tech | Role |
|---|---|---|
| **Backend** | Java 25, Spring Boot, Spring Data JPA, MySQL | REST API for patients, departments, visits, payments, and face embeddings |
| **Frontend** | React 19 + Vite, `face-api.js` (in-browser face recognition) | Web app: webcam capture, face match, registration, payment, department check-in |
| **Database** | MySQL 8 | Persistent storage |

The frontend is now a **web application** (previously a Python/CustomTkinter
desktop app) — it runs in a browser and accesses the webcam via the standard
`getUserMedia` API, so it can be opened from any machine with a browser and a
camera, not just a dedicated kiosk PC. See `frontend/README.md` for
frontend-specific notes, especially around face recognition compatibility.

```
┌─────────────────────┐        HTTP (REST, port 9090)        ┌──────────────────────┐
│  Frontend (Browser)  │ ────────────────────────────────────▶│   Backend (Server)   │
│  React + Vite        │                                       │  Spring Boot          │
└─────────────────────┘                                       └──────────┬───────────┘
                                                                            │ JDBC
                                                                            ▼
                                                                  ┌──────────────────┐
                                                                  │   MySQL 8         │
                                                                  └──────────────────┘
```

## What's in this package

```
SmartCareAI-main/
├── backend/
│   ├── Dockerfile                                    # multi-stage build for the Spring Boot API
│   ├── .dockerignore
│   ├── src/main/java/com/smartcare/config/WebConfig.java   # NEW - global CORS config for the web frontend
│   └── src/main/resources/application.properties     # env-var driven config
├── frontend/                                          # NEW - React + Vite web app (replaces the old
│   ├── src/                                           #   Python/CustomTkinter desktop client)
│   ├── public/models/                                 # face-api.js model weights (bundled, no download needed)
│   ├── README.md                                      # frontend setup + face-recognition notes
│   └── .env.example
├── docker-compose.yml                                 # MySQL + backend stack
├── .env.example                                       # docker-compose variables
└── README.md                                          # this file
```

---

## 1. Deploy the backend + database (Docker — recommended)

Prerequisites: Docker and Docker Compose installed.

```bash
cd SmartCareAI-main
cp .env.example .env       # edit DB credentials/ports if you want
docker compose up -d --build
```

This starts:
- `smartcare-mysql` — MySQL 8 on port `3306` (persisted in a named volume)
- `smartcare-backend` — Spring Boot API on port `9090`, waiting for MySQL to
  be healthy before starting, with the schema auto-created (`ddl-auto=update`)

Check it's up:

```bash
curl http://localhost:9090/departments
```

To view logs or stop:

```bash
docker compose logs -f backend
docker compose down          # add -v to also wipe the DB volume
```

> **Java 25 image note:** `backend/Dockerfile` uses `maven:3.9-eclipse-temurin-25`
> and `eclipse-temurin:25-jre-jammy` to match `<java.version>25</java.version>`
> in `pom.xml`. If your Docker registry/mirror doesn't have Java 25 images yet,
> either swap those tags for a JDK you do have, or lower `java.version` in
> `backend/pom.xml` to match your available JDK (e.g. 21) and update the
> Dockerfile tags to match.

> **CORS:** `backend/src/main/java/com/smartcare/config/WebConfig.java` enables
> CORS for all endpoints, since the browser-based frontend now runs on a
> different origin than the API (unlike the old desktop client). Make sure
> this file is included in your build.

### Deploying the backend to a cloud VM / server without Docker

```bash
cd backend
./mvnw clean package -DskipTests
# produces target/demo-0.0.1-SNAPSHOT.war (runnable)

export DB_URL="jdbc:mysql://<db-host>:3306/smartcare_db"
export DB_USERNAME="smartcare"
export DB_PASSWORD="<your-password>"
export SERVER_PORT=9090

java -jar target/demo-0.0.1-SNAPSHOT.war
```

Run it as a background service with `systemd`, `pm2`, or behind `nginx` as a
reverse proxy with TLS for production use.

### Backend environment variables

| Variable | Default | Description |
|---|---|---|
| `DB_URL` | `jdbc:mysql://localhost:3306/smartcare_db` | JDBC connection string |
| `DB_USERNAME` | `root` | MySQL username |
| `DB_PASSWORD` | `root` | MySQL password |
| `DDL_AUTO` | `update` | Hibernate schema behavior (`validate` recommended in production once schema is stable) |
| `SHOW_SQL` | `true` | Log SQL statements |
| `SERVER_PORT` | `9090` | HTTP port |

---

## 2. Run the frontend (React web app)

```bash
cd frontend
npm install
cp .env.example .env        # point VITE_API_URL at your backend, if not localhost:9090
npm run dev
```

Open the printed local URL (typically `http://localhost:5173`). Browsers
only grant webcam access on `localhost` or over `https://`, so serve it
accordingly if deploying beyond local dev.

For a production build:

```bash
npm run build
# static output in dist/ - serve with nginx, the backend, or any static host
```

**Face recognition note:** the old desktop app matched faces using Python's
`face_recognition` (dlib) library. Browsers can't run dlib, so the web
frontend uses `face-api.js` instead — its embeddings are **not** compatible
with previously-enrolled faces, so patients need to be re-enrolled once
through the new frontend. See `frontend/README.md` for details.

---

## 3. Quick local smoke test (everything on one machine)

```bash
# Terminal 1
docker compose up -d --build

# Terminal 2
cd frontend
npm install && npm run dev
```

The app defaults to `http://localhost:9090` for the backend, which matches
the backend container's published port, so no extra configuration is needed
for a single-machine setup.

---

## API summary

| Method | Path | Purpose |
|---|---|---|
| GET | `/departments` | List departments |
| POST | `/patients/register/basic` | Register a new patient |
| POST | `/patients/face/save` | Save a patient's face embedding |
| PUT | `/patients/face/update` | Update a patient's face embedding |
| GET | `/patients/faces` | Get all stored face embeddings (used for on-device matching) |
| GET | `/patients/{patientId}` | Get patient by ID |
| POST | `/patients/check-existing` | Look up a patient by personal details |
| POST | `/visits/create` | Create a visit |
| POST | `/visits/department/checkin` | Department check-in / queueing |
| POST | `/payment/validate` | Validate payment requirement for a visit |
| POST | `/payment/save` | Record a payment |
| GET | `/payment/latest` | Get the latest payment for a patient/department |

---

## Troubleshooting

- **Frontend can't reach the backend:** confirm `VITE_API_URL` (in
  `frontend/.env`) matches where the backend is actually running/exposed,
  and check the browser console for CORS errors (see the CORS note above).
- **Backend can't connect to MySQL in Docker:** wait for the `mysql` service's
  healthcheck to pass (`docker compose ps`) — the backend is configured to
  wait for it automatically.
- **Webcam not detected / permission denied:** browsers require `localhost`
  or `https://` to grant camera access, and the user must accept the
  permission prompt on first load.
- **Face not recognized after switching to the new frontend:** expected for
  patients enrolled by the old desktop app — the embedding formats aren't
  compatible. Re-enroll their face once through Registration or Patient
  Recovery → face update.
