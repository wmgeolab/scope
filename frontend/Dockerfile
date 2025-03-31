FROM docker.io/library/node:22.9-slim

WORKDIR /app

# Copy package files first to leverage Docker cache
COPY package*.json ./

# Install dependencies
RUN npm install && \
    npm cache clean --force

# Copy source files after dependencies
COPY src/ ./src/
COPY public/ ./public/
COPY .env* ./

ENV REACT_APP_API_URL=https://backend.scnw.cc

# Build the application
RUN npm run build

# Install serve for production
RUN npm install -g serve && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean && \
    npm cache clean --force

# Set production environment variables
ENV NODE_ENV=production
ENV GENERATE_SOURCEMAP=false
ENV REACT_APP_API_URL=https://backend.scnw.cc

# Expose the port
EXPOSE 3000

# Run the server
CMD ["serve", "-s", "build", "-l", "3000"]
