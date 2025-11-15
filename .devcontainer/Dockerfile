FROM python:latest

# install pre-commit
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt --no-cache-dir

# Install Terraform
RUN apt-get update && apt-get install -y gnupg lsb-release curl && \
    curl -fsSL https://apt.releases.hashicorp.com/gpg | gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/hashicorp.list && \
    apt-get update && apt-get install -y terraform

WORKDIR /app
