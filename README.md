# Wealth Advisor Assistant – Multi-Agent AI System

## Overview

This project implements a lightweight multi-agent Wealth Advisor Assistant capable of:

* Ingesting client financial data
* Performing portfolio analysis
* Evaluating financial risk
* Detecting anomalies
* Supporting Human-in-the-Loop (HITL) validation
* Generating structured advisory insights

The system is implemented using LangGraph-based orchestration with modular agents, structured workflow state, persistent checkpoints, logging, and Groq LLM integration.

The implementation focuses on clean architecture, modularity, observability, and production-oriented workflow design.

---

# Architecture Design

## Workflow Graph

The application is implemented as a stateful LangGraph workflow.

```text
start
  │
  ▼
data_fetcher
  │
  ▼
portfolio_analyzer
  │
  ▼
orchestrator
  │
  ├──────────────► advisory_agent
  │
  ▼
risk_evaluator
  │
  ▼
anomaly_detector
  │
  ▼
human_review
  │
  ├──────────────► rejected ───► end
  │
  ▼
advisory_agent
  │
  ▼
end
```

---

## Agent Responsibilities

### 1. Data Fetcher Agent

Responsible for:

* Loading client financial data
* Preparing structured workflow state
* Fetching contextual client information
* Handling incomplete or missing data

This agent acts as the entry point for financial data ingestion.

---

### 2. Portfolio Analyzer Agent

Responsible for:

* Portfolio analysis
* Transaction analysis
* Financial pattern evaluation
* Generating structured portfolio summaries

This stage prepares analytical context for downstream risk evaluation.

---

### 3. Orchestrator Agent

Acts as the workflow controller.

Responsibilities:

* Managing workflow transitions
* Routing execution between agents
* Deciding whether deeper evaluation is required
* Coordinating the final advisory flow

The orchestrator is implemented using LangGraph state transitions.

---

### 4. Risk Evaluator Agent

Responsible for:

* Evaluating financial risk exposure
* Assessing portfolio risk signals
* Identifying potentially risky financial behavior

This stage determines whether anomaly review and HITL validation are required.

---

### 5. Anomaly Detector Agent

Responsible for identifying:

* Unusual transactions
* Sudden balance changes
* High-risk financial behavior
* Abnormal spending patterns

Detected anomalies are added to the workflow state for downstream review.

---

### 6. Human Review (HITL)

The workflow supports Human-in-the-Loop validation for high-risk scenarios.

Capabilities:

* Manual review
* Approval/rejection of workflow continuation
* Validation of high-risk financial decisions
* Workflow interruption and resume

If the request is rejected during human review, the workflow terminates safely.

---

### 7. Advisory Agent

Responsible for generating the final structured advisory response.

The advisory generation layer uses Groq LLM with:

* Portfolio analysis
* Risk evaluation
* Detected anomalies
* Client financial context

The final output includes:

* Financial insights
* Risk observations
* Advisory recommendations
* Suggested next actions

---

# Agent Interaction Flow

## End-to-End Execution Flow

```text
Client Financial Data
        │
        ▼
Data Fetcher Agent
        │
        ▼
Portfolio Analyzer Agent
        │
        ▼
Orchestrator Agent
        │
        ▼
Risk Evaluator Agent
        │
        ▼
Anomaly Detector Agent
        │
        ▼
Human Review (Optional)
        │
        ▼
Advisory Agent
        │
        ▼
Structured Advisory Response
```

---

# State Management

The workflow uses structured shared state between agents.

The workflow state contains:

* Client details
* Portfolio data
* Transaction history
* Risk evaluation results
* Anomaly summaries
* HITL review status
* Advisory responses

This approach provides:

* Deterministic workflows
* Traceable execution
* Easier debugging
* Consistent inter-agent communication

---

# Persistence and Checkpointing

The application persists workflow state to support:

* Human-in-the-Loop interruptions
* Resume functionality
* Workflow recovery
* Stateful execution

This enables long-running and interruptible workflows.

---

# Logging and Observability

The application includes centralized logging for:

* Workflow execution
* Agent transitions
* Errors and exceptions
* Routing decisions
* HITL actions

Example log structure:

```text
logs/
├── system.log
├── wealth_advisor.log
```

The logging layer is designed to support date-wise rotating logs for scalability and debugging.

---

# Key Design Decisions and Trade-Offs

## 1. LangGraph-Based Orchestration

### Decision

LangGraph was selected for implementing the workflow.

### Why

* Stateful workflows
* Native graph orchestration
* HITL compatibility
* Easier debugging
* Persistent checkpoint support

### Trade-Off

Adds architectural complexity compared to sequential pipelines, but significantly improves workflow control and scalability.

---

## 2. Multi-Agent Architecture

### Decision

The workflow was intentionally divided into specialized agents.

### Why

* Separation of concerns
* Independent testing
* Easier maintenance
* Better extensibility
* Cleaner debugging boundaries

### Trade-Off

Requires orchestration and shared state management.

---

## 3. Structured State Instead of Free-Form Messaging

### Decision

Agents communicate using structured workflow state.

### Why

* Predictable data flow
* Easier validation
* Deterministic execution
* Better observability

### Trade-Off

Requires additional schema management.

---

## 4. Human-in-the-Loop (HITL)

### Decision

HITL support was added for high-risk financial scenarios.

### Why

* Enables manual validation
* Adds workflow safety
* Improves trustworthiness
* Supports interrupt/resume workflows

### Trade-Off

Adds workflow complexity and additional API coordination.

---

## 5. Groq LLM Integration

### Decision

Groq LLM is used for final advisory generation.

### Why

* Fast inference
* Low latency
* Good structured reasoning performance
* Suitable for agentic systems

### Trade-Off

LLM outputs still require validation in real financial environments.

---

# Assumptions Made

* Financial data is provided in valid JSON format.
* CRM integrations are mocked/simulated.
* The application is designed as a prototype system.
* Advisory outputs are informational and not regulatory financial advice.
* Anomaly detection is logic/rule-based for assignment scope.
* Enterprise authentication/security is simplified.

---

# Error Handling

The system includes graceful error handling across agents and tools.

Handled scenarios include:

* Missing client data
* Invalid payloads
* API failures
* LLM invocation failures
* Workflow interruptions

Example:

```python
try:
    response = crm_tool.get_client_data()
except Exception:
    logger.exception("CRM API failed")
    response = {}
```

---

# Project Structure

```text
app/
├── agents/
│   ├── data_fetcher_agent.py
│   ├── portfolio_analyzer_agent.py
│   ├── orchestrator_agent.py
│   ├── risk_evaluator_agent.py
│   ├── anomaly_detector_agent.py
│   └── advisory_agent.py
│
├── graph/
│   ├── graph.py
│   ├── state.py
│   └── checkpointer.py
│
├── services/
│   └── logging_service.py
│
├── models/
│   └── client_memory.py
│
├── logs/
│
├── docker-compose.yml
├── Dockerfile
└── main.py
```

---

# Instructions to Run the Project

## 1. Clone the Repository

```bash
git clone <repository_url>
cd wealth-advisor-assistant
```

---

## 2. Create Environment File

Create a `.env` file using `.env.example`.

Example:

```env
ENV=development
LOG_LEVEL=INFO

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=wealth_advisor

DATABASE_URL=postgresql://postgres:postgres@postgres:5432/wealth_advisor

GROQ_API_KEY=your_groq_api_key
LLM_MODEL=llama-3.3-70b-versatile
```

---

## 3. Start the Application

Run:

```bash
docker compose up --build
```

This will start:

* API service
* PostgreSQL database
* Workflow services

---

## 4. Ingest Client Financial Data

After the containers are running, ingest sample financial data using the ingestion API endpoint.

Example:

```bash
POST /ingest
```

This stores the client financial data in PostgreSQL and initializes workflow state.

---

## 5. Trigger Workflow Execution

Run the workflow using the advisory endpoint.

Example:

```bash
POST /advisory
```

The workflow executes:

* Portfolio analysis
* Risk evaluation
* Anomaly detection
* HITL routing (if high risk)
* Advisory generation

---

## 6. Test Human-in-the-Loop (HITL)

To test the HITL flow:

1. Ingest high-risk financial data
2. Run workflow execution
3. The workflow pauses at the `human_review` stage
4. Use the HITL API endpoint to approve or reject the workflow

Example:

```bash
POST /hitl/review
```

Possible actions:

* approve
* reject

If approved:

```text
human_review → advisory_agent → end
```

If rejected:

```text
human_review → rejected → end
```

---

# API Endpoints

## Health Check

```http
GET /health
```

Checks application health status.

---

## Fetch Clients

```http
GET /clients
```

Returns stored client records.

---

## Run Advisory Workflow

```http
POST /advisory/run/{client_id}
```

Triggers the advisory workflow for a given client.

The workflow executes:

* Portfolio analysis
* Risk evaluation
* Anomaly detection
* Human review routing (if high risk)
* Advisory generation

No request body is required for initial execution.

Example:

```http
POST /advisory/run/C101
```

---

## Create HITL Test Client

```http
POST /clients/hitl
```

Creates a high-risk client profile specifically for testing the Human-in-the-Loop workflow.

The generated client contains:

* High-risk portfolio signals
* Large abnormal transactions
* Risk indicators that trigger human review

This endpoint automatically stores the client in PostgreSQL.

---

# Testing Human-in-the-Loop (HITL)

## Step 1 – Create High-Risk Test Client

Run:

```http
POST /clients/hitl
```

This creates a test client designed to trigger the `human_review` node.

---

## Step 2 – Trigger Advisory Workflow

Run:

```http
POST /advisory/run/{client_id}
```

Example:

```http
POST /advisory/run/C101
```

No request body is required.

At this stage:

```text
risk_evaluator → anomaly_detector → human_review
```

The workflow pauses waiting for manual approval.

---

## Step 3 – Approve or Reject Human Review

Call the same advisory endpoint again with review payload.

Example:

```http
POST /advisory/run/C101
```

Request Body:

```json
{
  "approved": true,
  "advisor_notes": "Client activity reviewed and approved for advisory generation"
}
```

Possible outcomes:

### Approved

```text
human_review → advisory_agent → end
```

### Rejected

```text
human_review → rejected → end
```

Example rejection payload:

```json
{
  "approved": false,
  "advisor_notes": "High-risk transaction requires further investigation"
}
```

---

# Example Workflow Response

```json
{
  "client_id": "C101",
  "risk_level": "High",
  "anomalies_detected": [
    "Large withdrawal detected",
    "High-risk portfolio exposure"
  ],
  "hitl_required": true,
  "workflow_status": "waiting_for_human_review"
}
```

---

# Future Improvements

Potential future enhancements:

* ML-based anomaly detection
* Async agent execution
* Real-time streaming workflows
* OpenTelemetry observability
* Vector memory integration
* Role-based access control
* Monitoring dashboards
* Container orchestration support

---

# Conclusion

This project demonstrates a modular multi-agent financial advisory workflow built using LangGraph orchestration, structured state management, persistent workflows, and Human-in-the-Loop validation.

The implementation emphasizes:

* Modular architecture
* Stateful execution
* Workflow traceability
* Reliability
* Observability
* Extensibility
* Production-oriented engineering practices

The design is intentionally extensible for future enterprise-grade agentic financial systems.
