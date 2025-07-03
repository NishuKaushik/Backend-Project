# 🔐 Secure File Sharing System

This project is a submission for the Back-End Intern Test. It implements a secure file-sharing system between two types of users: **Ops Users** and **Client Users**. It includes role-based authentication, file access restrictions, and encrypted download links.

---

## 👥 User Roles

### 🧑‍💼 Ops User
- ✅ Login
- ✅ Upload `.pptx`, `.docx`, `.xlsx` files only

### 👤 Client User
- ✅ Sign Up (returns encrypted URL)
- ✅ Email Verification (console-based mock)
- ✅ Login
- ✅ Download file via secure encrypted link
- ✅ List all uploaded files

---

## 🚀 Features

- Role-based access using JWT
- File type validation for upload (Ops only)
- Secure, encrypted links for file download
- Token-protected APIs using FastAPI
- Email verification (mock implementation)
- Full API documentation via Swagger UI

---

## 🛠 Tech Stack

- **Framework**: FastAPI (Python)
- **Database**: In-memory (can extend to PostgreSQL/MongoDB)
- **Authentication**: JWT Tokens
- **File Storage**: Local file system
- **Email Service**: Console output
- **Tools Used**: Postman, Uvicorn, Git

---

## 🔁 API Endpoints

| Method | Endpoint                         | Description                         |
|--------|----------------------------------|-------------------------------------|
| POST   | `/ops/login/`                    | Ops user login                      |
| POST   | `/ops/upload/`                   | Upload a file (restricted types)    |
| POST   | `/client/signup/`                | Signup new client (returns link)    |
| GET    | `/client/verify-email/`          | Simulated email verification        |
| POST   | `/client/login/`                 | Client user login                   |
| GET    | `/download-file/{file_id}/`      | Secure file download for clients    |
| GET    | `/files/`                        | List all uploaded files             |

---

## ▶️ Running the Server Locally

```bash
uvicorn main:app --reload
Then open Swagger UI at:

👉 http://127.0.0.1:8000/docs

Use this interface to test all endpoints manually.

📸 Output 
✅ 1. Ops Login page
 The Ops user logs in using valid credentials. JWT token is returned for authorization in future requests.
![Screenshot 2025-07-03 112548](https://github.com/user-attachments/assets/4d240d52-933b-4413-b403-baad83352b97)


 

✅ 2. File Upload by Ops

✅ 3. Client Signup with Encrypted URL

✅ 4. Email Verification

✅ 5. Client Login

✅ 6. Secure File Download

✅ 7. List Uploaded Files

✅ 8. Unauthorized Access Attempt (Bonus)

🧪 Testing
Manual testing performed using:

✅ Swagger UI

✅ Postman Collection

## Test cases cover:

Role-based access (Ops vs Client)

File format restrictions

Secure link-based downloads

🧳 Deployment Plan
This project can be deployed on:

🔹 Render

🔹 Railway

🔹 Docker on AWS EC2 / DigitalOcean / Azure

🔐 For production:
Replace in-memory DB with PostgreSQL

Configure .env for secrets

Use Gunicorn + Nginx for serving FastAPI app

📬 Postman Collection
Included: postman_collection.json

You can import this into Postman to test all APIs with sample payloads and tokens.

📎 Repository
🔗 GitHub: https://github.com/NishuKaushik/Backend-Project

👤 Author
Nishu Kaushik
📧 nishukaushik166@gmail.com
🔗 GitHub Profile

---
