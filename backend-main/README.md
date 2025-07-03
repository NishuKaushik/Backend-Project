
# Secure File Sharing System

## Features
- Role-based (Ops/Client) authentication using JWT
- Email verification for client sign-up
- Ops-only file upload (.docx, .pptx, .xlsx)
- Clients can list/download files using encrypted links
- FastAPI + in-memory DB (can be extended to PostgreSQL/MongoDB)

## Running
```bash
uvicorn main:app --reload
```

Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to test the APIs.

## Deployment
- Use Docker or any cloud server (Render, Railway, EC2)
- Replace in-memory DB with PostgreSQL for persistence
