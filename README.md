# Hexagonal Architecture Spring Boot Generator

## Overview

This project generates complete Java Spring Boot applications following **Hexagonal Architecture (Ports and Adapters) principles** from Smithy service definitions. It automatically creates a fully functional backend with proper layer separation and dependency inversion.

## Features

### Core Generation
- ✅ **Hexagonal Architecture Structure** with Domain, Application, and Infrastructure layers
- ✅ **Smithy Integration** - Generates OpenAPI specs from Smithy definitions
- ✅ **Complete Code Generation** - DTOs, Services, Controllers, Repositories, Entities
- ✅ **Comprehensive Test Coverage** - Unit tests with 100% code coverage including edge cases
- ✅ **Component-Based Generator** - Modular architecture with specialized generators
- ✅ **Dependency Inversion** - All dependencies point toward the domain layer
- ✅ **Spring Boot 3** with Jakarta EE support
- ✅ **MapStruct** for entity transformations
- ✅ **JPA/Hibernate** for persistence
- ✅ **Bean Validation** with proper annotations
- ✅ **Lombok** for boilerplate reduction
- ✅ **Logging Utilities** with MDC support and comprehensive test coverage

### Documentation Generation
- ✅ **OpenAPI Documentation** - Generates PlantUML diagrams from OpenAPI specifications
- ✅ **Architecture Diagrams** - Creates hexagonal architecture component diagrams
- ✅ **Sequence Diagrams** - Generates CRUD sequence diagrams for each service
- ✅ **Real Code Analysis** - Analyzes actual Java controller files for accurate diagrams
- ✅ **Template-Based Diagrams** - Uses Mustache templates for consistent diagram generation
- ✅ **Automated Pipeline** - Integrated documentation generation in code generation pipeline

## Quick Start

### 1. Install Dependencies

```bash
# Install Python dependencies
poetry install

# Install Java and Maven (if not already installed)
brew install maven
sdk install java 21.0.2-tem
sdk use java 21.0.2-tem
```

### 2. Generate Project

```bash
# Make script executable
chmod +x scripts/run-hexagonal-architecture-generator.sh

# Run generator
./scripts/run-hexagonal-architecture-generator.sh
```

### 3. Run Generated Project

```bash
cd generated-project

# Build and run
mvn spring-boot:run
```

### 4. Test API

```bash
# Create user
curl -X POST http://localhost:8080/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "password123",
    "firstName": "John",
    "lastName": "Doe"
  }'

# Get user
curl http://localhost:8080/users/{userId}

# List users
curl http://localhost:8080/users
```

## Prerequisites

### System Requirements
- **Java 21** (recommended with SDKMAN)
- **Maven 3.8+**
- **Python 3.6+**
- **Smithy CLI** (optional, can use Maven plugin)

### Java Installation with SDKMAN
```bash
sdk install java 21.0.2-tem
sdk use java 21.0.2-tem
```

### Maven Installation
```bash
# Using Homebrew (macOS)
brew install maven

# Using SDKMAN
sdk install maven

# Verify installation
mvn -version
```

### Python Dependencies
```bash
# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install project dependencies
poetry install
```

The project uses `pyproject.toml` for dependency management:
```toml
[tool.poetry.dependencies]
python = "^3.8"
pystache = "^0.6.8"
```

### Smithy CLI (Optional)
```bash
# Using Homebrew
brew tap smithy-lang/tap
brew install smithy-cli

# Verify installation
smithy --version
```

## Project Structure

```
boiler-plate-code-gen/
├── libs/
│   ├── pyjava-backend-codegen/         # Core code generation library
│   │   ├── code_generator.py           # Main orchestrator
│   │   ├── generators/                 # Component-based generators
│   │   │   ├── dto_generator.py        # DTO generation
│   │   │   ├── domain_generator.py     # Domain layer generation
│   │   │   ├── application_generator.py # Application layer generation
│   │   │   ├── infrastructure_generator.py # Infrastructure layer generation
│   │   │   ├── test_generator.py       # Test generation
│   │   │   └── project_generator.py    # Project structure generation
│   │   └── templates/                  # Mustache templates for code generation
│   ├── openapi-docs-generator/         # OpenAPI documentation generator
│   │   ├── generators/
│   │   │   └── puml_generator.py       # PlantUML diagram generator
│   │   └── templates/
│   │       ├── class_diagram.mustache  # Entity class diagrams
│   │       └── api_diagram.mustache    # API operation diagrams
│   └── architect-docs-generator/       # Architecture documentation generator
│       ├── core/
│       │   └── project_analyzer.py     # Java project analyzer
│       ├── generators/
│       │   ├── component_diagram_generator.py # Component diagrams
│       │   └── sequence_diagram_generator.py  # Sequence diagrams
│       └── templates/
│           ├── component_diagram.mustache     # Hexagonal architecture diagrams
│           └── sequence_diagram.mustache      # CRUD sequence diagrams
├── scripts/
│   ├── code-gen-pipeline.sh            # Complete generation pipeline
│   ├── hexagonal-architecture-generator.py # Legacy generator script
│   └── run-hexagonal-architecture-generator.sh # Execution script
├── smithy/
│   ├── user-service.smithy             # User service definition
│   ├── movie-service.smithy            # Movie service definition
│   └── smithy-build.json               # Smithy build configuration
├── build/
│   └── smithy/                         # Generated OpenAPI specifications
├── docs/
│   └── puml/                           # Generated PlantUML diagrams
│       ├── open-api/                   # OpenAPI-based diagrams
│       └── components/                 # Architecture diagrams
├── projects/                           # Generated Spring Boot projects
│   ├── back-ms-users/                  # User microservice
│   └── back-ms-movies/                 # Movie microservice
└── generated-project/                  # Legacy output directory
```

## Generator Usage

### Component-Based Generator (Recommended)

```bash
# Using the new component-based generator
python3 libs/pyjava-backend-codegen/code_generator.py <config_path> <templates_dir> <output_dir>
```

### Example

```bash
python3 libs/pyjava-backend-codegen/code_generator.py \
  libs/pyjava-backend-codegen/templates/template-config.json \
  libs/pyjava-backend-codegen/templates \
  generated-project
```

### Legacy Generator

```bash
# Using the legacy monolithic generator
python3 scripts/hexagonal-architecture-generator.py \
  templates/java/template-config.json \
  templates/java \
  generated-project
```

### Complete Generation Pipeline (Recommended)

```bash
# Run the complete pipeline: code generation + documentation
./scripts/code-gen-pipeline.sh
```

### Individual Generators

```bash
# Code generation only
./scripts/run-hexagonal-architecture-generator.sh

# OpenAPI documentation only
python3 libs/openapi-docs-generator/generators/puml_generator.py

# Architecture documentation only
python3 libs/architect-docs-generator/generators/component_diagram_generator.py
python3 libs/architect-docs-generator/generators/sequence_diagram_generator.py
```

## Generated Architecture

The generator creates a complete Hexagonal Architecture project with proper package structure:

```
generated-project/
├── src/main/java/com/example/userservice/
│   ├── domain/
│   │   ├── model/User.java                    # Pure domain entities
│   │   └── ports/
│   │       ├── input/UserUseCase.java         # Consolidated use case interface
│   │       └── output/UserRepositoryPort.java # Repository interfaces
│   ├── application/
│   │   ├── dto/                               # Data transfer objects
│   │   │   ├── CreateUserRequestContent.java
│   │   │   ├── GetUserResponseContent.java
│   │   │   └── ...
│   │   ├── service/UserService.java           # Consolidated use case implementation
│   │   ├── mapper/UserMapper.java             # Entity mappers
│   │   └── util/LoggingUtils.java             # Logging utilities with MDC support
│   └── infrastructure/
│       ├── config/ApplicationConfiguration.java # Spring configuration
│       └── adapters/
│           ├── input/rest/UserController.java   # REST controllers
│           └── output/persistence/
│               ├── entity/UserDbo.java         # JPA entities
│               ├── repository/JpaUserRepository.java # Spring Data repos
│               └── adapter/UserRepositoryAdapter.java # Repository implementations
├── src/test/java/com/example/userservice/
│   ├── application/
│   │   ├── service/UserServiceTest.java       # Comprehensive service tests
│   │   └── util/LoggingUtilsTest.java         # Logging utility tests
│   └── resources/
│       └── logback-test.xml                   # Test logging configuration
└── pom.xml
```

### Architecture Layers

#### Domain Layer (`domain/`) - The Core
- **Models**: Pure POJOs without framework dependencies
- **Input Ports**: Use case interfaces (e.g., `CreateUserUseCase`)
- **Output Ports**: Repository interfaces (e.g., `UserRepositoryPort`)

#### Application Layer (`application/`) - Orchestration
- **Services**: Use case implementations with business logic
- **DTOs**: Request/Response objects with validation
- **Mappers**: MapStruct interfaces for transformations

#### Infrastructure Layer (`infrastructure/`) - Adapters
- **Input Adapters**: REST controllers for HTTP handling
- **Output Adapters**: JPA repositories and database adapters
- **JPA Entities**: Database entities with annotations
- **Configuration**: Spring Boot configuration classes

## Template Mapping Strategy

The generator intelligently maps existing templates to Hexagonal Architecture layers:

| Template | Domain Layer | Application Layer | Infrastructure Layer |
|----------|-------------|-------------------|---------------------|
| `pojo.mustache` | Domain Model | DTO | - |
| `apiEntity.mustache` | - | - | JPA Entity |
| `interface.mustache` | Use Case Port | - | - |
| `apiService.mustache` | - | Use Case Implementation | - |
| `apiController.mustache` | - | - | REST Controller |
| `apiRepository.mustache` | Repository Port | - | JPA Repository + Adapter |

## Configuration

### Template Configuration (`templates/java/template-config.json`)

Key configuration options:
```json
{
  "configOptions": {
    "basePackage": "com.example.userservice",
    "mainClass": "UserServiceApplication",
    "useSpringBoot3": "true",
    "useJakartaEe": "true",
    "useBeanValidation": "true",
    "java21": "true"
  }
}
```

## Smithy Service Definition

### 1. Project Structure Requirements

**IMPORTANT**: Each Smithy service file must have a corresponding projection in `smithy-build.json` to generate the OpenAPI specification.

#### Required Configuration:
```json
{
  "version": "1.0",
  "projections": {
    "user_service": {
      "plugins": {
        "openapi": {
          "service": "com.example.userservice#UserService",
          "protocol": "aws.protocols#restJson1"
        }
      }
    },
    "movie_service": {
      "plugins": {
        "openapi": {
          "service": "com.example.movieservice#MovieService",
          "protocol": "aws.protocols#restJson1"
        }
      }
    }
  }
}
```

### 2. Operation Naming Conventions

**IMPORTANT**: The generator expects operations to follow specific CRUD prefixes for proper code generation:

#### Required Operation Prefixes:
- **`Create`** - For creating new entities (e.g., `CreateUser`, `CreateMovie`, `CreateRental`)
- **`Get`** - For retrieving single entities (e.g., `GetUser`, `GetMovie`, `GetRental`)
- **`Update`** - For updating existing entities (e.g., `UpdateUser`, `UpdateMovie`, `UpdateRental`)
- **`Delete`** - For deleting entities (e.g., `DeleteUser`, `DeleteMovie`, `DeleteRental`)
- **`List`** - For listing multiple entities (e.g., `ListUsers`, `ListMovies`, `ListRentals`)

#### Examples:
✅ **Correct Naming**:
```smithy
operations: [
    CreateMovie,     // → Generates MovieService with Movie entity
    GetMovie,        // → Generates MovieService with Movie entity
    UpdateMovie,     // → Generates MovieService with Movie entity
    DeleteMovie,     // → Generates MovieService with Movie entity
    ListMovies,      // → Generates MovieService with Movie entity (singular)
    CreateRental,    // → Generates RentalService with Rental entity
    UpdateRental     // → Generates RentalService with Rental entity
]
```

❌ **Incorrect Naming** (will cause generation issues):
```smithy
operations: [
    RentMovie,       // ❌ No CRUD prefix - generates "Entity" fallback
    ReturnMovie,     // ❌ No CRUD prefix - generates "Entity" fallback
    SearchUsers,     // ❌ No CRUD prefix - generates "Entity" fallback
    FindMovies       // ❌ No CRUD prefix - generates "Entity" fallback
]
```

### 3. Define Your Service in Smithy

Create or modify `smithy/user-service.smithy`:

```smithy
@title("User Service API")
@cors(origin: "*")
@restJson1
@documentation("A service for managing user accounts.")
service UserService {
    version: "2023-01-01",
    operations: [
        CreateUser,
        GetUser, 
        UpdateUser,
        DeleteUser,
        ListUsers
    ]
}

@http(method: "POST", uri: "/users")
operation CreateUser {
    input: CreateUserRequest,
    output: CreateUserResponse,
    errors: [ValidationError, ConflictError]
}

// Define your structures, operations, etc.
```

## Generated Components

### Example Generated Files

1. **Domain Model** (`domain/model/User.java`)
```java
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class User {
    private String userId;
    private String username;
    private String email;
    // ... other fields
}
```

2. **Consolidated Use Case Interface** (`domain/ports/input/UserUseCase.java`)
```java
public interface UserUseCase {
    CreateUserResponseContent create(CreateUserRequestContent request);
    GetUserResponseContent get(String userId);
    UpdateUserResponseContent update(String userId, UpdateUserRequestContent request);
    DeleteUserResponseContent delete(String userId);
    ListUsersResponseContent list();
}
```

3. **Consolidated Application Service** (`application/service/UserService.java`)
```java
@Service
@RequiredArgsConstructor
@Transactional
public class UserService implements UserUseCase {
    private final UserRepositoryPort userRepositoryPort;
    private final UserMapper userMapper;
    
    @Override
    public CreateUserResponseContent create(CreateUserRequestContent request) {
        // Business logic implementation
    }
    
    @Override
    public GetUserResponseContent get(String userId) {
        // Business logic implementation
    }
    
    // ... other CRUD operations
}
```

4. **REST Controller** (`infrastructure/adapters/input/rest/UserController.java`)
```java
@RestController
@RequestMapping("/users")
@RequiredArgsConstructor
public class UserController {
    private final UserUseCase userUseCase;
    
    @PostMapping
    public ResponseEntity<CreateUserResponseContent> createUser(
            @Valid @RequestBody CreateUserRequestContent request,
            @RequestHeader("X-Request-ID") String requestId) {
        return ResponseEntity.status(HttpStatus.CREATED).body(userUseCase.create(request));
    }
    
    @GetMapping("/{userId}")
    public ResponseEntity<GetUserResponseContent> getUser(@PathVariable String userId) {
        return ResponseEntity.ok(userUseCase.get(userId));
    }
    
    // ... other endpoints
}
```

## Generated Artifacts

### Code Artifacts
The generated `pom.xml` includes:
- Spring Boot 3.x (Web, Data JPA, Validation)
- Jakarta EE APIs
- MapStruct for mapping
- Lombok for boilerplate reduction
- H2/PostgreSQL for database
- JUnit 5 for testing
- AssertJ for fluent assertions
- Mockito for mocking
- Logback for logging with test configuration

### Documentation Artifacts
Generated in `docs/puml/`:
- **OpenAPI Diagrams** (`open-api/`) - Entity class diagrams and API operation diagrams
- **Component Diagrams** (`components/`) - Hexagonal architecture diagrams showing layer relationships
- **Sequence Diagrams** (`components/`) - CRUD operation flows for each service
- **PlantUML Format** - All diagrams in `.puml` format for easy rendering and version control

## API Endpoints

Generated REST API endpoints:
- `POST /users` - Create user
- `GET /users/{userId}` - Get user by ID
- `PUT /users/{userId}` - Update user
- `DELETE /users/{userId}` - Delete user
- `GET /users` - List users with pagination and search

## Architecture Principles

The generator ensures:

1. **Dependency Rule**: Dependencies point inward toward the domain (hexagon center)
2. **Ports and Adapters**: External communication only through well-defined interfaces
3. **Interface Segregation**: Small, focused interfaces for each use case
4. **Single Responsibility**: Each class has one reason to change
5. **Dependency Inversion**: High-level modules don't depend on low-level modules

## Development Workflow

1. **Define Service**: Create/modify Smithy service definition with proper @documentation traits
2. **Generate Everything**: Run the complete pipeline `./scripts/code-gen-pipeline.sh`
   - Generates Spring Boot projects
   - Creates OpenAPI specifications
   - Generates architecture diagrams
   - Creates sequence diagrams
3. **Review Documentation**: Check generated PlantUML diagrams in `docs/puml/`
4. **Implement Business Logic**: Add specific business rules in services
5. **Add Tests**: Create unit and integration tests
6. **Configure Database**: Update `application.properties` for your database
7. **Deploy**: Build and deploy the Spring Boot application

## Component Architecture

The generator uses a modular component-based architecture with three main libraries:

### Code Generation Components (`libs/pyjava-backend-codegen/`)

1. **DTOGenerator** (`dto_generator.py`) - Generates data transfer objects
2. **DomainGenerator** (`domain_generator.py`) - Creates domain models and ports
3. **ApplicationGenerator** (`application_generator.py`) - Builds application services and mappers
4. **InfrastructureGenerator** (`infrastructure_generator.py`) - Creates controllers and adapters
5. **TestGenerator** (`test_generator.py`) - Generates comprehensive test suites
6. **ProjectGenerator** (`project_generator.py`) - Sets up project structure and configuration

### Documentation Generation Components

#### OpenAPI Documentation (`libs/openapi-docs-generator/`)
- **PumlGenerator** - Generates PlantUML diagrams from OpenAPI specifications
- **Entity Classification** - Separates domain entities from DTOs
- **API Operation Diagrams** - Creates visual representations of REST endpoints

#### Architecture Documentation (`libs/architect-docs-generator/`)
- **ProjectAnalyzer** - Analyzes Java project structure and extracts metadata
- **ComponentDiagramGenerator** - Creates hexagonal architecture diagrams
- **SequenceDiagramGenerator** - Generates CRUD sequence diagrams from actual controller code
- **Real Code Analysis** - Extracts method signatures and parameters from Java files

### Test Coverage Features

- **100% Code Coverage** - All generated code includes comprehensive tests
- **Edge Case Testing** - Tests for null parameters, exceptions, and error conditions
- **Functional Testing** - LoggingUtils tests use functional approach with assertDoesNotThrow()
- **MDC Testing** - Complete coverage of logging conditional branches
- **Repository Testing** - Proper mocking and verification of repository interactions

## Customization

### Adding New Operations
1. Add operation to Smithy service definition
2. Run generator to create new use cases and endpoints
3. Implement business logic in generated services

### Adding New Entities

Modify the `entities` list in the component generators:

```python
entities = ["User", "Product", "Order"]
```

### Modifying Templates
1. Edit Mustache templates in `libs/pyjava-backend-codegen/templates/`
2. Regenerate project to apply changes

### Extending Test Coverage
1. Modify test templates to add new test scenarios
2. Update `serviceTest.mustache` for additional edge cases
3. Enhance `LoggingUtilsTest.mustache` for new logging patterns

### Extending Entities
1. Add fields to Smithy structures
2. Regenerate to update DTOs, entities, and mappers

## Best Practices

1. **Keep Domain Pure**: Domain layer should have no external dependencies (hexagon center)
2. **Use Ports and Adapters**: All external communication goes through well-defined interfaces
3. **Test Each Layer**: Unit test domain logic, integration test adapters
4. **Follow Naming Conventions**: UseCase, Port, Adapter, Dbo suffixes
5. **Maintain Dependency Direction**: Always point toward the domain (inward to hexagon center)

## Troubleshooting

### Common Issues

1. **Python Dependencies Missing**
   ```bash
   poetry install
   ```

2. **Smithy Build Fails**
   ```bash
   smithy build --debug
   ```

3. **Generated Code Compilation Errors**
   - Check Java version (requires Java 21)
   - Verify Maven dependencies
   - Ensure proper package structure

4. **Template Rendering Issues**
   - Verify Mustache template syntax
   - Check context variables in generator script

5. **Missing Templates**: Ensure all required `.mustache` files exist
6. **Package Conflicts**: Check that `basePackage` is correctly set
7. **Permission Errors**: Ensure output directory is writable

## Extension Points

The generator can be extended to:

### Code Generation Extensions
- Support different frameworks (Quarkus, Micronaut)
- Add more adapter types (messaging, external APIs)
- Generate integration tests
- Add more hexagonal patterns

### Documentation Extensions
- Generate API documentation in other formats (Swagger UI, Postman collections)
- Create deployment diagrams
- Generate database schema diagrams
- Add interactive diagram features
- Support other diagram formats (Mermaid, Draw.io)

### Pipeline Extensions
- Add code quality checks
- Integrate with CI/CD pipelines
- Generate project templates for different IDEs
- Add Docker containerization

## Contributing

1. Fork the repository
2. Create feature branch
3. Add/modify templates or generator logic
4. Test with sample Smithy services
5. Submit pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review generated code structure
3. Verify Smithy service definition
4. Check Python and Java versions