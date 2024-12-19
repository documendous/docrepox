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
   git clone git@github.com:documendous/docrepox.git
   cd docrepox
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
   Check the logs for any errors. If all goes well, your system should be up and running. See the troubleshooting section below if you have any issues.

### Troubleshooting

#### "/mediafiles": not found

You may encounter this error the first time you run `docker compose up --build`:

<pre>
=> CACHED [web 15/20] COPY apps ./apps                                                              0.0s
=> CACHED [web 16/20] COPY config ./config                                                          0.0s
=> ERROR [web 17/20] COPY mediafiles ./mediafiles                                                   0.0s
------
[+] Running 0/1COPY mediafiles ./mediafiles:
⠧ Service web  Building                                                                             0.7s 
failed to solve: failed to compute cache key: failed to calculate checksum of ref 
d69779c3-e474-4919-97ec-64ea6039f742::fkc6ck6sib0h6wj2wbdnqq50m: "/mediafiles": not found
</pre>

Just create a folder called `mediafiles` in the docrepo folder:

```
mkdir docrepo/mediafiles
```

and then run `docker compose up --build` again.

---

