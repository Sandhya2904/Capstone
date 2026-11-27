from datetime import date
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt


ROOT = Path(__file__).resolve().parent
SCREENSHOTS = ROOT / "screenshots"


def title(doc, text, subtitle):
    paragraph = doc.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run(text)
    run.bold = True
    run.font.size = Pt(22)

    paragraph = doc.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run(subtitle)
    run.italic = True
    run.font.size = Pt(11)


def heading(doc, text, level=1):
    paragraph = doc.add_heading(text, level=level)
    paragraph.paragraph_format.keep_with_next = True


def bullets(doc, items):
    for item in items:
        doc.add_paragraph(item, style="List Bullet")


def numbered(doc, items):
    for item in items:
        doc.add_paragraph(item, style="List Number")


def table(doc, headers, rows, widths):
    grid = doc.add_table(rows=1, cols=len(headers))
    grid.style = "Table Grid"
    grid.alignment = WD_TABLE_ALIGNMENT.CENTER
    for index, header in enumerate(headers):
        grid.rows[0].cells[index].text = header
        for paragraph in grid.rows[0].cells[index].paragraphs:
            for run in paragraph.runs:
                run.bold = True
    for row in rows:
        cells = grid.add_row().cells
        for index, value in enumerate(row):
            cells[index].text = str(value)
    for row in grid.rows:
        for index, width in enumerate(widths):
            row.cells[index].width = Inches(width)


def screenshot(doc, filename, caption):
    path = SCREENSHOTS / filename
    if not path.exists():
        doc.add_paragraph(f"Screenshot unavailable: {filename}")
        return
    paragraph = doc.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.add_run().add_picture(str(path), width=Inches(6.4))
    paragraph = doc.add_paragraph(caption)
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in paragraph.runs:
        run.italic = True


doc = Document()
for section in doc.sections:
    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.7)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)

title(doc, "NetPulse Complete Project Report", "Architecture, Setup, Tests, Screenshots and Submission Evidence")
meta = doc.add_paragraph()
meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
meta.add_run(f"Prepared: {date.today().isoformat()}\n")
meta.add_run("Repository: https://github.com/Sandhya2904/Capstone")
doc.add_page_break()

heading(doc, "Contents")
for item in [
    "1. Project Overview",
    "2. Technology Stack",
    "3. System Architecture",
    "4. API Contract",
    "5. Project Structure",
    "6. Setup and Execution",
    "7. In-Memory Repository",
    "8. MySQL and Alembic Integration",
    "9. Automated Test Cases",
    "10. Live HTTP Verification",
    "11. Screenshots and Submission Evidence",
    "12. GitHub Submission",
]:
    doc.add_paragraph(item)
doc.add_page_break()

heading(doc, "1. Project Overview")
doc.add_paragraph(
    "NetPulse is a layered FastAPI device-monitoring API for registering network devices, "
    "updating status, and recording one alert for the first online-to-offline transition. "
    "The project uses a modular-monolith structure with route, model, service, repository, "
    "event, database, and migration responsibilities."
)

heading(doc, "2. Technology Stack")
table(doc, ["Area", "Technology"], [
    ("API", "FastAPI, Pydantic"),
    ("Server", "Uvicorn"),
    ("Tests", "pytest, TestClient"),
    ("Baseline persistence", "Python dictionaries and lists"),
    ("MySQL persistence", "SQLAlchemy, PyMySQL"),
    ("Schema migrations", "Alembic"),
    ("Configuration", "python-dotenv"),
    ("Documentation", "Swagger UI / OpenAPI 3.1"),
], [1.8, 4.6])

heading(doc, "3. System Architecture")
table(doc, ["Layer", "Responsibility", "Main file(s)"], [
    ("Routes", "Expose REST endpoints and translate domain errors to HTTP", "app/routes/devices.py"),
    ("Models", "Validate API payloads and define response schemas", "app/models.py"),
    ("Service", "Registration, lookup, status and offline-transition rules", "app/services/device_service.py"),
    ("Repository", "Implement in-memory or MySQL storage", "app/repositories/*.py"),
    ("Events", "Create offline alert records", "app/events.py"),
    ("Database", "Engine, sessions and SQLAlchemy ORM entities", "app/db/*.py"),
    ("Migrations", "Create and evolve MySQL tables", "alembic/versions/*.py"),
], [1.2, 3.2, 2.0])

doc.add_paragraph(
    "The offline alert rule is owned by DeviceService. It only calls create_offline_alert() "
    "when an existing device changes from stored status online to requested status offline. "
    "Initial offline registration and repeated offline updates create no additional alert."
)

heading(doc, "4. API Contract")
table(doc, ["Method", "Path", "Success", "Documented errors"], [
    ("POST", "/devices", "201", "409 duplicate; 422 invalid"),
    ("GET", "/devices", "200", "-"),
    ("GET", "/devices/{device_id}", "200", "404; 422"),
    ("PATCH", "/devices/{device_id}/status", "200", "404; 422"),
    ("GET", "/alerts", "200", "-"),
    ("GET", "/health", "200", "-"),
], [0.8, 2.6, 0.8, 2.2])

heading(doc, "5. Project Structure")
doc.add_paragraph(
    "app/\n"
    "  main.py                 FastAPI application\n"
    "  models.py               Pydantic request and response models\n"
    "  dependencies.py         Shared repository dependency and MySQL selection\n"
    "  events.py               Offline alert event\n"
    "  routes/devices.py       REST routes\n"
    "  services/               DeviceService business rules\n"
    "  repositories/           InMemoryDeviceRepository and MySqlDeviceRepository\n"
    "  db/                     SQLAlchemy session and ORM models\n"
    "alembic/                  Migration environment and revisions\n"
    "tests/                    Automated service and HTTP tests\n"
    "screenshots/              Submission screenshots\n"
    "README.md                 Setup and usage documentation\n"
    "requirements.txt          Python dependencies"
)

heading(doc, "6. Setup and Execution")
numbered(doc, [
    "Create the virtual environment: python3 -m venv .venv",
    "Activate it: source .venv/bin/activate",
    "Install dependencies: python -m pip install -r requirements.txt",
    "Run tests: python -m pytest -q",
    "Start the server: python -m uvicorn app.main:app --reload",
])
bullets(doc, [
    "Swagger UI: http://127.0.0.1:8000/docs",
    "OpenAPI JSON: http://127.0.0.1:8000/openapi.json",
])

heading(doc, "7. In-Memory Repository")
doc.add_paragraph(
    "The default repository stores devices and alerts in instance-level dictionaries and lists. "
    "The state is shared across requests but resets when the process restarts. Callers receive "
    "copies of stored objects so accidental mutation is prevented."
)

heading(doc, "8. MySQL and Alembic Integration")
doc.add_paragraph(
    "The MySqlDeviceRepository implements the exact repository interface used by the in-memory "
    "repository. It commits writes, rolls back on failures, and translates duplicate-key errors "
    "to DeviceAlreadyExistsError. SQLAlchemy models separate ORM persistence from Pydantic API schemas."
)
doc.add_paragraph(
    "Alembic migration 20261127_001 creates devices and alerts. Migration 20261127_002 demonstrates "
    "the evolving schema by adding and removing an optional location column."
)
doc.add_paragraph(
    "Example migration commands: alembic upgrade head, alembic current, alembic downgrade -1, "
    "and alembic upgrade head. Live MySQL execution requires a running MySQL server and a configured .env."
)

heading(doc, "9. Automated Test Cases")
table(doc, ["Test", "Expected result", "Result"], [
    ("Device registration", "Stored and returned", "Pass"),
    ("Duplicate registration", "DeviceAlreadyExistsError", "Pass"),
    ("Missing device", "DeviceNotFoundError", "Pass"),
    ("Initial offline registration", "No alert", "Pass"),
    ("Online-to-offline transition", "One alert", "Pass"),
    ("Repeated offline update", "Alert count remains one", "Pass"),
    ("Health endpoint", "status ok", "Pass"),
    ("OpenAPI contract", "Six operations listed", "Pass"),
    ("Duplicate HTTP request", "409", "Pass"),
    ("Invalid IPv4", "422", "Pass"),
], [2.5, 2.5, 1.0])
doc.add_paragraph("Final automated result: 10 tests passed with 1 dependency deprecation warning.")

heading(doc, "10. Live HTTP Verification")
heading(doc, "RTR-101 Walkthrough", 2)
numbered(doc, [
    "POST /devices with RTR-101: HTTP 201.",
    "PATCH /devices/RTR-101/status with offline: HTTP 200.",
    "PATCH RTR-101 to offline again: HTTP 200.",
    "GET /alerts: exactly one RTR-101 offline alert.",
    "Re-register RTR-101: HTTP 409.",
])

table(doc, ["Request", "Verified result"], [
    ("GET /health", "200, {status: ok}"),
    ("GET /devices/MISSING", "404"),
    ("Invalid IPv4 device payload", "422"),
    ("GET /openapi.json", "200"),
], [3.2, 3.2])

heading(doc, "11. Screenshots and Submission Evidence")
heading(doc, "Swagger UI", 2)
screenshot(doc, "01_swagger_endpoints.png", "Figure 1: Swagger UI displaying the six NetPulse operations")

heading(doc, "OpenAPI Contract", 2)
screenshot(doc, "02_openapi_contract.png", "Figure 2: Generated OpenAPI 3.1 JSON contract")

heading(doc, "Exact RTR-101 Request Payloads", 2)
doc.add_paragraph("Registration:")
doc.add_paragraph(
    '{\n  "device_id": "RTR-101",\n  "name": "Branch Router",\n'
    '  "device_type": "router",\n  "ip_address": "192.168.10.1",\n  "status": "online"\n}'
)
doc.add_paragraph("Status update:")
doc.add_paragraph('{ "status": "offline" }')

heading(doc, "Completion Checklist")
table(doc, ["Requirement", "Evidence"], [
    ("Six endpoints visible", "Swagger and OpenAPI"),
    ("Registration works", "HTTP 201"),
    ("Duplicate ID rejected", "HTTP 409"),
    ("Missing device rejected", "HTTP 404"),
    ("Repeated offline creates one alert", "HTTP 200 twice; one alert"),
    ("Automated tests pass", "10 passed"),
    ("MySQL repository exists", "MySqlDeviceRepository implemented"),
    ("Alembic migrations exist", "Initial and evolving schema revisions"),
], [3.2, 3.2])

heading(doc, "12. GitHub Submission")
doc.add_paragraph("Repository: https://github.com/Sandhya2904/Capstone")
doc.add_paragraph("Branch: main")
doc.add_paragraph("The complete project source, reports, screenshots and migration files are tracked in this repository.")

output = ROOT / "NetPulse_Complete_Project_Report.docx"
doc.save(output)
print(output)
