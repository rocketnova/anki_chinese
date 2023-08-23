FROM python:slim

# Update os packages
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    cron

# Create a non-root user called 'pipx'
# The pipx binaries will be installed to `/home/pipx/.local/bin`
RUN groupadd -r pipx && useradd -m --no-log-init -r -g pipx pipx
USER pipx

# Install pipx
RUN python3 -m pip install --user pipx \
  && python3 -m pipx ensurepath

# Install poetry
RUN /home/pipx/.local/bin/pipx install poetry

# Set workingc directory
WORKDIR /srv/application

# Install project files
COPY ./pyproject.toml .
COPY ./anki_chinese anki_chinese
RUN /home/pipx/.local/bin/poetry install

USER root

CMD ["cron", "-f"]
