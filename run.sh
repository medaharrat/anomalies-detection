#!/bin/bash
echo '[>] Exporting variables'
export INFLUXDB_DB=swat
export INFLUXDB_HOST=http://influxdb:8086
export AUTH_TOKEN=iJHZR-dq4I5LIpFZCc5bTUHx-I7dyz29ZTO-B4W5DpU4mhPVDFg-aAb2jK4Vz1C6n0DDb6ddA-bJ3EZAanAOUw==
export DEFAULT_BUCKET=swat
export MONITORING_BUCKET=primary
export DEFAULT_ORGANIZATION=primary
export ADMIN_USERNAME=admin
export ADMIN_PASSWORD=admin123

echo '[>] Creating influxdb directory'
mkdir -p influxdb

echo '[>] Creating grafana directory'
mkdir -p grafana

echo '[>] Running docker compose'
docker-compose up  --remove-orphans