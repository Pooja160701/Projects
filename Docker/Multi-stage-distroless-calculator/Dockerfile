###########################################
# BUILD STAGE
###########################################

FROM ubuntu AS build

# Install Go (or use golang image if you prefer)
RUN apt-get update && apt-get install -y golang-go ca-certificates && rm -rf /var/lib/apt/lists/*

WORKDIR /src

# If you want reproducible builds, set GO111MODULE=on and use modules
ENV CGO_ENABLED=0
ENV GO111MODULE=off

COPY . .

# Build a static binary
RUN go build -o /app .

############################################
# FINAL STAGE - DISTROLESS
############################################

FROM scratch

# Copy CA certs (optional, only if binary needs TLS). If not needed, remove CA certs lines.
COPY --from=build /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

# Copy the compiled binary from the build stage
COPY --from=build /app /app

# Make the binary executable and run
ENTRYPOINT ["/app"]