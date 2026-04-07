# First stage: Generate static page
FROM ubuntu:24.04 AS builder

WORKDIR /build
COPY generate-page .
RUN chmod +x generate-page && ./generate-page > index.html

# Second stage: production ngninx (unprivileged)
FROM nginxinc/nginx-unprivileged:1.28

# # Labels: link a package to registry
# LABEL org.opencontainer.image.source="http://github.com/fabriciojm/status-page"
# LABEL org.opencontainer.image.version="1.0.0"

# Copy generated html
COPY --from=builder /build/index.html /usr/share/nginx/html/index.html

# Document port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 CMD curl -f http://localhost:8080/ || exit 1
