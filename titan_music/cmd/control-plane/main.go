package main

import (
	"encoding/json"
	"log"
	"net/http"
	"os"
	"time"
)

type Health struct {
	OK bool `json:"ok"`
}

func main() {
	port := env("CONTROL_PLANE_PORT", "9000")
	sidecarURL := env("SIDE_CAR_URL", "http://127.0.0.1:9001")

	mux := http.NewServeMux()
	mux.HandleFunc("/healthz", func(w http.ResponseWriter, r *http.Request) {
		writeJSON(w, Health{OK: true})
	})
	mux.HandleFunc("/readyz", func(w http.ResponseWriter, r *http.Request) {
		client := &http.Client{Timeout: 2 * time.Second}
		resp, err := client.Get(sidecarURL + "/healthz")
		if err != nil || resp.StatusCode >= 300 {
			http.Error(w, "not ready", http.StatusServiceUnavailable)
			return
		}
		writeJSON(w, Health{OK: true})
	})

	srv := &http.Server{
		Addr:              ":" + port,
		Handler:           mux,
		ReadHeaderTimeout: 5 * time.Second,
	}

	log.Fatal(srv.ListenAndServe())
}

func env(k, d string) string {
	v := os.Getenv(k)
	if v == "" {
		return d
	}
	return v
}

func writeJSON(w http.ResponseWriter, v any) {
	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(v)
}
