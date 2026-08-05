AI-Powered Health Claim Processing Platform
Enterprise Healthcare Backend • AI Agents • Domain-Driven Design • Event-Driven Architecture

Production-grade backend demonstrating how Large Language Models (LLMs) safely integrate with healthcare systems through validated AI tools, clinical workflows, transactional guarantees, and Domain-Driven Design.

Built with Python, FastAPI, PostgreSQL, Redis, and modern AI engineering practices.














</div>
Overview

Modern healthcare systems generate enormous amounts of structured and unstructured information:

Medical records
Prior authorizations
Insurance claims
Provider documentation
Clinical notes
Patient communications

This project demonstrates how Artificial Intelligence can safely assist healthcare operations without bypassing business rules or compliance requirements.

Unlike AI demos that allow an LLM to interact directly with databases, this platform ensures every AI-generated action follows the exact same workflow as a human user.

AI becomes an intelligent orchestration layer, not the source of truth.

Why This Project Exists

Healthcare organizations spend millions of hours every year on repetitive administrative work.

Examples include:

Reviewing insurance claims
Registering patients
Scheduling follow-up appointments
Validating provider information
Processing prior authorizations
Explaining claim denials
Extracting information from clinical documents

This platform demonstrates how AI Agents can automate those workflows while preserving security, auditability, and domain integrity.

AI Architecture

Instead of allowing an LLM to execute arbitrary code or query databases directly, the assistant interacts only through validated AI Tools.

User

↓

Natural Language

↓

OpenAI / LLM

↓

Structured Tool Calls

↓

Tool Registry

↓

JSON Schema Validation

↓

Authentication

↓

Authorization (RBAC)

↓

Application Use Cases

↓

Domain Model

↓

Database Transaction

↓

Transactional Outbox

↓

Event Bus

↓

Notification Services

↓

Audit Logs

Every AI action is:

authenticated
authorized
validated
audited
transactional
observable
AI Capabilities

The assistant can orchestrate healthcare workflows such as:

Patient Management
Register Patient
Find Patient
Update Patient Information
Medical Records
Create Medical Record
Update Medical Record
Retrieve Medical History
Claims Processing
Create Claim
Submit Claim
Approve Claim
Reject Claim
Explain Claim Denial
Prior Authorization
Submit Prior Authorization
Approve Prior Authorization
Reject Prior Authorization
Provider Management
Register Provider
Follow-up Management
Schedule Follow-up
Cancel Follow-up
Notifications
Send Patient Notification
AI Example

User asks:

Submit a claim for John Doe's MRI, notify his physician, and schedule a follow-up if the insurer rejects the claim.

The AI produces structured tool calls.

[
  {
    "tool": "submit_claim"
  },
  {
    "tool": "send_notification"
  },
  {
    "tool": "schedule_follow_up"
  }
]

Each tool delegates to an Application Use Case, ensuring all domain validations and business rules are enforced.

AI Design Principles

The assistant never:

writes SQL
bypasses repositories
bypasses authentication
skips domain validation
modifies aggregates directly

Instead it invokes application services exactly like a REST API.

Enterprise Architecture

This platform follows:

Domain-Driven Design
Clean Architecture
Hexagonal Architecture
SOLID Principles
CQRS
Repository Pattern
Unit of Work
Transactional Outbox
Dependency Injection
Optimistic Concurrency
Event-Driven Architecture
Bounded Contexts
health_claim_processing/

├── ai_assistant/
├── claims/
├── medical_records/
├── patients/
├── providers/
├── prior_authorization/
├── follow_up/
├── notifications/
└── shared/

Each bounded context follows:

presentation/

application/

domain/

infrastructure/
AI Assistant
ai_assistant/

presentation/

application/

domain/

    tooling/

tools/

infrastructure/

The AI Assistant itself is treated as its own bounded context.

AI Tool Framework

The platform contains a reusable AI Tool Framework.

Tool

↓

Tool Registry

↓

Tool Definition

↓

Tool Parameters

↓

Tool Execution

↓

Application Use Cases

New capabilities can be added simply by registering a new tool.

Example Tool
RegisterPatientTool

↓

RegisterPatientUseCase

↓

Patient Aggregate

↓

Patient Repository

The tool itself contains no business logic.

Security

Every AI request passes through:

JWT Authentication
Role-Based Authorization
Request Validation
Domain Validation
Audit Logging
Transaction Management
Healthcare AI Examples

The platform demonstrates AI-assisted workflows such as:

Clinical document extraction
Structured medical record generation
Insurance claim drafting
Claim denial explanation
Provider lookup
Prior authorization assistance
Patient communication drafting

These features are designed to assist healthcare professionals. Final decisions remain under human oversight.

Technology Stack
Layer	Technology
Backend	Python, FastAPI
AI	OpenAI API, Function Calling, Structured Outputs
Database	PostgreSQL
Cache	Redis
Messaging	Kafka / Redis Streams
ORM	SQLAlchemy
Validation	Pydantic
Testing	Pytest
Infrastructure	Docker
Engineering Goals

This project demonstrates how to build AI-enabled enterprise software that is:

Secure
Observable
Maintainable
Testable
Auditable
Transactional
Event Driven
Domain Centric
Future Roadmap
AI Conversation Memory
Retrieval-Augmented Generation (RAG)
FHIR Integration
HL7 Integration
Multi-Agent Collaboration
Voice Clinical Assistant
OpenTelemetry
Kubernetes Deployment
AI Evaluation Pipeline
Human-in-the-Loop Review
Multi-tenant SaaS Support
Author

Rowland Obi

Senior Backend Engineer

Specializing in:

Python
AI Backend Engineering
FastAPI
Django
Domain-Driven Design
Distributed Systems
PostgreSQL
Redis
Kafka
Event-Driven Architecture
