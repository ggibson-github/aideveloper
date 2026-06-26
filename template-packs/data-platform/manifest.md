# Integration manifest (data platform pack)

## Environments

- dev, staging, prod — separate buckets/databases

## Data contracts

- Schema registry path; Avro/JSON contract ids

## Naming

- Tables: `domain.entity`; topics: `domain.event.v1`

## Definition of done

- Pipeline task: pytest or `dbt test` log in evidence
- Contract change: downstream nodes marked stale in artifact graph
