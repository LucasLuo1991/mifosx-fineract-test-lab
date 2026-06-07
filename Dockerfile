FROM mcr.microsoft.com/playwright:v1.60.0-noble

WORKDIR /app

# Copy dependency manifests first so rebuilds can reuse install layers.
COPY ./database-setup/requirements.txt ./database-setup/requirements.txt
COPY ./ui-tests/package*.json ./ui-tests/

# Install Python tooling needed by the database setup tests.
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv && \
    rm -rf /var/lib/apt/lists/*

# Keep Python packages out of the system interpreter.
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN python -m pip install --upgrade pip \
    && pip install -r ./database-setup/requirements.txt

# Install JavaScript test tooling for Playwright and Newman.
RUN npm ci --prefix ./ui-tests
RUN npm install -g newman newman-reporter-htmlextra

# Copy the test workspaces after dependencies are installed.
COPY ./api-tests ./api-tests
COPY ./database-setup ./database-setup
COPY ./ui-tests ./ui-tests

# Keep the test runner container alive for manual or Jenkins-triggered commands.
CMD ["sleep", "infinity"]
