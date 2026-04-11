# FarmLink

> A microservices platform connecting Nigerian smallholder farmers directly to bulk buyers — with transparent pricing, escrow-secured payments, and blockchain-verified transaction receipts.

## The problem

Smallholder farmers in Nigeria (95% of all farmers) sell through middlemen who offer below-market prices because farmers have no price visibility and no payment security. FarmLink removes that dependency.

Confirmed at the BusinessDay Future of Agriculture Conference, March 2026: *"Nigeria does not have a formal structured market for smallholder farmers."* One Acre Fund research confirms: *"Farmers are often forced to sell at the farm gate at prices far below fair market value."*

## How it works

1. A farmer lists produce (crop, quantity, location, asking price)
2. The price intelligence service shows the farmer real market prices before they accept any offer
3. A buyer browses listings and places an order
4. The buyer's payment is locked in escrow — the farmer sees "payment secured" before harvesting
5. On delivery confirmation, funds release to the farmer automatically minus a 1.5% platform fee
6. An immutable receipt is written to the Sui blockchain — verifiable by both parties forever

## Architecture

```
Clients (Mobile / Web / USSD)
        │
Spring Cloud Gateway (JWT auth · rate limiting via Redis · routing)
        │
   ┌────┴──────────────────────────────────────┐
   │              Java services                 │
   │  auth-service    (Spring Boot)             │
   │  order-service   (Spring Boot)             │
   │  escrow-service  (Spring Boot + Resilience4j circuit breaker) │
   └────┬──────────────────────────────────────┘
        │
   Kafka event bus
   (order.confirmed · escrow.held · order.delivered · escrow.released)
        │
   ┌────┴──────────────────────────────────────┐
   │             Python services                │
   │  price-service        (FastAPI + Redis cache)  │
   │  forecast-service     (FastAPI)            │
   │  notification-service (FastAPI · Kafka consumer · SMS via Termii) │
   └────┬──────────────────────────────────────┘
        │
   Sui blockchain (immutable transaction receipts · Sui Move smart contracts)
```

## Tech stack

| Layer | Technology |
|---|---|
| Java services | Java 17, Spring Boot 3, Spring Cloud Gateway, Maven |
| Python services | Python 3.11, FastAPI |
| Messaging | Apache Kafka (event streaming), Outbox pattern |
| Caching | Redis — cache-aside pattern (price data, 24hr TTL) |
| Rate limiting | Redis — token bucket (max 3 OTP requests/phone/hour) |
| Resilience | Resilience4j circuit breaker (escrow → blockchain calls) |
| Databases | PostgreSQL (users, orders, escrow), MongoDB (price snapshots) |
| Blockchain | Sui Move smart contracts, Sui testnet |
| DevOps | Docker, docker-compose, GitHub Actions CI/CD, Terraform |
| Deployment | Fly.io, Supabase, MongoDB Atlas, Upstash (all free tier) |
| Notifications | Termii SMS (Nigerian numbers) |

## Kafka event topics

| Topic | Producer | Consumers |
|---|---|---|
| `order.confirmed` | order-service | escrow-service, notification-service |
| `escrow.held` | escrow-service | notification-service |
| `order.delivered` | order-service | escrow-service, notification-service |
| `escrow.released` | escrow-service | notification-service, blockchain writer |

## Key engineering patterns

- **Event-driven architecture** — services communicate exclusively via Kafka topics, fully decoupled
- **Cache-aside pattern** — price-service checks Redis first; on miss, fetches and caches for 24 hours
- **Circuit breaker** — Resilience4j wraps Sui blockchain calls in escrow-service; fails fast and queues retry if blockchain is slow
- **Outbox pattern** — escrow-service writes Kafka events to a DB table atomically before publishing, guaranteeing no event is ever lost on crash
- **Token bucket rate limiting** — Spring Cloud Gateway enforces OTP request limits per phone number via Redis
- **API Gateway pattern** — single entry point handles JWT validation, routing, and rate limiting before requests reach any service

## Repo structure

```
farmlink/
├── README.md
├── docker-compose.yml          ← run everything locally
├── docker-compose.prod.yml     ← production config
├── .github/
│   └── workflows/
│       └── deploy.yml          ← CI/CD pipeline
├── infra/
│   └── terraform/              ← infrastructure as code
├── services/
│   ├── auth-service/           ← Spring Boot (Java)
│   ├── order-service/          ← Spring Boot (Java)
│   ├── escrow-service/         ← Spring Boot + Resilience4j (Java)
│   ├── price-service/          ← FastAPI + Redis cache (Python)
│   ├── forecast-service/       ← FastAPI (Python)
│   └── notification-service/   ← FastAPI + Kafka consumer (Python)
└── contracts/
    └── farmlink.move           ← Sui Move smart contract
```

## Running locally

### Prerequisites
- Docker Desktop
- Java 17+
- Python 3.11+
- Maven

### Start all services

```bash
git clone https://github.com/YOUR_USERNAME/farmlink.git
cd farmlink
docker-compose up --build
```

Services will be available at:

| Service | URL |
|---|---|
| Spring Cloud Gateway | http://localhost:8080 |
| auth-service | http://localhost:8081 |
| order-service | http://localhost:8082 |
| escrow-service | http://localhost:8083 |
| price-service | http://localhost:8084 |
| forecast-service | http://localhost:8085 |
| notification-service | http://localhost:8086 |
| PostgreSQL | localhost:5432 |
| MongoDB | localhost:27017 |
| Redis | localhost:6379 |
| Kafka | localhost:9092 |

## Infrastructure (zero cost)

| What | Free tool | Replaces |
|---|---|---|
| Compute | Fly.io free tier | AWS EC2 |
| Docker registry | GitHub Container Registry | AWS ECR |
| PostgreSQL | Supabase free tier | AWS RDS |
| MongoDB | MongoDB Atlas free | DocumentDB |
| Redis | Upstash free tier | ElastiCache |
| Kafka | Upstash Kafka free (10k msg/day) | AWS MSK |
| Secrets | GitHub Secrets | AWS SSM |
| CI/CD | GitHub Actions | Already free |

## Business model

FarmLink charges a 1.5% transaction fee on every settled order. No settlement, no fee — incentives are fully aligned with both farmer and buyer success.

## Build status

- [x] Phase 0 — Project scaffolding + DevOps
- [ ] Phase 1 — Java core services (auth, order, escrow)
- [ ] Phase 2 — Python intelligence layer (price, forecast, notification)
- [ ] Phase 3 — Sui blockchain integration
- [ ] Phase 4 — Frontend + production deployment

## Author

Esther Aiyeola — DevOps & Backend Engineer
[LinkedIn](https://www.linkedin.com/in/esther-aiyeola-4a10b5296/) · [GitHub](https://github.com/Estheraiyeola)