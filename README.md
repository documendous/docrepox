# DocrepoX

DocrepoX is an open-source (LGPL-v3) Enterprise Content Management (ECM) and Digital Asset Management (DAM) platform designed to store, organise, and retrieve digital assets and documents. Its versatility makes it valuable for businesses of all sizes and even handy for personal use.

## Project Objectives

- **Scalability**: Designed to serve organisations from small teams to large enterprises.

- **Integration**: Built with the aim of seamless integration with third-party applications.

- **Security**: Developed with stringent security standards to inspire confidence in its use.

---

## Getting Started

### Assumptions

- You are using Linux or macOS. Windows is probably ok to use but these instructions assume you will be using Docker which runs a bit differently on Windows. You will have to consult https://docs.docker.com/desktop/setup/install/windows-install/ to see if this will be possible for you.
- Docker is installed and operational on your system, and you are familiar with its basics, including images, containers, volumes, and networks.

### Simple Install

This will install and give you a running DocrepoX system:

Just run from the directory where you would like to install DocrepoX (if needed, change localhost to your hostname of choice):

```
curl -s https://raw.githubusercontent.com/documendous/docrepox/main/setup.sh | bash -s -- localhost
```

After running, you can click control-c.

To run again from here on out while persisting your data, you can continue to run:

```
docker compose -f docker-compose.prod.yml up
```

### Setup Instructions For Development Purposes

1. **Clone the Repository**:
   ```
   git clone https://github.com/documendous/docrepox.git
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
   cp env.dev.example .env.dev
   cp .env.dev docrepo/.env
   ```
   If you're interested in trying out a production-ready setup, have a look at the "Using in production" section below.

6. Create the mediafiles folder in docrepo:

   ```
   mkdir docrepo/mediafiles
   ```

6. **Run Docker Compose**:
   ```
   docker compose up --build
   ```

7. **Verify Logs**:
   Check the logs for any errors. If all goes well, your system should be up and running. See the troubleshooting section below if you have any issues.

### Troubleshooting

#### DisallowedHost at /

You may see an error like this at startup:

<pre>
DisallowedHost at /
Invalid HTTP_HOST header: '172.215.42.20:8000'. You may need to add '172.215.42.20' to ALLOWED_HOSTS.
</pre>

You will need to add the hostname (or ip address) to your .env file:

```
...
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,[::1],172.215.42.20
...
```

and then restart.

#### Docker: "network not found" on docker compose up --build

This can happen if you run `docker system prune -af`.

Consult docker docs on this but generally you can rebuild with this command:

```
docker compose up --remove-orphans --build --force-recreate
```

#### "/mediafiles": Not Found Error

If you encounter the following error during your first run of `docker compose up --build`:

<pre>
=> CACHED [web 15/20] COPY apps ./apps                                                             0.0s
=> CACHED [web 16/20] COPY config ./config                                                         0.0s
=> ERROR [web 17/20] COPY mediafiles ./mediafiles                                                  0.0s
------
[+] Running 0/1COPY mediafiles ./mediafiles:
⠧ Service web  Building                                                                            0.7s 
failed to solve: failed to compute cache key: failed to calculate checksum of ref 
d69779c3-e474-4919-97ec-64ea6039f742::fkc6ck6sib0h6wj2wbdnqq50m: "/mediafiles": not found
</pre>

**Solution:**  

Simply create a folder named `mediafiles` within the `docrepo` directory:

```bash
mkdir docrepo/mediafiles
```

After that, run the following command again:

```bash
docker compose up --build
```

This should resolve the issue and allow the build process to complete successfully.

### Logging in & Using DocrepoX

After DocrepoX successfully starts up, log in at http://localhost:8000 and use admin/admin (username/password).

By default in the dev environment there are a number of test users and test projects. 

The admin user should have access at the Django admin console: http://localhost:8000/admin/

There is documentation on how to use the system: http://localhost:8000/ddocs/

### Using in Production

For a production-ready deployment, uses the `docker-compose.prod.yml` configuration, which includes Nginx.

You will need to build the expected .env.prod and .env.prod.db files:

```
cp env.prod.example .env.prod
cp env.prod.db.example .env.prod.db
```

Edit both files to ensure the settings are correct (you will need to remove the dev settings and ensure db server settings are in .env.prod.db only).

Typically this is what .env.prod looks like as a default (it should be enough to get you up and running):

```
DEBUG=0
SECRET_KEY=a_much_better_secret_this_time_change_this
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,[::1]
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=docrepo
SQL_USER=admin
SQL_PASSWORD=admin
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
ROOT_LOG_LEVEL=INFO
```

and env.prod.db:

```
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
POSTGRES_DB=docrepo
```

Obviously--it should go without saying, change any password and secret keys.

After this:

```
cp .env.prod docrepo/.env.prod
```

Instead of the standard Docker command, execute the following:

```bash
docker compose -f docker-compose.prod.yml up --build
```

**Important Note:**

This project is still in its early stages. Exercise caution and sound judgment when evaluating its suitability for production use, particularly regarding stability, security, and overall reliability.

---

### Upgrading

Upgrading is simple if you installed via this github repo.

Stop DocrepoX:

```bash
docker compose stop -f docker-compose.prod.yml 
```

Get newest version of DocrepoX:

```bash
git branch

# if not on main do:
git checkout main
git pull
```

Update package changes:

```bash
source .venv/bin/activate
poetry export --with dev -f requirements.txt --output requirements.txt
cp requirements.txt docrepo/requirements.txt
```

Start up DocrepoX:

```bash
docker compose -f docker-compose.prod.yml up --build
```

Ensure the build and startup complete successfully. Log into DocrepoX. The correct version will show on the footer of the dashboard.

Afterwards, you can stop the containers and run in daemon mode:

```bash
docker compose -f docker-compose.prod.yml up -d
```

**Note:** You may need to recreate the static volume in some cases especially if some css files are not being picked up.

```bash
docker container rm docrepox-web-1
docker container rm docrepox-nginx-1
docker volume rm docrepox_prod_static_volume
```

**Note:** do not remove the media volume or the database volume if these are not backed up and you understand how to restore them.

---