````markdown
# Distributed URL Shortener

A production-oriented URL shortening service built to understand and implement **system design and distributed systems concepts**.

The project is being built incrementally — starting with the core URL-shortening functionality and evolving toward a distributed, horizontally scalable system with **Redis caching, rate limiting, distributed ID generation, load balancing, observability, and fault tolerance**.

---

##  Project Status

**Currently in development**

### Completed

- [x] Dockerized PostgreSQL
- [x] Dockerized Redis
- [x] SQLAlchemy database layer
- [x] URL persistence
- [x] PostgreSQL-generated unique IDs
- [x] Base62 encoding
- [x] URL creation service
- [x] Interactive terminal URL creation

### In Progress / Planned

- [ ] FastAPI REST API
- [ ] URL redirection
- [ ] Redis caching
- [ ] Rate limiting
- [ ] Distributed ID generation
- [ ] Load balancing
- [ ] Horizontal scaling
- [ ] Testing & load testing
- [ ] Observability
- [ ] Production deployment

---

# Architecture

## Current Architecture

The current implementation focuses on the core URL creation pipeline.

```text
                    User
                      |
                      | Long URL
                      v
              +---------------+
              |  URL Service  |
              +-------+-------+
                      |
                      v
                PostgreSQL
                      |
                      | Unique ID
                      v
                  Base62
                      |
                      v
                Short Code
                      |
                      v
                 PostgreSQL
````

### Current Flow

```text
Long URL
   |
   v
URL Service
   |
   v
PostgreSQL
   |
   | Generate unique ID
   v
Base62 Encoding
   |
   v
Short Code
   |
   v
Store URL Mapping
```

---

## Planned Production Architecture

The final system will evolve toward a distributed architecture:

```text
                         Clients
                            |
                            v
                    +---------------+
                    | Load Balancer |
                    +-------+-------+
                            |
             +--------------+--------------+
             |              |              |
             v              v              v
        +---------+    +---------+    +---------+
        | FastAPI |    | FastAPI |    | FastAPI |
        | Node 1  |    | Node 2  |    | Node N  |
        +----+----+    +----+----+    +----+----+
             |              |              |
             +--------------+--------------+
                            |
                  +---------+---------+
                  |                   |
                  v                   v
             +---------+        +-----------+
             |  Redis  |        | PostgreSQL|
             |  Cache  |        | Database  |
             +---------+        +-----------+
```

The application will be horizontally scalable, with Redis handling frequently accessed URLs and PostgreSQL acting as the persistent source of truth.

---

# Core Design

## 1. Unique ID Generation

Every shortened URL requires a unique identifier.

Currently, PostgreSQL generates the ID using a database sequence.

Example:

```text
Request 1 → ID 3
Request 2 → ID 4
Request 3 → ID 5
```

PostgreSQL guarantees that concurrent requests receive different sequence values.

### Current approach

```text
FastAPI
   |
   v
PostgreSQL Sequence
   |
   v
Unique Numeric ID
```

### Future approach

The project will eventually use a **distributed ID generation strategy**, such as a Snowflake-style ID generator, so application instances can generate globally unique IDs without depending on PostgreSQL for every ID.

---

# 2. Base62 Encoding

The numeric ID is converted into a compact Base62 string.

Base62 contains:

```text
0-9  → 10 characters
a-z  → 26 characters
A-Z  → 26 characters

Total → 62 characters
```

Therefore:

```text
62^7 ≈ 3.5 trillion
```

A 7-character Base62 code can represent roughly 3.5 trillion different values.

### Example

```text
Database ID
    |
    v
   1187
    |
    v
Base62 Encoding
    |
    v
   "j9"
```

> Base62 itself does **not** guarantee uniqueness.
> Uniqueness comes from the unique numeric ID that is encoded.

---

# 3. Database

PostgreSQL currently stores the URL mapping.

### `urls`

| Column       | Type        | Description               |
| ------------ | ----------- | ------------------------- |
| `id`         | BIGINT      | Unique numeric identifier |
| `short_code` | VARCHAR(16) | Base62 encoded ID         |
| `long_url`   | TEXT        | Original URL              |
| `created_at` | TIMESTAMP   | Creation timestamp        |
| `expires_at` | TIMESTAMP   | Optional expiration       |

The `short_code` column has a unique constraint as an additional database-level protection against duplicate short codes.

---

# 4. Redis Caching

Redis is already included in the infrastructure, but the caching logic has **not been implemented yet**.

The planned redirect flow is:

```text
GET /{short_code}
        |
        v
      Redis
        |
    +---+---+
    |       |
   HIT     MISS
    |       |
    v       v
Redirect  PostgreSQL
             |
             v
        Store in Redis
             |
             v
          Redirect
```

URL shorteners are expected to be **read-heavy systems**, so caching frequently accessed URLs reduces database load and improves redirect latency.

---

# Current Implementation

The following components are currently implemented:

* [x] Project structure
* [x] Docker Compose setup
* [x] PostgreSQL 17
* [x] Redis 7
* [x] Environment-based configuration
* [x] SQLAlchemy database layer
* [x] URL database model
* [x] PostgreSQL unique ID generation
* [x] Base62 encoding
* [x] URL creation service
* [x] Interactive terminal URL creation
* [x] Persistent URL storage

### Current Example

```text
Enter long URL: https://www.cricbuzz.com/

ID: 5
Short code: 5
Long URL: https://www.cricbuzz.com/
Short URL: http://localhost:8000/5
```

---

# What's Left

## API Layer

* [ ] FastAPI application
* [ ] `POST /api/v1/urls`
* [ ] `GET /{short_code}`
* [ ] Request/response schemas
* [ ] URL validation
* [ ] HTTP error handling

## Redirect System

* [ ] Short-code lookup
* [ ] HTTP redirect
* [ ] Handle invalid short codes
* [ ] Handle expired URLs

## Caching

* [ ] Redis connection layer
* [ ] Cache URL mappings
* [ ] Cache hit/miss handling
* [ ] TTL support
* [ ] Cache invalidation strategy

## Rate Limiting

* [ ] Per-user rate limiting
* [ ] Per-IP rate limiting
* [ ] Redis-backed rate limiter
* [ ] HTTP `429 Too Many Requests`

## Distributed ID Generation

Current:

```text
PostgreSQL Sequence
```

Planned:

```text
Snowflake-style Distributed ID Generator
```

## Scalability

* [ ] Multiple FastAPI instances
* [ ] Load balancer
* [ ] Horizontal scaling
* [ ] Database connection pooling
* [ ] Read replicas
* [ ] Database partitioning/sharding analysis

## Reliability

* [ ] Health checks
* [ ] Retry strategies
* [ ] Graceful shutdown
* [ ] Redis failure handling
* [ ] Database failure handling

## Observability

* [ ] Structured logging
* [ ] Metrics
* [ ] Request latency tracking
* [ ] Cache hit/miss metrics
* [ ] Error monitoring
* [ ] Distributed tracing

## Testing

* [ ] Unit tests
* [ ] Integration tests
* [ ] API tests
* [ ] Concurrent request tests
* [ ] Collision testing
* [ ] Load testing

## Deployment

* [ ] Production Docker configuration
* [ ] CI/CD pipeline
* [ ] Cloud deployment
* [ ] Production PostgreSQL
* [ ] Production Redis
* [ ] Monitoring

---

# Project Structure

```text
url-shortener/
│
├── app/
│   ├── api/
│   │
│   ├── core/
│   │   └── config.py
│   │
│   ├── db/
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   └── init_db.py
│   │
│   ├── models/
│   │   └── url.py
│   │
│   ├── services/
│   │   ├── base62.py
│   │   ├── test_base62.py
│   │   ├── url_service.py
│   │   └── test_url_service.py
│   │
│   └── main.py
│
├── tests/
│
├── .env
├── .gitignore
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# Running Locally

## 1. Clone the repository

```bash
git clone <repository-url>
cd url-shortener
```

## 2. Create virtual environment

```bash
python -m venv .venv
```

### Windows

```powershell
.venv\Scripts\activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Start PostgreSQL and Redis

```bash
docker compose up -d
```

This starts:

```text
PostgreSQL → localhost:5434
Redis      → localhost:6379
```

## 5. Configure environment variables

Create `.env`:

```env
DATABASE_URL=postgresql+psycopg2://urluser:urlpassword@localhost:5434/urlshortener
REDIS_URL=redis://localhost:6379/0
```

> `.env` should never be committed to GitHub.

## 6. Initialize the database

```bash
python -m app.db.init_db
```

## 7. Test Base62

```bash
python -m app.services.test_base62
```

## 8. Test URL creation

```bash
python -m app.services.test_url_service
```

Example:

```text
Enter long URL: https://www.cricbuzz.com/

ID: 5
Short code: 5
Long URL: https://www.cricbuzz.com/
Short URL: http://localhost:8000/5
```

---

# Technology Stack

| Component      | Technology              |
| -------------- | ----------------------- |
| Language       | Python                  |
| API            | FastAPI                 |
| Database       | PostgreSQL 17           |
| ORM            | SQLAlchemy              |
| Cache          | Redis 7                 |
| Infrastructure | Docker / Docker Compose |
| Encoding       | Base62                  |
| Configuration  | Pydantic Settings       |

---

# Learning Goals

This project is being built to gain practical experience with:

* System Design
* Distributed Systems
* URL Shortening
* Database Design
* Unique ID Generation
* Base62 Encoding
* Redis Caching
* Rate Limiting
* Horizontal Scaling
* Load Balancing
* Fault Tolerance
* API Design
* Observability
* Production Backend Engineering

The system is intentionally being built **incrementally**, with each architectural decision implemented and understood before moving to the next layer.

```
