FROM node:20-slim

WORKDIR /app

# Install git (required for some npm packages)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Install dependencies first (cache layer)
COPY package.json package-lock.json* ./
RUN npm install --omit=dev

# Copy source
COPY src/ ./src/

# Create sessions directory
RUN mkdir -p /app/sessions

# Expose API port
EXPOSE 3001

# Environment
ENV NODE_ENV=production
ENV SESSION_DIR=/app/sessions
ENV WHATSAPP_PORT=3001

# Start
CMD ["npm", "start"]
