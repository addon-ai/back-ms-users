# Hexagonal Architecture Templates

## Overview

This collection provides production-ready Spring Boot service templates following **Hexagonal Architecture** (Ports and Adapters) principles. These templates help you quickly bootstrap microservices with clean architecture, best practices, and comprehensive tooling.

## What is Hexagonal Architecture?

Hexagonal Architecture, also known as **Ports and Adapters**, is an architectural pattern that:

- **Isolates** business logic from external concerns
- **Enables** easy testing and maintainability  
- **Provides** flexibility to change implementations
- **Follows** SOLID principles and clean code practices

## Template Collection

We provide **2 main templates** to cover different architectural needs:

### 🍃 Spring Boot Template (`springboot-service`)
**Traditional Spring Boot microservice with blocking I/O**

- **Best for**: Standard CRUD operations, traditional web applications
- **Technology**: Spring MVC, JPA/Hibernate, blocking I/O
- **Use cases**: Most business applications, simple to moderate complexity
- **Performance**: Good for typical web workloads

### ⚡ WebFlux Template (`webflux-service`)  
**Reactive microservice with non-blocking I/O**

- **Best for**: High-concurrency, I/O intensive applications
- **Technology**: Spring WebFlux, R2DBC, reactive streams
- **Use cases**: Real-time applications, high-throughput systems
- **Performance**: Excellent for concurrent workloads

## Key Features

Both templates include:

- ✅ **Hexagonal Architecture** - Clean separation of concerns
- ✅ **Complete CRUD operations** - Ready-to-use REST endpoints
- ✅ **Database integration** - PostgreSQL with proper configuration
- ✅ **Docker support** - Multi-stage Dockerfile and docker-compose
- ✅ **CI/CD workflows** - GitHub Actions with automated testing
- ✅ **Test coverage** - 85% threshold with comprehensive testing
- ✅ **API documentation** - SpringDoc OpenAPI 3 (Swagger)
- ✅ **Code quality** - MapStruct, Lombok, and best practices
- ✅ **Multiple environments** - Local, develop, test, staging, production

## Quick Start

1. **Choose your template** based on your requirements
2. **Use Backstage** to generate your microservice
3. **Configure** your database connection
4. **Start developing** your business logic
5. **Deploy** using the included CI/CD pipeline

## Architecture Benefits

### 🧪 Testability
- Easy unit testing of business logic
- Mock external dependencies
- Test each layer independently

### 🔧 Maintainability  
- Clear separation of concerns
- Easy to modify without side effects
- Follows established patterns

### 🔌 Flexibility
- Swap implementations easily
- Framework-independent core
- Support for multiple adapters

### 📈 Scalability
- Modular design
- Clear boundaries
- Easy to extend functionality

## Next Steps

- [Available Templates](templates.md) - Detailed comparison of templates
