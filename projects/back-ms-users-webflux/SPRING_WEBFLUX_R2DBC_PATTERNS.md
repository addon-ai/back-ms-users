# 🚀 Spring WebFlux + R2DBC + PostgreSQL Patterns

## 📋 Resumen Ejecutivo

Este documento define los patrones y estructuras necesarias para generar automáticamente clases Java compatibles con **Spring WebFlux**, **R2DBC**, y **PostgreSQL UUID** usando plantillas Mustache.

---

## 🏗️ 1. Entity DBO (Database Object)

### ✅ Estructura Requerida

```java
package {{package}}.infrastructure.adapters.output.persistence.entity;

import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;
import org.springframework.data.relational.core.mapping.Column;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import lombok.Builder;
import {{enumPackage}}.{{statusEnum}};
import java.util.UUID;
import java.time.Instant;

/**
 * R2DBC Entity representing {{entityName}} data in the database.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table("{{tableName}}")
public class {{entityName}}Dbo {

    @Id
    @Column("{{primaryKeyColumn}}")
    private UUID id;

    {{#fields}}
    @Column("{{columnName}}")
    private {{javaType}} {{fieldName}};
    {{/fields}}

    @Column("status")
    @Builder.Default
    private {{statusEnum}} status = {{statusEnum}}.ACTIVE;
    
    @Column("created_at")
    private Instant createdAt;

    @Column("updated_at")
    private Instant updatedAt;
}
```

### 🔑 Puntos Críticos

1. **ID siempre UUID**: `private UUID id;`
2. **Columnas snake_case**: `@Column("user_id")`, `@Column("first_name")`
3. **Timestamps como Instant**: `private Instant createdAt;`
4. **Status como Enum**: `private EntityStatus status;`

---

## 🗄️ 2. JPA Repository (R2DBC)

### ✅ Estructura Requerida

```java
package {{package}}.infrastructure.adapters.output.persistence.repository;

import {{package}}.infrastructure.adapters.output.persistence.entity.{{entityName}}Dbo;
import org.springframework.data.r2dbc.repository.Query;
import org.springframework.data.r2dbc.repository.R2dbcRepository;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import java.util.UUID;

/**
 * Spring Data R2DBC Repository for {{entityName}} entities.
 */
@Repository
public interface Jpa{{entityName}}Repository extends R2dbcRepository<{{entityName}}Dbo, UUID> {
    
    /**
     * Find entities with search functionality.
     */
    @Query("SELECT * FROM {{tableName}} u WHERE " +
           "(:search IS NULL OR " +
           {{#searchFields}}
           "LOWER(u.{{columnName}}) LIKE LOWER(CONCAT('%', :search, '%')){{#hasNext}} OR {{/hasNext}}" +
           {{/searchFields}}
           ") " +
           "LIMIT :limit OFFSET :offset")
    Flux<{{entityName}}Dbo> findBySearchTerm(@Param("search") String search, 
                                             @Param("limit") Long limit, 
                                             @Param("offset") Long offset);
    
    /**
     * Count entities matching search term.
     */
    @Query("SELECT COUNT(*) FROM {{tableName}} u WHERE " +
           "(:search IS NULL OR " +
           {{#searchFields}}
           "LOWER(u.{{columnName}}) LIKE LOWER(CONCAT('%', :search, '%')){{#hasNext}} OR {{/hasNext}}" +
           {{/searchFields}}
           ")")
    Mono<Long> countBySearchTerm(@Param("search") String search);
    
    /**
     * Find all entities with pagination.
     */
    @Query("SELECT * FROM {{tableName}} LIMIT :limit OFFSET :offset")
    Flux<{{entityName}}Dbo> findAllPaged(@Param("limit") Long limit, @Param("offset") Long offset);
}
```

### 🔑 Puntos Críticos

1. **Tipo genérico UUID**: `R2dbcRepository<{{entityName}}Dbo, UUID>`
2. **Queries completas**: Siempre incluir `FROM {{tableName}}`
3. **Columnas snake_case en SQL**: `u.first_name`, `u.user_id`
4. **Parámetros reactivos**: `Mono<Long>`, `Flux<{{entityName}}Dbo>`

---

## 🔄 3. Repository Adapter

### ✅ Estructura Requerida

```java
package {{package}}.infrastructure.adapters.output.persistence.adapter;

import {{package}}.domain.ports.output.{{entityName}}RepositoryPort;
import {{package}}.domain.model.{{entityName}};
import {{package}}.infrastructure.adapters.output.persistence.entity.{{entityName}}Dbo;
import {{package}}.infrastructure.adapters.output.persistence.repository.Jpa{{entityName}}Repository;
import {{package}}.application.mapper.{{entityName}}Mapper;
import {{package}}.infrastructure.config.exceptions.InternalServerErrorException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import java.util.UUID;

/**
 * Reactive repository adapter implementing the {{entityName}} domain port.
 */
@Slf4j
@Component
@RequiredArgsConstructor
public class {{entityName}}RepositoryAdapter implements {{entityName}}RepositoryPort {

    private final Jpa{{entityName}}Repository r2dbcRepository;
    private final {{entityName}}Mapper mapper;

    @Override
    public Mono<{{entityName}}> save({{entityName}} entity) {
        log.debug("Saving {{entityName}}: {}", entity);
        return Mono.fromCallable(() -> mapper.toDbo(entity))
                .flatMap(r2dbcRepository::save)
                .map(mapper::toDomain)
                .doOnError(e -> log.error("Database error while saving {{entityName}}: {}", e.getMessage(), e))
                .onErrorMap(e -> new InternalServerErrorException("Failed to save {{entityName}}", e));
    }

    @Override
    public Mono<{{entityName}}> findById(String id) {
        log.debug("Finding {{entityName}} by id: {}", id);
        return r2dbcRepository.findById(UUID.fromString(id))
                .map(mapper::toDomain)
                .doOnError(e -> log.error("Database error while finding {{entityName}} by id {}: {}", id, e.getMessage(), e))
                .onErrorMap(e -> new InternalServerErrorException("Failed to find {{entityName}} by id", e));
    }

    @Override
    public Flux<{{entityName}}> findAll() {
        log.debug("Finding all {{entityName}}s");
        return r2dbcRepository.findAll()
                .map(mapper::toDomain)
                .doOnError(e -> log.error("Database error while finding all {{entityName}}s: {}", e.getMessage(), e))
                .onErrorMap(e -> new InternalServerErrorException("Failed to find all {{entityName}}s", e));
    }

    @Override
    public Mono<Void> deleteById(String id) {
        log.debug("Deleting {{entityName}} by id: {}", id);
        return r2dbcRepository.deleteById(UUID.fromString(id))
                .doOnError(e -> log.error("Database error while deleting {{entityName}} by id {}: {}", id, e.getMessage(), e))
                .onErrorMap(e -> new InternalServerErrorException("Failed to delete {{entityName}} by id", e));
    }

    @Override
    public Mono<Boolean> existsById(String id) {
        log.debug("Checking if {{entityName}} exists by id: {}", id);
        return r2dbcRepository.existsById(UUID.fromString(id))
                .doOnError(e -> log.error("Database error while checking if {{entityName}} exists by id {}: {}", id, e.getMessage(), e))
                .onErrorMap(e -> new InternalServerErrorException("Failed to check if {{entityName}} exists by id", e));
    }

    @Override
    public Flux<{{entityName}}> findBySearchTerm(String search, Integer page, Integer size) {
        log.debug("Searching {{entityName}}s with term: {}, page: {}, size: {}", search, page, size);
        
        long limit = size != null && size > 0 ? size : 20L;
        long offset = page != null && page > 0 ? (page - 1) * limit : 0L;
        
        if (search == null || search.trim().isEmpty()) {
            return r2dbcRepository.findAllPaged(limit, offset)
                    .map(mapper::toDomain)
                    .doOnError(e -> log.error("Database error while finding all {{entityName}}s: {}", e.getMessage(), e))
                    .onErrorMap(e -> new InternalServerErrorException("Failed to find all {{entityName}}s", e));
        }
        
        return r2dbcRepository.findBySearchTerm(search, limit, offset)
                .map(mapper::toDomain)
                .doOnError(e -> log.error("Database error while searching {{entityName}}s: {}", e.getMessage(), e))
                .onErrorMap(e -> new InternalServerErrorException("Failed to search {{entityName}}s", e));
    }
}
```

### 🔑 Puntos Críticos

1. **Conversión String → UUID**: `UUID.fromString(id)` en todos los métodos que reciben String ID
2. **Mapeo reactivo**: `Mono.fromCallable(() -> mapper.toDbo(entity))`
3. **Error handling**: Siempre usar `onErrorMap` para excepciones de dominio
4. **Logging**: Debug para operaciones normales, Error para excepciones

---

## 🗺️ 4. Mapper (MapStruct)

### ✅ Estructura Requerida

```java
package {{package}}.application.mapper;

import {{package}}.domain.model.{{entityName}};
import {{package}}.infrastructure.adapters.output.persistence.entity.{{entityName}}Dbo;
import {{package}}.application.dto.{{entityNameLower}}.Create{{entityName}}RequestContent;
import {{package}}.application.dto.{{entityNameLower}}.Create{{entityName}}ResponseContent;
import {{package}}.application.dto.{{entityNameLower}}.Update{{entityName}}RequestContent;
import {{package}}.application.dto.{{entityNameLower}}.Update{{entityName}}ResponseContent;
import {{package}}.application.dto.{{entityNameLower}}.{{entityName}}Response;
import {{package}}.application.dto.{{entityNameLower}}.List{{entityName}}sResponseContent;
import {{package}}.application.dto.{{entityNameLower}}.Get{{entityName}}ResponseContent;
import {{package}}.application.dto.{{entityNameLower}}.Delete{{entityName}}ResponseContent;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.MappingTarget;
import org.mapstruct.IterableMapping;
import org.mapstruct.NullValuePropertyMappingStrategy;
import org.mapstruct.factory.Mappers;

import java.util.List;
import java.math.BigDecimal;
import java.util.UUID;
import java.time.Instant;

/**
 * MapStruct mapper for {{entityName}} transformations between layers.
 */
@Mapper(componentModel = "spring", nullValuePropertyMappingStrategy = NullValuePropertyMappingStrategy.IGNORE)
public interface {{entityName}}Mapper {

    {{entityName}}Mapper INSTANCE = Mappers.getMapper({{entityName}}Mapper.class);

    // Domain to DBO mappings
    @Mapping(source = "{{entityIdField}}", target = "id", qualifiedByName = "stringToUuid")
    {{#fieldMappings}}
    @Mapping(source = "{{domainField}}", target = "{{dboField}}")
    {{/fieldMappings}}
    @org.mapstruct.Named("domainToDbo")
    {{entityName}}Dbo toDbo({{entityName}} domain);
    
    @Mapping(source = "id", target = "{{entityIdField}}", qualifiedByName = "uuidToString")
    {{#fieldMappings}}
    @Mapping(source = "{{dboField}}", target = "{{domainField}}")
    {{/fieldMappings}}
    @org.mapstruct.Named("dboToDomain")
    {{entityName}} toDomain({{entityName}}Dbo dbo);
    
    // UUID conversion methods
    @org.mapstruct.Named("stringToUuid")
    default UUID stringToUuid(String value) {
        return value != null ? UUID.fromString(value) : null;
    }
    
    @org.mapstruct.Named("uuidToString")
    default String uuidToString(UUID value) {
        return value != null ? value.toString() : null;
    }
    
    // Instant conversion methods
    @org.mapstruct.Named("stringToInstant")
    default Instant stringToInstant(String value) {
        return value != null ? Instant.parse(value) : null;
    }
    
    @org.mapstruct.Named("instantToString")
    default String instantToString(Instant value) {
        return value != null ? value.toString() : null;
    }
    
    @IterableMapping(qualifiedByName = "dboToDomain")
    List<{{entityName}}> toDomainList(List<{{entityName}}Dbo> dbos);
    
    @IterableMapping(qualifiedByName = "domainToDbo")
    List<{{entityName}}Dbo> toDboList(List<{{entityName}}> domains);

    // DTO to Domain mappings for Create/Update operations
    @Mapping(target = "{{entityIdField}}", expression = "java(java.util.UUID.randomUUID().toString())")
    @Mapping(target = "status", constant = "ACTIVE")
    @Mapping(target = "createdAt", expression = "java(java.time.Instant.now().toString())")
    @Mapping(target = "updatedAt", ignore = true)
    {{entityName}} fromCreateRequest(Create{{entityName}}RequestContent request);
    
    @Mapping(target = "{{entityIdField}}", ignore = true)
    @Mapping(target = "status", ignore = true)
    @Mapping(target = "createdAt", ignore = true)
    @Mapping(target = "updatedAt", expression = "java(java.time.Instant.now().toString())")
    {{entityName}} fromUpdateRequest(Update{{entityName}}RequestContent request);
    
    @Mapping(target = "{{entityIdField}}", ignore = true)
    @Mapping(target = "status", ignore = true)
    @Mapping(target = "createdAt", ignore = true)
    @Mapping(target = "updatedAt", expression = "java(java.time.Instant.now().toString())")
    void updateEntityFromRequest(Update{{entityName}}RequestContent request, @MappingTarget {{entityName}} entity);

    // Basic mapping methods
    @org.mapstruct.Named("domainToDto")
    {{entityName}}Response toDto({{entityName}} domain);
    
    @IterableMapping(qualifiedByName = "domainToDto")
    List<{{entityName}}Response> toDtoList(List<{{entityName}}> domains);

    // Specific response mapping methods
    Create{{entityName}}ResponseContent toCreateResponse({{entityName}} domain);
    Get{{entityName}}ResponseContent toGetResponse({{entityName}} domain);
    Update{{entityName}}ResponseContent toUpdateResponse({{entityName}} domain);
    
    // Delete response method
    default Delete{{entityName}}ResponseContent toDeleteResponse({{entityName}} domain) {
        return Delete{{entityName}}ResponseContent.builder()
            .deleted(true)
            .message("{{entityName}} deleted successfully")
            .build();
    }
    
    // Pagination support for list responses
    default List{{entityName}}sResponseContent toListResponse(List<{{entityName}}> domains, int page, int size) {
        if (domains == null) return null;
        
        int total = domains.size();
        int totalPages = (int) Math.ceil((double) total / size);
        
        return List{{entityName}}sResponseContent.builder()
            .{{entityNameLowerPlural}}(toDtoList(domains))
            .page(BigDecimal.valueOf(page))
            .size(BigDecimal.valueOf(size))
            .total(BigDecimal.valueOf(total))
            .totalPages(BigDecimal.valueOf(totalPages))
            .build();
    }
}
```

### 🔑 Puntos Críticos

1. **Conversiones UUID**: Métodos `stringToUuid` y `uuidToString` con `@Named`
2. **Conversiones Instant**: Métodos `stringToInstant` e `instantToString`
3. **Mapeos explícitos**: `@Mapping(source = "userId", target = "id", qualifiedByName = "stringToUuid")`
4. **Timestamps automáticos**: `expression = "java(java.time.Instant.now().toString())"`

---

## 📊 5. Ejemplo de Variables Mustache

### ✅ Variables para User Entity

```json
{
  "package": "com.example.userservice",
  "entityName": "User",
  "entityNameLower": "user",
  "entityNameLowerPlural": "users",
  "entityIdField": "userId",
  "tableName": "users",
  "primaryKeyColumn": "user_id",
  "statusEnum": "EntityStatus",
  "enumPackage": "com.example.userservice.domain.model",
  "fields": [
    {
      "fieldName": "username",
      "columnName": "username",
      "javaType": "String"
    },
    {
      "fieldName": "email",
      "columnName": "email",
      "javaType": "String"
    },
    {
      "fieldName": "firstName",
      "columnName": "first_name",
      "javaType": "String"
    },
    {
      "fieldName": "lastName",
      "columnName": "last_name",
      "javaType": "String"
    }
  ],
  "searchFields": [
    {
      "columnName": "username",
      "hasNext": true
    },
    {
      "columnName": "email",
      "hasNext": true
    },
    {
      "columnName": "first_name",
      "hasNext": true
    },
    {
      "columnName": "last_name",
      "hasNext": false
    }
  ],
  "fieldMappings": [
    {
      "domainField": "username",
      "dboField": "username"
    },
    {
      "domainField": "email",
      "dboField": "email"
    },
    {
      "domainField": "firstName",
      "dboField": "firstName"
    },
    {
      "domainField": "lastName",
      "dboField": "lastName"
    }
  ]
}
```

---

## ⚠️ 6. Errores Comunes a Evitar

### ❌ Problemas Frecuentes

1. **Tipo ID incorrecto**:
   ```java
   // ❌ INCORRECTO
   R2dbcRepository<UserDbo, String>
   
   // ✅ CORRECTO
   R2dbcRepository<UserDbo, UUID>
   ```

2. **Queries SQL incompletas**:
   ```java
   // ❌ INCORRECTO
   @Query("SELECT * FROM WHERE username = :username")
   
   // ✅ CORRECTO
   @Query("SELECT * FROM users WHERE username = :username")
   ```

3. **Mapeo de columnas incorrecto**:
   ```java
   // ❌ INCORRECTO
   @Column("UserId")  // CamelCase
   
   // ✅ CORRECTO
   @Column("user_id") // snake_case
   ```

4. **Conversión UUID faltante**:
   ```java
   // ❌ INCORRECTO
   r2dbcRepository.findById(id)
   
   // ✅ CORRECTO
   r2dbcRepository.findById(UUID.fromString(id))
   ```

5. **Mappers sin conversión de tipos**:
   ```java
   // ❌ INCORRECTO
   @Mapping(source = "userId", target = "id")
   
   // ✅ CORRECTO
   @Mapping(source = "userId", target = "id", qualifiedByName = "stringToUuid")
   ```

---

## 🎯 7. Checklist de Validación

### ✅ Antes de Generar Código

- [ ] **Entity DBO**: ID es `UUID`, columnas en snake_case
- [ ] **Repository**: Tipo genérico es `UUID`, queries completas
- [ ] **Adapter**: Conversión `UUID.fromString(id)` en métodos
- [ ] **Mapper**: Métodos de conversión UUID ↔ String con `@Named`
- [ ] **SQL Schema**: Columnas `UUID` en PostgreSQL
- [ ] **Imports**: `java.util.UUID` en todas las clases necesarias

### ✅ Después de Generar Código

- [ ] **Compilación**: Sin errores de tipos
- [ ] **Tests**: Conversiones UUID funcionan
- [ ] **Runtime**: No errores `operator does not exist: uuid = character varying`
- [ ] **Queries**: SQL válido con nombres de tabla correctos

---

## 🚀 Conclusión

Siguiendo estos patrones, las plantillas Mustache generarán código Java completamente compatible con:

- ✅ **Spring WebFlux** (Reactive)
- ✅ **R2DBC** (Non-blocking database access)
- ✅ **PostgreSQL UUID** (Proper type handling)
- ✅ **MapStruct** (Type-safe mapping)
- ✅ **Hexagonal Architecture** (Clean separation of concerns)

**Resultado**: Código generado automáticamente sin errores de compilación ni runtime.