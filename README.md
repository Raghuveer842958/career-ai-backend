# 🚀 CareerAI Backend

> AI-Powered Career Development Backend built with FastAPI, MongoDB, LangChain, LangGraph, and Large Language Models.

CareerAI Backend powers the complete CareerAI platform by providing authentication, resume analysis, job recommendations, AI interview sessions, interview history management, and intelligent career assistance through modern AI workflows.

---

# ✨ Features

## 🔐 Authentication & Security

* User Registration
* User Login
* JWT Authentication
* Protected Endpoints
* Secure Password Hashing
* Role-Based Authorization Ready

---

## 📄 Resume Intelligence

AI-powered resume analysis including:

* Resume Strength Detection
* Weakness Analysis
* Resume Improvement Suggestions
* Project Evaluation
* Resume Chat Assistant
* Career Guidance Recommendations

---

## 💼 Job Intelligence

* Job Search APIs
* Job Details APIs
* Personalized Job Recommendations
* AI-Powered Matching Logic
* Saved Jobs Support (Upcoming)

---

## 🎤 AI Mock Interviews

* Interview Session Creation
* Dynamic Question Generation
* AI Interview Evaluation
* Feedback Generation
* Score Calculation
* Interview Transcript Management

---

## 📊 Interview History

* Previous Interview Retrieval
* Performance Tracking
* Detailed Feedback Storage
* Historical Score Analysis

---

## 🤖 AI & LLM Integration

CareerAI leverages modern AI frameworks to build intelligent workflows.

### AI Capabilities

* Resume Analysis
* Resume Chat Assistant
* Interview Evaluation
* Career Recommendations
* Job Matching
* Resume Optimization (In Progress)

---

# 🛠️ Tech Stack

## Backend Framework

* FastAPI
* Python 3.x

## Database

* MongoDB
* Motor (Async MongoDB Driver)

## Authentication

* JWT Authentication
* Password Hashing

## AI Frameworks

* LangChain
* LangGraph

## LLM Providers

* OpenAI
* Ollama

## API Architecture

* REST APIs
* Async Endpoints
* Dependency Injection

---

# 🏗️ Backend Architecture

```text
backend/
│
├── app/
│
├── routes/
│   ├── auth_routes.py
│   ├── resume_routes.py
│   ├── jobs_routes.py
│   ├── interview_routes.py
│   └── history_routes.py
│
├── controllers/
│
├── services/
│   ├── ai/
│   ├── jobs/
│   ├── interviews/
│   └── resume/
│
├── database/
│   ├── mongodb.py
│   └── collections.py
│
├── middleware/
│   └── auth.py
│
├── schemas/
│
├── models/
│
├── agents/
│   ├── resume_agent.py
│   ├── interview_agent.py
│   └── career_agent.py
│
├── langgraph/
│
├── utils/
│
├── config/
│
└── main.py
```

> Folder names may vary depending on implementation.

---

# 🤖 AI Workflow Overview

```text
User Request
      │
      ▼
 FastAPI Endpoint
      │
      ▼
 Business Service Layer
      │
      ▼
 LangChain
      │
      ▼
 LangGraph Workflow
      │
      ▼
 OpenAI / Ollama
      │
      ▼
 Structured Response
      │
      ▼
 Frontend
```

---

# 🔄 System Design

## Resume Analysis Flow

```text
Resume Upload
      │
      ▼
 Resume Parser
      │
      ▼
 AI Analysis Agent
      │
      ▼
 Strengths
 Weaknesses
 Suggestions
 Projects Review
```

---

## Interview Flow

```text
Interview Setup
      │
      ▼
 AI Question Generator
      │
      ▼
 User Response
      │
      ▼
 Evaluation Agent
      │
      ▼
 Score + Feedback
      │
      ▼
 History Storage
```

---

# 🗄️ Database

MongoDB is used for storing:

* Users
* Resumes
* Interview Sessions
* Interview History
* Job Bookmarks
* AI Responses
* Analytics Data

---

# ⚡ Performance Features

* Async FastAPI Endpoints
* Async MongoDB Operations
* Modular Service Architecture
* Reusable AI Components
* Scalable Agent-Based Design
* Separation of Concerns

---

# ⚙️ Installation

Clone the repository:

```bash
git clone <repository-url>
```

Navigate into the project:

```bash
cd careerai-backend
```

Create virtual environment:

```bash
python -m venv venv
```

Activate virtual environment:

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the server:

```bash
uvicorn main:app --reload
```

---

# 🌐 Environment Variables

Create a `.env` file.

```env
MONGODB_URI=

DATABASE_NAME=

JWT_SECRET=

JWT_ALGORITHM=HS256

OPENAI_API_KEY=

OLLAMA_BASE_URL=
```

---

# 📚 API Documentation

FastAPI automatically generates API documentation.

### Swagger UI

```text
http://localhost:8000/docs
```

### ReDoc

```text
http://localhost:8000/redoc
```

---

# 🔮 Upcoming Features

* Resume Optimizer
* Saved Jobs
* Job Application Tracking
* AI Cover Letter Generator
* ATS Score Analyzer
* Resume Version Management
* Dashboard Analytics
* Multi-Agent Career Coach

---

# 🧪 Testing

Run tests:

```bash
pytest
```

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push changes
5. Open a Pull Request

---

# 👨‍💻 Author

**Raghuveer Chauhan**

Full Stack Developer | AI Application Developer

Specializing in:

* FastAPI
* MongoDB
* LangChain
* LangGraph
* AI Agents
* Full Stack Development

---

# ⭐ Support

If you found this project helpful, please consider giving the repository a star.

⭐ Your support helps improve and maintain CareerAI.
