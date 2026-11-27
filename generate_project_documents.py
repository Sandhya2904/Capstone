from datetime import date
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.shared import Inches, Pt


ROOT = Path(__file__).resolve().parent
SCREENSHOTS = ROOT / "screenshots"


def add_title(doc, title, subtitle=None):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(title)
    r.bold = True
    r.font.size = Pt(20)
    if subtitle:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(subtitle)
        r.italic = True
        r.font.size = Pt(11)


def add_heading(doc, text, level=1):
    p = doc.add_heading(text, level=level)
    p.paragraph_format.keep_with_next = True


def add_bullets(doc, items):
    for item in items:
        doc.add_paragraph(item, style="List Bullet")


def add_numbered(doc, items):
    for item in items:
        doc.add_paragraph(item, style="List Number")


def add_table(doc, headers, rows, widths=None):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for index, header in enumerate(headers):
        cell = table.rows[0].cells[index]
        cell.text = header
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.bold = True
    for row in rows:
        cells = table.add_row().cells
        for index, value in enumerate(row):
            cells[index].text = str(value)
    if widths:
        for row in table.rows:
            for index, width in enumerate(widths):
                row.cells[index].width = Inches(width)


def add_screenshot(doc, filename, caption):
    path = SCREENSHOTS / filename
    if path.exists():
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(str(path), width=Inches(6.4))
        c = doc.add_paragraph(caption)
        c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in c.runs:
            run.italic = True
    else:
        doc.add_paragraph(f"Screenshot unavailable: {filename}")


def base_document(title, subtitle):
    doc = Document()
    section = doc.sections[0]
    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.7)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)
    add_title(doc, title, subtitle)
    doc.add_paragraph(f"Prepared: {date.today().isoformat()}")
    doc.add_paragraph("Repository: https://github.com/Sandhya2904/Capstone")
    doc.add_page_break()
    return doc


# Document 1: architecture and implementation
architecture = base_document(
    "NetPulse Project Architecture and Implementation",
    "Capstone Hands-on 1 - FastAPI, In-Memory Repository, MySQL and Alembic",
)
add_heading(architecture, "1. Project Overview")
architecture.add_paragraph(
    "NetPulse is a layered modular-monolith API for registering network devices, updating status, "
    "and creating one alert for the first online-to-offline transition. The application does not "
    "ping real devices or use a database in its baseline mode."
)

add_heading(architecture, "2. Technology Stack")
add_table(architecture,
    ["Area", "Technology"],
    [
        ("API", "FastAPI, Pydantic"),
        ("Server", "Uvicorn"),
        ("Tests", "pytest, TestClient"),
        ("In-memory mode", "Python dictionaries and lists"),
        ("MySQL mode", "SQLAlchemy, PyMySQL"),
        ("Schema migrations", "Alembic"),
        ("Configuration", "python-dotenv"),
        ("Interface", "Swagger UI / OpenAPI 3.1"),
    ],
    [1.6, 4.8],
)

add_heading(architecture, "3. Layer Responsibilities")
add_table(architecture,
    ["Layer", "Responsibility", "Main files"],
    [
        ("Routes", "HTTP endpoints and status-code/error translation", "app/routes/devices.py"),
        ("Models", "Pydantic request/response schemas and IPv4 validation", "app/models.py"),
        ("Service", "Registration, lookup, status and transition rules", "app/services/device_service.py"),
        ("Repository", "In-memory or MySQL persistence behind one interface", "app/repositories/*.py"),
        ("Events", "Creates offline alerts", "app/events.py"),
        ("Database", "SQLAlchemy engine, ORM entities and session dependency", "app/db/*.py"),
        ("Migrations", "Creates and evolves database tables", "alembic/versions/*.py"),
    ],
    [1.2, 3.2, 2.0],
)

add_heading(architecture, "4. Offline Alert Rule")
architecture.add_paragraph(
    "The DeviceService reads the stored status before updating it. It calls create_offline_alert() "
    "only when the stored status is online and the requested status is offline. Initial offline "
    "registration and repeated offline updates do not create additional alerts."
)

add_heading(architecture, "5. Repository Structure")
architecture.add_paragraph(
    "NetPulse/\n"
    "  app/\n"
    "    main.py                 FastAPI application\n"
    "    models.py               Pydantic API models\n"
    "    dependencies.py         Shared repository selection\n"
    "    events.py               Offline alert event\n"
    "    routes/devices.py       REST endpoints\n"
    "    services/               Business rules\n"
    "    repositories/           In-memory and MySQL repositories\n"
    "    db/                     SQLAlchemy session and ORM models\n"
    "  alembic/                  Migration environment and revisions\n"
    "  tests/                    Service and HTTP test suites\n"
    "  .env.example             MySQL environment template\n"
    "  requirements.txt         Python dependencies\n"
    "  README.md                Setup and usage guide"
)

add_heading(architecture, "6. API Contract")
add_table(architecture,
    ["Method", "Path", "Success", "Error"],
    [
        ("POST", "/devices", "201", "409 duplicate; 422 invalid"),
        ("GET", "/devices", "200", "-"),
        ("GET", "/devices/{device_id}", "200", "404"),
        ("PATCH", "/devices/{device_id}/status", "200", "404; 422"),
        ("GET", "/alerts", "200", "-"),
        ("GET", "/health", "200", "-"),
    ],
    [0.8, 2.7, 0.8, 2.0],
)

add_heading(architecture, "7. Repository Swappability")
architecture.add_paragraph(
    "Both repository implementations expose the same methods: add_device, list_devices, get_device, "
    "update_status, save_alert, and list_alerts. Therefore, DeviceService and app/events.py do not "
    "need to change when the in-memory implementation is replaced with MySQL."
)
architecture.save(ROOT / "1_NetPulse_Architecture_and_Implementation.docx")


# Document 2: setup, test cases and execution report
testing = base_document(
    "NetPulse Setup, Test Cases and Execution Report",
    "Automated Tests and Live HTTP Verification",
)
add_heading(testing, "1. Environment Setup")
add_numbered(testing, [
    "Created Python virtual environment: python3 -m venv .venv",
    "Activated environment: source .venv/bin/activate",
    "Installed dependencies: python -m pip install -r requirements.txt",
    "Started API: python -m uvicorn app.main:app --reload",
])

testing.add_paragraph("Primary URLs:")
add_bullets(testing, [
    "Swagger UI: http://127.0.0.1:8000/docs",
    "OpenAPI JSON: http://127.0.0.1:8000/openapi.json",
])

add_heading(testing, "2. Automated Test Cases")
add_table(testing,
    ["Case", "Expected result", "Result"],
    [
        ("Device registration", "Device is stored and returned", "Pass"),
        ("Duplicate registration", "DeviceAlreadyExistsError", "Pass"),
        ("Missing device", "DeviceNotFoundError", "Pass"),
        ("Initial offline registration", "No alert is created", "Pass"),
        ("Online-to-offline transition", "Exactly one alert", "Pass"),
        ("Repeated offline update", "Alert count remains one", "Pass"),
        ("Health endpoint", "Returns status ok", "Pass"),
        ("OpenAPI contract", "Six operations are listed", "Pass"),
        ("Duplicate HTTP registration", "HTTP 409", "Pass"),
        ("Invalid IPv4", "HTTP 422", "Pass"),
    ],
    [2.5, 2.5, 1.0],
)

testing.add_paragraph(
    "Final automated result: 10 passed. The suite uses a fresh InMemoryDeviceRepository for each test "
    "and also validates live HTTP behavior through FastAPI TestClient."
)

add_heading(testing, "3. RTR-101 Live Walkthrough")
add_numbered(testing, [
    "POST /devices with RTR-101 and status online: HTTP 201.",
    "PATCH /devices/RTR-101/status with status offline: HTTP 200.",
    "PATCH the same device to offline again: HTTP 200.",
    "GET /alerts: exactly one alert for RTR-101.",
    "Re-POST RTR-101: HTTP 409.",
])

add_heading(testing, "4. Additional HTTP Verification")
add_table(testing,
    ["Request", "Verified status"],
    [
        ("GET /health", "200 with {status: ok}"),
        ("GET /devices/MISSING", "404"),
        ("Invalid IPv4 payload", "422"),
        ("GET /openapi.json", "200"),
    ],
    [3.2, 3.2],
)

add_heading(testing, "5. MySQL and Alembic Notes")
testing.add_paragraph(
    "The MySQL repository, SQLAlchemy models, environment template, and Alembic revisions were "
    "implemented. Live MySQL migration execution requires a running MySQL server and database/user "
    "configuration from .env. The in-memory baseline is executable without MySQL."
)
testing.save(ROOT / "2_NetPulse_Test_Cases_and_Execution_Report.docx")


# Document 3: screenshot evidence and submission
evidence = base_document(
    "NetPulse Submission Evidence",
    "Screenshots and Completion Checklist",
)
add_heading(evidence, "1. Submission Evidence Summary")
add_bullets(evidence, [
    "Swagger UI displaying all six API operations.",
    "OpenAPI 3.1 contract generated from FastAPI routes and Pydantic models.",
    "Passing automated pytest result.",
    "Live RTR-101 registration and repeated-offline walkthrough.",
    "MySQL/Alembic implementation and schema-evolution migration files.",
])

add_heading(evidence, "2. Swagger UI - Endpoint Evidence")
add_screenshot(evidence, "01_swagger_endpoints.png", "Figure 1: Swagger UI showing devices, alerts and health operations")

add_heading(evidence, "3. OpenAPI Contract Evidence")
add_screenshot(evidence, "02_openapi_contract.png", "Figure 2: Generated /openapi.json contract")

add_heading(evidence, "4. Exact RTR-101 Swagger Inputs")
evidence.add_paragraph("Registration JSON:")
evidence.add_paragraph(
    '{\n  "device_id": "RTR-101",\n  "name": "Branch Router",\n  "device_type": "router",\n'
    '  "ip_address": "192.168.10.1",\n  "status": "online"\n}'
)
evidence.add_paragraph("Status update JSON:")
evidence.add_paragraph('{ "status": "offline" }')

add_heading(evidence, "5. Execution Checklist")
add_table(evidence,
    ["Requirement", "Evidence"],
    [
        ("Six endpoints visible", "Swagger screenshot and OpenAPI paths"),
        ("Successful RTR-101 registration", "HTTP 201"),
        ("One alert after two offline updates", "HTTP 200 twice; alert count remains one"),
        ("Passing pytest", "10 passed"),
        ("MySQL/Alembic files", "app/db, app/repositories/mysql_device_repository.py, alembic/versions"),
        ("GitHub repository", "https://github.com/Sandhya2904/Capstone"),
        ("Repository interface", "Routes and service unchanged across storage implementations"),
    ],
    [3.2, 3.2],
)

evidence.save(ROOT / "3_NetPulse_Submission_Evidence_Screenshots.docx")

print("Created:")
print(ROOT / "1_NetPulse_Architecture_and_Implementation.docx")
print(ROOT / "2_NetPulse_Test_Cases_and_Execution_Report.docx")
print(ROOT / "3_NetPulse_Submission_Evidence_Screenshots.docx")
