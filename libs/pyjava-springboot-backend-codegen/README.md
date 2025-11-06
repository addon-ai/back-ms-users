# PyJava Backend Code Generator

A sophisticated code generator that creates complete Java Spring Boot applications following **Hexagonal Architecture (Ports and Adapters) principles** from Smithy service definitions.

## Architecture Overview

The generator is organized into specialized components following clean architecture principles:

```
libs/pyjava-backend-codegen/
├── core/                           # Core orchestration components
│   ├── code_generator.py          # Main orchestrator
│   ├── config_loader.py           # Configuration management
│   └── openapi_processor.py       # OpenAPI specification processing
├── utils/                          # Utility components
│   ├── template_renderer.py       # Mustache template rendering
│   ├── file_manager.py            # File system operations
│   └── property_converter.py      # OpenAPI to Java type conversion
├── generators/                     # Layer-specific generators
│   ├── dto_generator.py           # DTO generation
│   ├── domain_generator.py        # Domain layer generation
│   ├── application_generator.py   # Application layer generation
│   ├── infrastructure_generator.py # Infrastructure layer generation
│   ├── test_generator.py          # Test generation
│   └── project_generator.py       # Project structure generation
├── templates/                      # Organized Mustache templates
│   ├── domain/                    # Domain layer templates
│   │   ├── pojo.mustache          # Domain models
│   │   ├── interface.mustache     # Repository ports
│   │   ├── consolidatedUseCase.mustache # Use case interfaces
│   │   └── EntityStatus.mustache  # Status enum
│   ├── application/               # Application layer templates
│   │   ├── apiService.mustache    # Individual services
│   │   ├── consolidatedService.mustache # Consolidated services
│   │   ├── apiMapper.mustache     # MapStruct mappers
│   │   ├── dtoRecord.mustache     # DTO records
│   │   └── LoggingUtils.mustache  # Logging utilities
│   ├── infrastructure/            # Infrastructure layer templates
│   │   ├── apiController.mustache # REST controllers
│   │   ├── apiRepository.mustache # JPA repositories
│   │   ├── apiEntity.mustache     # JPA entities
│   │   ├── Configuration.mustache # Spring configuration
│   │   ├── SecurityConfiguration.mustache # Security config
│   │   └── *Exception.mustache    # Exception classes
│   ├── project/                   # Project configuration templates
│   │   ├── Application.mustache   # Main Spring Boot class
│   │   ├── pom.xml.mustache      # Maven configuration
│   │   ├── application.properties.mustache # App properties
│   │   └── README.md.mustache    # Project documentation
│   └── tests/                     # Test templates
│       ├── serviceTest.mustache   # Service tests
│       ├── controllerTest.mustache # Controller tests
│       ├── mapperTest.mustache    # Mapper tests
│       └── repositoryAdapterTest.mustache # Repository tests
├── docs/                          # Documentation
│   ├── component-diagram.puml     # Architecture diagrams
│   └── sequence-diagram.puml      # Process flow diagrams
├── main.py                        # CLI entry point
└── __main__.py                    # Module entry point
```

## Component Responsibilities

### Core Components (`core/`)

#### CodeGenerator
- **Purpose**: Main orchestrator coordinating all generation phases
- **Responsibilities**: 
  - Extracts data from OpenAPI specifications
  - Coordinates layer-specific generators
  - Manages generation workflow
  - Provides generation summary

#### ConfigLoader
- **Purpose**: Configuration management and package structure building
- **Responsibilities**:
  - Loads project configuration
  - Builds Java package structure
  - Creates Mustache context variables

#### OpenApiProcessor
- **Purpose**: OpenAPI specification processing
- **Responsibilities**:
  - Loads and parses OpenAPI JSON files
  - Extracts schemas, operations, and metadata
  - Provides structured data to generators

### Utility Components (`utils/`)

#### TemplateRenderer
- **Purpose**: Mustache template rendering with organized template discovery
- **Responsibilities**:
  - Renders templates with context data
  - Searches templates across organized subdirectories
  - Handles HTML entity conversion

#### FileManager
- **Purpose**: File system operations and directory management
- **Responsibilities**:
  - Creates directory structures
  - Writes generated files
  - Manages package path conversions

#### PropertyConverter
- **Purpose**: OpenAPI to Java type conversion
- **Responsibilities**:
  - Converts OpenAPI types to Java types
  - Handles validation annotations
  - Manages import statements

### Layer Generators (`generators/`)

Each generator is responsible for a specific architectural layer:

- **DtoGenerator**: Data Transfer Objects with validation
- **DomainGenerator**: Pure domain models and ports
- **ApplicationGenerator**: Use cases, services, and mappers
- **InfrastructureGenerator**: Controllers, repositories, and adapters
- **TestGenerator**: Comprehensive test suites
- **ProjectGenerator**: Project configuration and supporting files

## Template Organization

Templates are organized by architectural layer for better maintainability:

### Domain Layer Templates
- Focus on pure business logic
- No framework dependencies
- Ports and interfaces

### Application Layer Templates
- Business logic orchestration
- DTO validation and mapping
- Use case implementations

### Infrastructure Layer Templates
- External system adapters
- Framework-specific code
- Configuration classes

### Project Templates
- Maven configuration
- Spring Boot setup
- Docker configuration

### Test Templates
- Comprehensive test coverage
- Layer-specific testing strategies
- Mock configurations

## Usage

### As a Module
```bash
python -m libs.pyjava-backend-codegen config.json templates/ output/
```

### Direct Import
```python
from libs.pyjava_backend_codegen.core.code_generator import CodeGenerator

generator = CodeGenerator(config_path, templates_dir, project_config)
generator.generate_complete_project()
```

## Generated Architecture

The generator creates a complete Hexagonal Architecture project:

```
generated-project/
├── src/main/java/com/example/service/
│   ├── domain/                    # Pure business logic
│   │   ├── model/                # Domain entities
│   │   └── ports/               # Use case and repository interfaces
│   ├── application/              # Orchestration layer
│   │   ├── dto/                 # Data transfer objects
│   │   ├── service/             # Use case implementations
│   │   ├── mapper/              # Entity transformations
│   │   └── util/                # Application utilities
│   └── infrastructure/          # External adapters
│       ├── config/              # Spring configuration
│       └── adapters/
│           ├── input/rest/      # REST controllers
│           └── output/persistence/ # JPA repositories
└── src/test/java/               # Comprehensive tests
```

## Key Features

- **Clean Architecture**: Proper dependency inversion and layer separation
- **Comprehensive Testing**: 100% code coverage with edge case handling
- **Dynamic Configuration**: Adapts to any number of entities and operations
- **Template Organization**: Maintainable template structure by architectural layer
- **Type Safety**: Proper Java type conversion with validation
- **Modern Stack**: Spring Boot 3, Jakarta EE, MapStruct, Lombok

## Extension Points

The modular architecture allows easy extension:

1. **New Generators**: Add specialized generators for new layers
2. **Template Customization**: Modify templates for different frameworks
3. **Type Converters**: Add support for new data types
4. **Output Formats**: Generate for different project structures

## Dependencies

- **pystache**: Mustache template rendering
- **pathlib**: Modern path operations
- **json**: Configuration parsing
- **subprocess**: External tool integration