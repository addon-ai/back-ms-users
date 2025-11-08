# List Users Pagination Issue - Complete Solution Guide

## 🚨 Problem Summary

**Issue**: GET `/users?page=1&size=20` endpoint returns mock data with "string" values instead of real database data and incorrect pagination metadata.

**Current Response**:
```json
{
  "users": [
    {
      "userId": "string",
      "username": "string", 
      "email": "string",
      "firstName": "string",
      "lastName": "string",
      "status": "string",
      "createdAt": "string",
      "updatedAt": "string"
    }
  ],
  "page": 0,
  "size": 0, 
  "total": 0,
  "totalPages": 0
}
```

**Expected Response**:
```json
{
  "users": [
    {
      "userId": "123e4567-e89b-12d3-a456-426614174000",
      "username": "john_doe",
      "email": "john@example.com", 
      "firstName": "John",
      "lastName": "Doe",
      "status": "ACTIVE",
      "createdAt": "2024-11-08T16:30:00Z",
      "updatedAt": "2024-11-08T16:30:00Z"
    }
  ],
  "page": 1,
  "size": 20,
  "total": 1,
  "totalPages": 1
}
```

---

## 🔍 Root Cause Analysis

### 1. SQL Query Issues

**Problem**: Repository queries have incorrect table aliases and column names.

**Current Broken Queries**:
```sql
-- Wrong alias 'e' instead of 'u'
SELECT * FROM users u WHERE 
LOWER(e.username) LIKE LOWER(CONCAT('%', :search, '%'))

-- Wrong column names (camelCase instead of snake_case)
LOWER(e.firstName) LIKE LOWER(CONCAT('%', :search, '%'))
```

**Correct Queries**:
```sql
-- Correct alias 'u' and snake_case columns
SELECT * FROM users u WHERE 
LOWER(u.username) LIKE LOWER(CONCAT('%', :search, '%')) OR
LOWER(u.first_name) LIKE LOWER(CONCAT('%', :search, '%'))
```

### 2. Missing Count Methods

**Problem**: Repository lacks proper count methods for pagination.

**Missing Methods**:
- `countAll()` - Count total records
- `countBySearchTerm()` - Count filtered records

### 3. Incorrect Service Logic

**Problem**: Service doesn't implement proper pagination with total count.

**Current Issues**:
- No total count calculation
- Incorrect pagination logic
- Missing reactive composition with `Mono.zip()`

### 4. Mapper Configuration Issues

**Problem**: Mapper doesn't properly handle pagination metadata.

---

## ✅ Complete Solution Implementation

### 1. Fix Repository SQL Queries

**File**: `JpaUserRepository.java`

```java
@Repository
public interface JpaUserRepository extends R2dbcRepository<UserDbo, UUID> {
    
    /**
     * ✅ CORRECTED: Fixed table aliases and column names
     */
    @Query("SELECT * FROM users u WHERE " +
           "(:search IS NULL OR :search = '' OR " +
           "LOWER(u.username) LIKE LOWER(CONCAT('%', :search, '%')) OR " +
           "LOWER(u.email) LIKE LOWER(CONCAT('%', :search, '%')) OR " +
           "LOWER(u.first_name) LIKE LOWER(CONCAT('%', :search, '%')) OR " +
           "LOWER(u.last_name) LIKE LOWER(CONCAT('%', :search, '%'))) " +
           "ORDER BY u.created_at DESC " +
           "LIMIT :limit OFFSET :offset")
    Flux<UserDbo> findBySearchTerm(@Param("search") String search, 
                                   @Param("limit") Long limit, 
                                   @Param("offset") Long offset);
    
    /**
     * ✅ CORRECTED: Fixed count query with proper aliases
     */
    @Query("SELECT COUNT(*) FROM users u WHERE " +
           "(:search IS NULL OR :search = '' OR " +
           "LOWER(u.username) LIKE LOWER(CONCAT('%', :search, '%')) OR " +
           "LOWER(u.email) LIKE LOWER(CONCAT('%', :search, '%')) OR " +
           "LOWER(u.first_name) LIKE LOWER(CONCAT('%', :search, '%')) OR " +
           "LOWER(u.last_name) LIKE LOWER(CONCAT('%', :search, '%')))")
    Mono<Long> countBySearchTerm(@Param("search") String search);
    
    /**
     * ✅ NEW: Added missing count all method
     */
    @Query("SELECT COUNT(*) FROM users")
    Mono<Long> countAll();
    
    /**
     * ✅ CORRECTED: Proper pagination query
     */
    @Query("SELECT * FROM users u ORDER BY u.created_at DESC LIMIT :limit OFFSET :offset")
    Flux<UserDbo> findAllPaged(@Param("limit") Long limit, @Param("offset") Long offset);
}
```

### 2. Update Repository Port Interface

**File**: `UserRepositoryPort.java`

```java
public interface UserRepositoryPort {
    
    Mono<User> save(User user);
    Mono<User> findById(String id);
    Flux<User> findAll();
    Flux<User> findBySearchTerm(String search, Integer page, Integer size);
    Mono<Void> deleteById(String id);
    Mono<Boolean> existsById(String id);
    
    /**
     * ✅ NEW: Added missing count methods
     */
    Mono<Long> countBySearchTerm(String search);
    Mono<Long> countAll();
}
```

### 3. Fix Repository Adapter Implementation

**File**: `UserRepositoryAdapter.java`

```java
@Slf4j
@Component
@RequiredArgsConstructor
public class UserRepositoryAdapter implements UserRepositoryPort {

    private final JpaUserRepository r2dbcRepository;
    private final UserMapper mapper;

    /**
     * ✅ CORRECTED: Proper search with pagination
     */
    @Override
    public Flux<User> findBySearchTerm(String search, Integer page, Integer size) {
        log.debug("Searching Users with term: {}, page: {}, size: {}", search, page, size);
        
        long limit = size != null && size > 0 ? size : 20L;
        long offset = page != null && page > 0 ? (page - 1) * limit : 0L;
        
        if (search == null || search.trim().isEmpty()) {
            return r2dbcRepository.findAllPaged(limit, offset)
                    .map(mapper::toDomain)
                    .doOnError(e -> log.error("Database error while finding all Users: {}", e.getMessage(), e))
                    .onErrorMap(e -> new InternalServerErrorException("Failed to find all Users", e));
        }
        
        return r2dbcRepository.findBySearchTerm(search, limit, offset)
                .map(mapper::toDomain)
                .doOnError(e -> log.error("Database error while searching Users: {}", e.getMessage(), e))
                .onErrorMap(e -> new InternalServerErrorException("Failed to search Users", e));
    }
    
    /**
     * ✅ NEW: Implemented count methods
     */
    @Override
    public Mono<Long> countBySearchTerm(String search) {
        log.debug("Counting Users with search term: {}", search);
        return r2dbcRepository.countBySearchTerm(search)
                .doOnError(e -> log.error("Database error while counting Users: {}", e.getMessage(), e))
                .onErrorMap(e -> new InternalServerErrorException("Failed to count Users", e));
    }
    
    @Override
    public Mono<Long> countAll() {
        log.debug("Counting all Users");
        return r2dbcRepository.countAll()
                .doOnError(e -> log.error("Database error while counting all Users: {}", e.getMessage(), e))
                .onErrorMap(e -> new InternalServerErrorException("Failed to count all Users", e));
    }
}
```

### 4. Fix Service Layer Logic

**File**: `UserService.java`

```java
@Service
@RequiredArgsConstructor
public class UserService implements UserUseCase {

    private final UserRepositoryPort userRepositoryPort;
    private final UserMapper userMapper;

    /**
     * ✅ CORRECTED: Proper pagination with total count using reactive composition
     */
    @Override
    public Mono<ListUsersResponseContent> list(Integer page, Integer size, String search) {
        logger.info("Executing ListUsers with page: {}, size: {}, search: {}", page, size, search);
        
        int pageNum = page != null && page > 0 ? page : 1;
        int pageSize = size != null && size > 0 ? size : 20;
        
        Mono<Long> countMono;
        Flux<User> userFlux;
        
        if (search != null && !search.trim().isEmpty()) {
            countMono = userRepositoryPort.countBySearchTerm(search);
            userFlux = userRepositoryPort.findBySearchTerm(search, pageNum, pageSize);
        } else {
            countMono = userRepositoryPort.countAll();
            userFlux = userRepositoryPort.findBySearchTerm("", pageNum, pageSize);
        }
        
        return Mono.zip(
                userFlux.collectList(),
                countMono
        ).map(tuple -> {
            List<User> users = tuple.getT1();
            Long totalCount = tuple.getT2();
            logger.info("Retrieved {} users out of {} total", users.size(), totalCount);
            return userMapper.toListResponse(users, pageNum, pageSize, totalCount.intValue());
        })
        .doOnError(e -> logger.error("Error in ListUsers", e));
    }
}
```

### 5. Fix Mapper Implementation

**File**: `UserMapper.java`

```java
@Mapper(componentModel = "spring", nullValuePropertyMappingStrategy = NullValuePropertyMappingStrategy.IGNORE)
public interface UserMapper {

    /**
     * ✅ CORRECTED: Proper pagination support with total count
     */
    default ListUsersResponseContent toListResponse(List<User> domains, int page, int size, int totalCount) {
        if (domains == null) return null;
        
        int totalPages = (int) Math.ceil((double) totalCount / size);
        
        return ListUsersResponseContent.builder()
            .users(toDtoList(domains))
            .page(BigDecimal.valueOf(page))
            .size(BigDecimal.valueOf(size))
            .total(BigDecimal.valueOf(totalCount))
            .totalPages(BigDecimal.valueOf(totalPages))
            .build();
    }
    
    /**
     * ✅ NEW: Conversion methods for audit fields (Instant ↔ String)
     */
    default String instantToString(Instant instant) {
        return instant != null ? instant.toString() : null;
    }
    
    default Instant stringToInstant(String dateString) {
        return dateString != null ? Instant.parse(dateString) : null;
    }
    
    /**
     * ✅ CORRECTED: Domain to DBO with audit field conversion
     */
    @Mapping(source = "userId", target = "id")
    @Mapping(source = "createdAt", target = "createdAt", qualifiedByName = "stringToInstant")
    @Mapping(source = "updatedAt", target = "updatedAt", qualifiedByName = "stringToInstant")
    UserDbo toDbo(User domain);
    
    /**
     * ✅ CORRECTED: DBO to Domain with audit field conversion
     */
    @Mapping(source = "id", target = "userId")
    @Mapping(source = "createdAt", target = "createdAt", qualifiedByName = "instantToString")
    @Mapping(source = "updatedAt", target = "updatedAt", qualifiedByName = "instantToString")
    User toDomain(UserDbo dbo);
}
```

---

## 🎯 Python/Mustache Code Generation Templates

### 1. Repository Interface Template

**File**: `jpa_repository.mustache`

```mustache
package {{packageName}}.infrastructure.adapters.output.persistence.repository;

import {{packageName}}.infrastructure.adapters.output.persistence.entity.{{EntityName}}Dbo;
import org.springframework.data.r2dbc.repository.Query;
import org.springframework.data.r2dbc.repository.R2dbcRepository;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import java.util.UUID;

@Repository
public interface Jpa{{EntityName}}Repository extends R2dbcRepository<{{EntityName}}Dbo, UUID> {
    
    /**
     * Find entities with search functionality.
     */
    @Query("SELECT * FROM {{tableName}} u WHERE " +
           "(:search IS NULL OR :search = '' OR " +
           {{#searchableFields}}
           "LOWER(u.{{dbColumnName}}) LIKE LOWER(CONCAT('%', :search, '%')){{#hasNext}} OR {{/hasNext}}" +
           {{/searchableFields}}
           ") ORDER BY u.created_at DESC " +
           "LIMIT :limit OFFSET :offset")
    Flux<{{EntityName}}Dbo> findBySearchTerm(@Param("search") String search, 
                                             @Param("limit") Long limit, 
                                             @Param("offset") Long offset);
    
    /**
     * Count entities matching search term.
     */
    @Query("SELECT COUNT(*) FROM {{tableName}} u WHERE " +
           "(:search IS NULL OR :search = '' OR " +
           {{#searchableFields}}
           "LOWER(u.{{dbColumnName}}) LIKE LOWER(CONCAT('%', :search, '%')){{#hasNext}} OR {{/hasNext}}" +
           {{/searchableFields}}
           ")")
    Mono<Long> countBySearchTerm(@Param("search") String search);
    
    /**
     * Find all entities with pagination.
     */
    @Query("SELECT * FROM {{tableName}} u ORDER BY u.created_at DESC LIMIT :limit OFFSET :offset")
    Flux<{{EntityName}}Dbo> findAllPaged(@Param("limit") Long limit, @Param("offset") Long offset);
    
    /**
     * Count all entities.
     */
    @Query("SELECT COUNT(*) FROM {{tableName}}")
    Mono<Long> countAll();
}
```

### 2. Service Layer Template

**File**: `service.mustache`

```mustache
@Service
@RequiredArgsConstructor
public class {{EntityName}}Service implements {{EntityName}}UseCase {

    private final {{EntityName}}RepositoryPort {{entityName.toLowerCase}}RepositoryPort;
    private final {{EntityName}}Mapper {{entityName.toLowerCase}}Mapper;

    @Override
    public Mono<List{{EntityName}}sResponseContent> list(Integer page, Integer size, String search) {
        logger.info("Executing List{{EntityName}}s with page: {}, size: {}, search: {}", page, size, search);
        
        int pageNum = page != null && page > 0 ? page : 1;
        int pageSize = size != null && size > 0 ? size : 20;
        
        Mono<Long> countMono;
        Flux<{{EntityName}}> {{entityName.toLowerCase}}Flux;
        
        if (search != null && !search.trim().isEmpty()) {
            countMono = {{entityName.toLowerCase}}RepositoryPort.countBySearchTerm(search);
            {{entityName.toLowerCase}}Flux = {{entityName.toLowerCase}}RepositoryPort.findBySearchTerm(search, pageNum, pageSize);
        } else {
            countMono = {{entityName.toLowerCase}}RepositoryPort.countAll();
            {{entityName.toLowerCase}}Flux = {{entityName.toLowerCase}}RepositoryPort.findBySearchTerm("", pageNum, pageSize);
        }
        
        return Mono.zip(
                {{entityName.toLowerCase}}Flux.collectList(),
                countMono
        ).map(tuple -> {
            List<{{EntityName}}> {{entityName.toLowerCase}}s = tuple.getT1();
            Long totalCount = tuple.getT2();
            logger.info("Retrieved {} {{entityName.toLowerCase}}s out of {} total", {{entityName.toLowerCase}}s.size(), totalCount);
            return {{entityName.toLowerCase}}Mapper.toListResponse({{entityName.toLowerCase}}s, pageNum, pageSize, totalCount.intValue());
        })
        .doOnError(e -> logger.error("Error in List{{EntityName}}s", e));
    }
}
```

### 3. Mapper Template

**File**: `mapper.mustache`

```mustache
@Mapper(componentModel = "spring", nullValuePropertyMappingStrategy = NullValuePropertyMappingStrategy.IGNORE)
public interface {{EntityName}}Mapper {

    /**
     * Audit field conversion methods
     */
    @Named("instantToString")
    default String instantToString(Instant instant) {
        return instant != null ? instant.toString() : null;
    }
    
    @Named("stringToInstant")
    default Instant stringToInstant(String dateString) {
        return dateString != null ? Instant.parse(dateString) : null;
    }
    
    /**
     * Domain to DBO mapping with audit field conversion
     */
    @Mapping(source = "{{entityIdField}}", target = "id")
    {{#auditFields}}
    @Mapping(source = "{{fieldName}}", target = "{{fieldName}}", qualifiedByName = "stringToInstant")
    {{/auditFields}}
    {{EntityName}}Dbo toDbo({{EntityName}} domain);
    
    /**
     * DBO to Domain mapping with audit field conversion
     */
    @Mapping(source = "id", target = "{{entityIdField}}")
    {{#auditFields}}
    @Mapping(source = "{{fieldName}}", target = "{{fieldName}}", qualifiedByName = "instantToString")
    {{/auditFields}}
    {{EntityName}} toDomain({{EntityName}}Dbo dbo);
    
    /**
     * Pagination support for list responses
     */
    default List{{EntityName}}sResponseContent toListResponse(List<{{EntityName}}> domains, int page, int size, int totalCount) {
        if (domains == null) return null;
        
        int totalPages = (int) Math.ceil((double) totalCount / size);
        
        return List{{EntityName}}sResponseContent.builder()
            .{{entityName.toLowerCase}}s(toDtoList(domains))
            .page(BigDecimal.valueOf(page))
            .size(BigDecimal.valueOf(size))
            .total(BigDecimal.valueOf(totalCount))
            .totalPages(BigDecimal.valueOf(totalPages))
            .build();
    }
}
```

---

## 🐍 Python Generation Script Context

### Context Variables for Templates

```python
# Context for repository template
repository_context = {
    "packageName": "com.example.userservice",
    "EntityName": "User",
    "tableName": "users",
    "searchableFields": [
        {"dbColumnName": "username", "hasNext": True},
        {"dbColumnName": "email", "hasNext": True}, 
        {"dbColumnName": "first_name", "hasNext": True},
        {"dbColumnName": "last_name", "hasNext": False}
    ]
}

# Context for service template  
service_context = {
    "EntityName": "User",
    "entityName": {"toLowerCase": "user"}
}

# Context for mapper template
mapper_context = {
    "EntityName": "User", 
    "entityName": {"toLowerCase": "user"},
    "entityIdField": "userId",
    "auditFields": [
        {"fieldName": "createdAt"},
        {"fieldName": "updatedAt"}
    ]
}
```

---

## 📋 Implementation Checklist

### ✅ Repository Layer Fixes
- [ ] Fix SQL query table aliases (`e` → `u`)
- [ ] Fix column names (camelCase → snake_case)
- [ ] Add `countAll()` method
- [ ] Add `countBySearchTerm()` method
- [ ] Implement proper pagination logic

### ✅ Service Layer Fixes  
- [ ] Use `Mono.zip()` for reactive composition
- [ ] Calculate total count properly
- [ ] Handle empty search terms correctly
- [ ] Pass correct parameters to mapper

### ✅ Mapper Layer Fixes
- [ ] Add audit field conversion methods
- [ ] Fix pagination metadata calculation
- [ ] Handle null values properly
- [ ] Use correct BigDecimal types

### ✅ Code Generation Updates
- [ ] Update repository Mustache templates
- [ ] Update service Mustache templates  
- [ ] Update mapper Mustache templates
- [ ] Update Python generation scripts
- [ ] Add proper context variables

---

## 🚀 Expected Result After Fix

**Correct API Response**:
```json
{
  "users": [
    {
      "userId": "123e4567-e89b-12d3-a456-426614174000",
      "username": "john_doe", 
      "email": "john@example.com",
      "firstName": "John",
      "lastName": "Doe", 
      "status": "ACTIVE",
      "createdAt": "2024-11-08T16:30:00Z",
      "updatedAt": "2024-11-08T16:30:00Z"
    }
  ],
  "page": 1,
  "size": 20, 
  "total": 1,
  "totalPages": 1
}
```

**Key Improvements**:
- ✅ Real data instead of "string" placeholders
- ✅ Correct pagination metadata
- ✅ Proper total count calculation
- ✅ Working search functionality
- ✅ Reactive composition with proper error handling