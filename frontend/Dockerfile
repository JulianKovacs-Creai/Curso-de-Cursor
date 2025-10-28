# Multi-stage Dockerfile for E-commerce Frontend
# Node.js 18 with pnpm, nginx, and security optimizations

# =============================================================================
# Stage 1: Base Image with Node.js
# =============================================================================
FROM node:18-alpine as base

# Set environment variables
ENV NODE_ENV=production \
    PNPM_HOME="/pnpm" \
    PATH="$PNPM_HOME:$PATH"

# Install pnpm
RUN corepack enable pnpm

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S -D -H -u 1001 -h /app -s /sbin/nologin -G nodejs nodejs

# =============================================================================
# Stage 2: Dependencies Installation
# =============================================================================
FROM base as deps

# Set working directory
WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm install

# =============================================================================
# Stage 3: Build Stage
# =============================================================================
FROM base as builder

# Set working directory
WORKDIR /app

# Copy dependencies from deps stage
COPY --from=deps /app/node_modules ./node_modules
COPY --from=deps /app/package.json ./package.json
COPY --from=deps /app/package-lock.json ./package-lock.json

# Copy source code
COPY . .

# Build the application
RUN npm run build

# =============================================================================
# Stage 4: Production Image with Nginx
# =============================================================================
FROM nginx:1.25-alpine as production

# Install security updates
RUN apk update && apk upgrade && \
    apk add --no-cache curl && \
    rm -rf /var/cache/apk/*

# Create non-root user for nginx
RUN addgroup -g 1001 -S nginx && \
    adduser -S -D -H -u 1001 -h /var/cache/nginx -s /sbin/nologin -G nginx nginx

# Copy built application from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Create necessary directories
RUN mkdir -p /var/cache/nginx /var/log/nginx /var/run/nginx && \
    chown -R nginx:nginx /var/cache/nginx /var/log/nginx /var/run/nginx /usr/share/nginx/html

# Set proper permissions
RUN chmod -R 755 /usr/share/nginx/html && \
    chmod 644 /etc/nginx/nginx.conf

# Switch to non-root user
USER nginx

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]

# =============================================================================
# Stage 5: Development Image
# =============================================================================
FROM base as development

# Set environment variables
ENV NODE_ENV=development

# Set working directory
WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install all dependencies (including dev dependencies)
RUN npm install

# Copy source code
COPY . .

# Change ownership to non-root user
RUN chown -R nodejs:nodejs /app

# Switch to non-root user
USER nodejs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1

# Development command
CMD ["npm", "run", "dev"]

# =============================================================================
# Stage 6: Testing Image
# =============================================================================
FROM development as testing

# Install testing dependencies
RUN npm install

# Copy test files
COPY tests/ /app/tests/
COPY __tests__/ /app/__tests__/

# Run tests
CMD ["npm", "run", "test"]
