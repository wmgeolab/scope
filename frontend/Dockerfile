FROM docker.io/library/node:22.9-slim AS build

WORKDIR /app

# Install only necessary dependencies
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

# Copy only necessary source files for building
COPY src/ ./src/
COPY public/ ./public/
COPY .env* ./

# Build the application with optimizations
RUN npm run build

# Create a smaller production image
FROM docker.io/library/node:22.9-slim AS production

WORKDIR /app

# Copy only the built application files
COPY --from=build /app/build ./build

# Install only the serve package
RUN npm install -g serve && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean && \
    npm cache clean --force

# Set production environment variables
ENV NODE_ENV=production
ENV GENERATE_SOURCEMAP=false

# Expose the port
EXPOSE 3000

# Run the server with minimal footprint
CMD ["serve", "-s", "build", "-l", "3000"]
