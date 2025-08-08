#!/bin/bash

set -e

function wait_for_health() {
    retries=0
    max_retries=30
    until curl --fail http://localhost:8000/api/v1/collections; do
        sleep 3
        retries=$((retries+1))
        if [ $retries -ge $max_retries ]; then
            echo "Chroma DB failed to start in time."
            exit 1
        fi
        echo "Waiting for Chroma DB to become healthy... ($retries/$max_retries)"
    done
}

echo "Starting vector database via docker-compose..."
docker-compose up -d
wait_for_health
echo "Chroma vector database is healthy."

echo "Running data initialization..."
python3 db/init_vector_db.py

echo "Initialization complete. Ready for chunking/embedding/retrieval implementation!"