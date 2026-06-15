FROM golang:1.24-alpine AS build
WORKDIR /src
COPY . .
RUN mkdir -p /out && CGO_ENABLED=0 GOOS=linux go build -o /out/control-plane ./cmd/control-plane

FROM gcr.io/distroless/static:nonroot
WORKDIR /
COPY --from=build /out/control-plane /control-plane
EXPOSE 9000
USER nonroot:nonroot
ENTRYPOINT ["/control-plane"]
