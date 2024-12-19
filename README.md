# DocrepoX

DocrepoX is an open-source (LGPL-v3) Enterprise Content Management (ECM) and Digital Asset Management (DAM) platform designed to store, organise, and retrieve digital assets and documents. Its versatility makes it valuable for businesses of all sizes and even handy for personal use.

## Project Objectives

- **Scalability**: Designed to serve organisations from small teams to large enterprises.

- **Integration**: Built with the aim of seamless integration with third-party applications.

- **Security**: Developed with stringent security standards to inspire confidence in its use.

---

## Getting Started

### Assumptions

- You are using Linux or macOS.
- Docker is installed and operational on your system, and you are familiar with its basics, including images, containers, volumes, and networks.

### Setup Instructions

1. **Clone the Repository**:
   ```
   git clone <repository_url>
   cd <repository_directory>
   ```
   Alternatively, download and extract the repository’s zip file.

2. **Create a Virtual Environment** (Python 3.10 or newer):
   ```
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Packages**:
   ```
   pip install poetry
   poetry install
   ```

4. **Generate Requirements File**:
   ```
   poetry export --with dev -f requirements.txt --output requirements.txt
   cp requirements.txt docrepo/requirements.txt
   ```

5. **Configure Environment Variables**:
   ```
   cp env.example .env.dev
   cp env.example docrepo/.env
   ```

6. **Run Docker Compose**:
   ```
   docker compose up --build
   ```

7. **Verify Logs**:
   Check the logs for any errors. If all goes well, your system should be up and running.

---

