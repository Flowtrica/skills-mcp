FROM python:3.12-slim

# Install git (needed to clone skill repos)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --no-cache-dir uv

# Copy the skills-mcp code
COPY . /app
WORKDIR /app

# Install skills-mcp
RUN uv pip install --system -e .

# Default entrypoint
ENTRYPOINT ["skills-mcp"]
CMD ["--help"]
