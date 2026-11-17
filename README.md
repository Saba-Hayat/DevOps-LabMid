# DevOps Lab Mid - Assignment Submission Portal

**Course:** DevOps for Cloud Computing (CSC418)  
**University:** COMSATS University Islamabad, Attock Campus  
**Instructor:** Mr. Babar Shazad  
**Student:** Saba Hayat

## Project Overview

A Flask-based assignment submission portal with automated testing through GitHub Actions. Every push triggers tests. The pipeline generates a JSON report and sends it to a local HTTP receiver through a Cloudflare Quick Tunnel.

## Features

- Assignment submission form.
- Required-field validation.
- HTTP/HTTPS submission URL validation.
- JSON storage and display of valid submissions.
- Automated pytest test cases.
- GitHub Actions CI on every push.
- JSON test report containing individual test results and failure messages.
- Authenticated report delivery to a local receiver.
- Local report saved at `reports/test-report.json`.

## Project Setup

### 1. Clone the repository

```powershell
git clone https://github.com/Saba-Hayat/DevOps-LabMid.git
cd DevOps-LabMid
```

### 2. Create and activate virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

## Run the Application

```powershell
python run.py
```

Open the local URL displayed by Flask in your browser.

## Execute Automated Tests

```powershell
python -m pytest -v
```

To generate a JSON test report locally:

```powershell
python -m pytest -v --json-report --json-report-file=pytest-report.json
```

## Start the Local Report Receiver

Set the same secret token configured in GitHub:

```powershell
$env:REPORT_TOKEN = "YOUR_REPORT_TOKEN"
python receiver.py
```

The receiver listens on port `5001`.

Health endpoint:

```text
http://127.0.0.1:5001/health
```

Report endpoint:

```text
http://127.0.0.1:5001/report
```

## Expose the Receiver Using Cloudflare Tunnel

Keep the receiver running in one terminal. Open another terminal and run:

```powershell
cloudflared tunnel --url http://127.0.0.1:5001
```

Copy the generated HTTPS URL and append `/report`.

## Configure GitHub Secrets

In the repository, open:

**Settings → Secrets and variables → Actions**

Create these repository secrets:

- `REPORT_TOKEN`: The same token used by the local receiver.
- `REPORT_URL`: The Cloudflare HTTPS tunnel URL ending in `/report`.

If the temporary Quick Tunnel URL changes, update `REPORT_URL`.

## CI Report Contents

The automatically delivered JSON report includes:

- Repository name.
- Branch name.
- Commit SHA.
- GitHub Actions run identifier.
- Execution timestamp.
- Individual test names and results.
- Failure messages where applicable.
- Total, passed and failed test counts.
- Overall pipeline test status.

The local receiver automatically saves the latest report to:

```text
reports/test-report.json
```

The report is replaced after every successful delivery, including failing test runs.

## Demonstration

The required demonstration consists of:

1. Push code with all tests passing.
2. Introduce a controlled defect and push again.
3. Verify that tests fail and the failing report reaches the local receiver.
4. Fix the defect and push again.
5. Verify that tests pass and the local JSON report is updated.

## GitHub Repository

https://github.com/Saba-Hayat/DevOps-LabMid
