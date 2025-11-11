# Available Templates

## Template Overview

Our collection provides **2 main templates** designed for different architectural and performance requirements:

## 🍃 Spring Boot Template

### `springboot-service`
**Traditional Spring Boot microservice with Hexagonal Architecture**

| Aspect | Details |
|--------|---------|
| **Type** | `springboot` |
| **Description** | Template for generating Spring Boot microservices with Hexagonal Architecture |
| **Technology Stack** | Spring MVC, JPA/Hibernate, PostgreSQL |
| **I/O Model** | Blocking (traditional servlet model) |
| **Best For** | Standard CRUD operations, traditional web applications |
| **Concurrency** | Thread-per-request model |
| **Learning Curve** | Easy - familiar Spring Boot patterns |

#### Key Features
- ✅ Spring Boot 3.2.5 with Java 21
- ✅ JPA/Hibernate for database access
- ✅ Traditional REST controllers
- ✅ Blocking I/O operations
- ✅ Standard Spring Security integration
- ✅ Familiar development patterns

#### When to Use
- **Standard web applications** with moderate traffic
- **CRUD-heavy applications** with traditional data access patterns
- **Teams familiar** with traditional Spring Boot development
- **Simple to moderate complexity** business logic
- **Integration with legacy systems** that use blocking I/O

---

## ⚡ WebFlux Template

### `webflux-service`
**Reactive microservice with Spring WebFlux and Hexagonal Architecture**

| Aspect | Details |
|--------|---------|
| **Type** | `webflux` |
| **Description** | Template for generating WebFlux reactive microservices with Hexagonal Architecture |
| **Technology Stack** | Spring WebFlux, R2DBC, PostgreSQL |
| **I/O Model** | Non-blocking (reactive streams) |
| **Best For** | High-concurrency, I/O intensive applications |
| **Concurrency** | Event-loop model with backpressure |
| **Learning Curve** | Moderate - requires reactive programming knowledge |

#### Key Features
- ✅ Spring WebFlux with reactive streams
- ✅ R2DBC for reactive database access
- ✅ Reactive REST endpoints (`Mono` and `Flux`)
- ✅ Non-blocking I/O operations
- ✅ Built-in backpressure handling
- ✅ Reactive security integration

#### When to Use
- **High-concurrency applications** (thousands of concurrent users)
- **I/O intensive operations** with external service calls
- **Streaming data processing** and real-time applications
- **Microservices architectures** with many inter-service calls
- **Applications requiring** high throughput and low resource usage

---

## Template Comparison

| Feature | Spring Boot | WebFlux |
|---------|-------------|---------|
| **Programming Model** | Imperative | Reactive |
| **Threading** | Thread-per-request | Event loop |
| **Database Access** | JPA/Hibernate (blocking) | R2DBC (reactive) |
| **HTTP Client** | RestTemplate/WebClient | WebClient (reactive) |
| **Error Handling** | Try-catch blocks | Reactive error operators |
| **Testing** | Standard Spring Test | WebTestClient, StepVerifier |

## Architecture Commonalities

Both templates share the same **Hexagonal Architecture** structure:

### 🎯 Domain Layer
- Pure business logic
- No external dependencies
- Domain models and entities
- Business rules and validations

### 🔧 Application Layer  
- Use cases and application services
- DTOs and mappers
- Coordinates between domain and infrastructure
- Port definitions (interfaces)

### 🏗️ Infrastructure Layer
- REST controllers (MVC vs WebFlux)
- Database repositories (JPA vs R2DBC)
- External service clients
- Configuration and exception handling

## Choosing the Right Template

### Choose **Spring Boot** (`springboot-service`) when:
- ✅ Building traditional web applications
- ✅ Team is familiar with Spring Boot
- ✅ Moderate concurrency requirements
- ✅ Simple to moderate complexity
- ✅ Integration with blocking systems
- ✅ Rapid development is priority

### Choose **WebFlux** (`webflux-service`) when:
- ✅ High concurrency requirements
- ✅ I/O intensive operations
- ✅ Real-time or streaming applications
- ✅ Microservices with many external calls
- ✅ Resource efficiency is critical
- ✅ Team has reactive programming experience
