# Wave Payment System - Architecture Overview

## System Architecture Flow

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐    ┌──────────────────┐
│   Frontend      │    │     Flask        │    │    GraphQL      │    │    Services      │
│  (HTML/JS/CSS)  │───▶│   Web Server     │───▶│   API Layer     │───▶│   (Business      │
│                 │    │   (app.py)       │    │  (schema.py)    │    │    Logic)        │
└─────────────────┘    └──────────────────┘    └─────────────────┘    └──────────────────┘
                                                         │                        │
                                                         ▼                        ▼
                                                ┌─────────────────┐    ┌──────────────────┐
                                                │   GraphQL       │    │    Database      │
                                                │  Mutations &    │    │   Access Layer   │
                                                │   Queries       │    │  (database.py)   │
                                                └─────────────────┘    └──────────────────┘
                                                                                  │
                                                                                  ▼
                                                                       ┌──────────────────┐
                                                                       │   PostgreSQL     │
                                                                       │   Database       │
                                                                       │  (models.py)     │
                                                                       └──────────────────┘
```

## GraphQL's Role in the System

**GraphQL acts as the API Contract Layer** between your frontend and backend:

1. **Single Endpoint**: `/graphql` handles all API requests
2. **Type Safety**: Defines strict schema for User and Transaction types
3. **Query Language**: Allows frontend to request exactly what data it needs
4. **Mutation Interface**: Handles all data modifications (create user, transactions, etc.)

## Data Flow Example - Making a Payment

```
1. Frontend (payment.js) → 2. Flask Route (/graphql) → 3. GraphQL Schema → 4. Transaction Manager → 5. Database Layer → 6. PostgreSQL

User clicks "Send Money" ──→ POST to /graphql ──→ requestTransaction mutation ──→ validate & execute ──→ update balances ──→ commit to DB
```

## Class Responsibilities Matrix

| Layer | Component | Primary Responsibility | Called By | Calls |
|-------|-----------|----------------------|-----------|-------|
| **Frontend** | HTML/JS/CSS | User interface, form handling | User | Flask routes |
| **Web Server** | `app.py` | HTTP routing, template rendering | Frontend | GraphQL schema |
| **API** | `schema.py` | GraphQL operations, type definitions | Flask | Services |
| **Business Logic** | `user_manager.py` | User operations, validation | GraphQL | Database layer |
| **Business Logic** | `transaction_manager.py` | Payment processing, business rules | GraphQL | Database layer |
| **Business Logic** | `auth.py` | Authentication logic | GraphQL | Database layer |
| **Business Logic** | `graphql_translator.py` | GraphQL query building | Flask routes | GraphQL schema |
| **Data Access** | `database.py` | SQL operations, session management | Services | SQLAlchemy |
| **Data Models** | `models.py` | Database schema, ORM definitions | Database layer | PostgreSQL |

## Key Architectural Patterns

### 1. **Layered Architecture**
- **Presentation** → **API** → **Business Logic** → **Data Access** → **Database**

### 2. **GraphQL as API Gateway**
```python
# GraphQL handles all API requests through mutations and queries
class Mutation(graphene.ObjectType):
    add_user = AddUser.Field()           # User creation
    request_transaction = RequestTransaction.Field()  # Payments
    attempt_login = AttemptLogin.Field()  # Authentication
```

### 3. **Service Layer Pattern**
- Services contain business logic
- Services are called by GraphQL resolvers
- Services call database layer for persistence

### 4. **Session Management**
```python
# GraphQL schema manages database sessions
context = {'session': session}
result = schema.execute(mutation, context_value=context)
```

## Why GraphQL Was Chosen

1. **Type Safety**: Schema defines exact data structure
2. **Single Endpoint**: No need for multiple REST endpoints
3. **Flexible Queries**: Frontend can request specific fields
4. **Real-time**: Built-in subscription support (if needed later)
5. **Introspection**: Self-documenting API

## Flow Summary

**Frontend** sends queries/mutations to **Flask** → **Flask** routes to **GraphQL** → **GraphQL** validates and calls **Services** → **Services** execute business logic and call **Database layer** → **Database layer** performs SQL operations on **PostgreSQL**

Each layer has a clear separation of concerns, with GraphQL serving as the contract between frontend and backend.
