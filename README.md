# Credit-Based API Management  & Usage Control System 

## Problem Statement

Modern API platforms often struggle with:
- **Uncontrolled API consumption** from trial or free-tier users  
- **Untracked resource usage**, leading to unfair abuse of premium features  
- **Manual billing** and lack of transparency  
- **Lack of real-time alerts**, monitoring, or blocking when thresholds are breached

These pain points lead to:
- Poor infrastructure scalability  
- Revenue leakage  
- Dissatisfied legitimate users due to rate throttling

---

## Our Solution

We’ve built a **Multi-Tenant API Usage Monitoring & Billing System** that:

- Tracks **every API call** with service name, endpoint, tenant, and method  
- **Deducts credits** dynamically based on usage and per-endpoint configuration  
- Sends **real-time MQTT alerts** for credit exhaustion or warnings  
- Blocks users with **insufficient credits** using FastAPI middleware  
- Logs every usage event with timestamp and credit count  
-  Generates **invoices and usage summaries** using Celery Beat every 5 minutes for the user logged in
- Allows seamless proxying to downstream APIs using a unified `/api/proxy/...` endpoint  

---

## Key Features

| Feature           | Description                                                                                |
|-------------------|--------------------------------------------------------------------------------------------|
| JWT Auth + RBAC   | Login/Register, Token-based access with user/admin roles                                   |
| Credit-Based Billing | Deduct credits per API call, per endpoint                                                  |
| Access Blocking   | Prevent access when credits are exhausted                                                  |
| Monthly Invoices  | Invoices generated using `usage_logs` via Celery Beat every 5 minutes for the user logged in |
| Usage Tracking    | Logs to MongoDB with endpoint, service, time, and credits used                             |
| MQTT Alerts       | Real-time alerting when credit is low or exhausted                                         |
| Admin Controls  | Modify credits, subscriptions, endpoints via admin APIs                               |

---

## Tech Stack

| Tool             | Purpose                                                                                                      |
|------------------|--------------------------------------------------------------------------------------------------------------|
| **FastAPI**       | Backend API server                                                                                           |
| **MongoDB**       | Users, plans, usage logs, invoices, notifications, subscriptions, scheduled_summary, usage_summary, services |
| **Celery**        | Credit deduction, log writing                                                                                |
| **Celery Beat**   | Generates usage summaries of user logged in every 5 minutes                                                  |
| **EMQX (MQTT)**   | Publishes real-time usage alerts                                                                             |
| **JWT**           | Token authentication with user/tenant scoping                                                                |
| **Requests**      | Used for API proxying                                                                                        |

---

## How the System Works

### ➤ Proxy Endpoint

All API traffic is routed through:

**POST /api/proxy/{service}/{path:path}**

This:
- Validates tenant token  
- Checks for sufficient credits  
- Deducts credits (via Celery task)  
- Logs the call  
- Forwards to actual API and returns result

---

### ➤ Usage Flow

1. **User logs in → Gets JWT**
2. **Calls are made to `/api/proxy/service/path`**
3. System:
   - Verifies endpoint in DB
   - Checks and deducts credits via Celery
   - Logs usage to MongoDB
   - Publishes MQTT alerts if needed

---


## Periodic Tasks

| Task                            | Schedule (via Celery Beat) | Purpose                         |
|---------------------------------|-----------------------------|---------------------------------|
| `generate_scheduled_summary_task` | Every 5 minutes             | Create usage summary entries    |

---

## MQTT Topics

| Topic Format                            | Triggered When                  |
|-----------------------------------------|----------------------------------|
| `tenant/{tenant_id}/warning`           | Credits drop ≤ 100 or exhausted |
| `tenant/{tenant_id}/credit-success`    | Credits deducted successfully    |

---

## Example Payloads

### ➤ Usage Log Entry

```json
{
  "tenant_id": "abc123",
  "service": "notes",
  "endpoint": "/notes/create",
  "credits_used": 5,
  "timestamp": "2025-07-08T10:54:45Z"
}
➤ Invoice Record
{
  "tenant_id": "abc123",
  "total_credits_used": 100,
  "log_count": 20,
  "logs": [...],
  "generated_at": "2025-07-01T05:00:00Z"
}

Local Development
➤ Run All Components

# Start FastAPI
uvicorn main:app --reload

# Start Celery Worker
celery -A celery_worker worker --loglevel=info --pool=solo

# Start Celery Beat
celery -A celery_worker beat --loglevel=info
```
This project is designed to be plug-and-play for any future APIs, just configure service + endpoint + credits and you're done.