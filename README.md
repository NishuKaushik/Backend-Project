# 🔐 Secure File Sharing System

This project is a submission for the **Back-End Intern Test**. It implements a secure file-sharing system between two types of users: **Ops Users** and **Client Users**. It includes role-based authentication, file access restrictions, and encrypted download links.

---

## 👥 User Roles

### 🧑‍💼 Ops User
- Login  
- Upload `.pptx`, `.docx`, `.xlsx` files only

### 👤 Client User
- Sign Up (returns encrypted URL)  
- Email Verification (console-based mock)  
- Login  
- Download file via secure encrypted link  
- List all uploaded files

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
- **Database**: In-memory (can be extended to PostgreSQL/MongoDB)  
- **Authentication**: JWT Tokens  
- **File Storage**: Local file system  
- **Email Service**: Console output  
- **Tools Used**: Postman, Uvicorn, Git  

---

## 📌 API Endpoints

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
Open Swagger UI at:
👉 http://127.0.0.1:8000/docs

Use this interface to test all endpoints manually.

📸 Output Screenshots are in Secure File sharing Screenshots

Ops tries to access client-only route — access denied.

🧪 Testing
Manual testing performed using:

✅ Swagger UI

✅ Postman Collection

Test cases include:

Role-based access (Ops vs Client)

File format restrictions

Secure link-based downloads

🚀 Deployment Plan
The project can be deployed on:

Render

Railway

Docker on AWS EC2 / DigitalOcean / Azure

🔒 For Production:
Replace in-memory DB with PostgreSQL

Configure .env file for secrets

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


