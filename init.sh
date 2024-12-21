#!/bin/sh

docker compose exec kafka-0 kafka-topics.sh \
  --create --topic obscene-words --partitions 3 --replication-factor 3 \
  --bootstrap-server localhost:9092 --config min.insync.replicas=2

docker compose exec kafka-0 kafka-topics.sh \
  --create --topic bans --partitions 3 --replication-factor 3 \
  --bootstrap-server localhost:9092 --config min.insync.replicas=2

docker compose exec kafka-0 kafka-topics.sh \
  --create --topic messages-out --partitions 3 --replication-factor 3 \
  --bootstrap-server localhost:9092 --config min.insync.replicas=2
