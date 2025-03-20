# LLM Research Tracker  

📌 **A web-based research tool for AI researchers to track, explore, and stay updated on the latest machine learning publications.**  

## 🚀 Overview  
AI Research Tracker is an intelligent and scalable research discovery tool designed to help researchers:  
- **Understand** the LLM research landscape.  
- **Find** relevant papers based on topics search.  
- **Stay updated** with  notifications on emerging publications on a weekly basis. 

The system continuously monitors new research, providing users with structured insights based on their interests.  

---

## ⚙️ Tech Stack  
- **Backend:** FastAPI (API)  
- **Database:** Weaviate (Vector Database)  
- **Frontend:** React (soon in progress)
- **Hosting:** AWS 

---

## 📂 Project Structure  
### 🔧 **Core Directories**  
- **`.github/workflows/`** – Contains CI/CD pipeline configurations for automated testing and deployment (e.g., `ci_cd_pipeline.yml`).  
- **`api/`** – Backend API logic, likely built using FastAPI or Django.  
- **`bin/`** – Executable scripts or command-line utilities.  
- **`data/`** – Stores datasets or processed research information.  
- **`models/`** – Machine learning models or database schema representations.  
- **`services/`** – Business logic handling, API interactions, or microservices.  
- **`tests/`** – Unit and integration tests to ensure system reliability.  

### 📝 **Configuration Files**  
- **`.env`** – Environment variables for API keys, database credentials, etc. (should be excluded from version control).  
- **`.gitignore`** – Specifies files to exclude from Git tracking (recently modified to remove a large file).  
- **`LICENSE`** – MIT License file for open-source contributions.  
- **`README.md`** – Project documentation with setup and usage details.  

### ⚙️ **System & Execution Files**  
- **`__init__.py`** – Marks directories as Python packages.  
- **`docker-compose.yml`** – Defines multi-container Docker setup for deployment.  
- **`main.py`** – Main entry point for the backend application (FastAPI or Django).  

