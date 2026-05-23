# Bogatti Admin Panel Architecture

This document outlines the architecture and implementation details for the Bogatti Web Admin Panel.

## Tech Stack
- **Frontend:** Next.js 14+ (App Router)
- **Styling:** Tailwind CSS + Shadcn UI (Spotify Dark Theme)
- **Authentication:** NextAuth.js
- **Database:** PostgreSQL (via Prisma ORM)
- **State Management:** TanStack Query (React Query)

## Modules

### 1. Dashboard Overview
- Real-time usage charts (Queries per hour/day).
- Active server status.
- Top active users.

### 2. Dynamic Config Controller
- Interface to edit `config.json` remotely.
- Update `toman_per_usd` conversion rates.
- Modify UI strings (Persian/English).

### 3. Model & Key Management
- Add/Remove AI models (GPT-4, Gemini, Claude).
- Rotate API keys.
- Set per-model pricing.

### 4. User & Safety Management
- View user query logs.
- Block IPs or phone numbers.
- Monitor credit balances.

## Database Schema (SQL)

```sql
-- Users Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    phone_number VARCHAR(15) UNIQUE NOT NULL,
    balance_usd DECIMAL(10, 2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_blocked BOOLEAN DEFAULT FALSE
);

-- AI Models Table
CREATE TABLE ai_models (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    provider VARCHAR(50) NOT NULL,
    api_key_env_var VARCHAR(100),
    cost_per_request DECIMAL(10, 5) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE
);

-- Configuration Table (Single Row)
CREATE TABLE app_config (
    id SERIAL PRIMARY KEY,
    json_data JSONB NOT NULL, -- Stores UI strings and rates
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Query Logs Table
CREATE TABLE query_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    model_id INTEGER REFERENCES ai_models(id),
    prompt TEXT,
    response TEXT,
    cost DECIMAL(10, 5),
    latency_ms INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Backend API Integration
The Next.js backend (API Routes) will communicate directly with the PostgreSQL database and provide the JSON endpoint that the Android app's `ModularConfigManager` consumes.
