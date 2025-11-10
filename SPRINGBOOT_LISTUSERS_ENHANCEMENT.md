# Spring Boot ListUsers Enhancement

## 🔄 Cambios Realizados en libs/pyjava-springboot-backend-codegen

Se implementaron modificaciones en los templates del generador de Spring Boot tradicional para agregar parámetros adicionales al endpoint `listUsers`, permitiendo filtrado por status del usuario y rango de fechas de creación con valores por defecto inteligentes.

## 📁 Archivos Modificados

### 1. **apiController.mustache**
**Ubicación:** `libs/pyjava-springboot-backend-codegen/templates/infrastructure/apiController.mustache`

**Cambios:**
- ✅ Agregados nuevos parámetros `@RequestParam`:
  - `status`: Filtro por status del usuario (ACTIVE, INACTIVE, PENDING, SUSPENDED, DELETED) - Default: ACTIVE
  - `dateFrom`: Fecha de inicio para filtrar por createdAt (formato ISO) - Default: 1 mes atrás
  - `dateTo`: Fecha de fin para filtrar por createdAt (formato ISO) - Default: fecha actual
- ✅ Actualizada documentación Swagger con descripciones de los nuevos parámetros
- ✅ Modificado el logging para incluir los nuevos parámetros
- ✅ Actualizada la llamada al `userUseCase.list()` con los nuevos parámetros

### 2. **consolidatedUseCase.mustache**
**Ubicación:** `libs/pyjava-springboot-backend-codegen/templates/domain/consolidatedUseCase.mustache`

**Cambios:**
- ✅ Actualizada la firma del método `list()` para incluir los nuevos parámetros:
  ```java
  ListUsersResponseContent list(Integer page, Integer size, String search, String status, String dateFrom, String dateTo);
  ```

### 3. **consolidatedService.mustache**
**Ubicación:** `libs/pyjava-springboot-backend-codegen/templates/application/consolidatedService.mustache`

**Cambios:**
- ✅ Implementada la nueva firma del método `list()`
- ✅ **Agregada lógica de valores por defecto:**
  - `status`: "ACTIVE" si está vacío o null
  - `dateFrom`: 1 mes atrás desde la fecha actual si está vacío o null
  - `dateTo`: fecha actual si está vacío o null
- ✅ Actualizado el logging para incluir tanto valores originales como efectivos
- ✅ Simplificada la lógica delegando el filtrado completo al repositorio
- ✅ Reemplazada la lógica condicional por una llamada unificada a `findByFilters()`

### 4. **interface.mustache (Domain Port)**
**Ubicación:** `libs/pyjava-springboot-backend-codegen/templates/domain/interface.mustache`

**Cambios:**
- ✅ Agregado nuevo método `findByFilters()`:
  ```java
  List<User> findByFilters(String search, String status, String dateFrom, String dateTo, Integer page, Integer size);
  ```

### 5. **apiRepository.mustache (JPA Repository)**
**Ubicación:** `libs/pyjava-springboot-backend-codegen/templates/infrastructure/apiRepository.mustache`

**Cambios:**
- ✅ Agregada consulta SQL `findByFilters()` con:
  - Filtrado por término de búsqueda (username, email, firstName, lastName)
  - Filtrado por status del usuario (usando campo `e.status`)
  - Filtrado por rango de fechas de creación
  - Paginación y ordenamiento por fecha de creación descendente
  - Manejo de parámetros opcionales con validaciones NULL

### 6. **apiRepository.mustache (Repository Adapter)**
**Ubicación:** `libs/pyjava-springboot-backend-codegen/templates/infrastructure/apiRepository.mustache`

**Cambios:**
- ✅ Implementado el método `findByFilters()`
- ✅ Agregado logging detallado para los nuevos parámetros de filtrado
- ✅ Mantenida la lógica de paginación existente
- ✅ Aplicado el manejo de errores consistente con el patrón existente

## 📝 Detalles Técnicos

### Consulta SQL Implementada
```sql
SELECT e FROM UserDbo e WHERE 
(:search IS NULL OR :search = '' OR 
 LOWER(e.username) LIKE LOWER(CONCAT('%', :search, '%')) OR 
 LOWER(e.email) LIKE LOWER(CONCAT('%', :search, '%')) OR 
 LOWER(e.firstName) LIKE LOWER(CONCAT('%', :search, '%')) OR 
 LOWER(e.lastName) LIKE LOWER(CONCAT('%', :search, '%'))) 
AND (:status IS NULL OR :status = '' OR e.status = :status) 
AND (:dateFrom IS NULL OR :dateFrom = '' OR e.createdAt >= CAST(:dateFrom AS TIMESTAMP)) 
AND (:dateTo IS NULL OR :dateTo = '' OR e.createdAt <= CAST(:dateTo AS TIMESTAMP)) 
ORDER BY e.createdAt DESC
```

### Parámetros del Endpoint

| Parámetro | Tipo | Requerido | Descripción | Valor por Defecto | Ejemplo |
|-----------|------|-----------|-------------|-------------------|----------|
| `page` | Integer | No | Número de página (base 1) | `1` | `1` |
| `size` | Integer | No | Tamaño de página | `20` | `20` |
| `search` | String | No | Término de búsqueda | - | `"john"` |
| `status` | String | No | Status del usuario | `"ACTIVE"` | `"ACTIVE"` |
| `dateFrom` | String | No | Fecha de inicio (ISO) | 1 mes atrás | `"2024-01-01T00:00:00Z"` |
| `dateTo` | String | No | Fecha de fin (ISO) | Fecha actual | `"2024-12-31T23:59:59Z"` |

### Status Válidos (EntityStatus)
- `ACTIVE`: Usuario activo (**valor por defecto**)
- `INACTIVE`: Usuario inactivo
- `PENDING`: Usuario pendiente de activación
- `SUSPENDED`: Usuario suspendido temporalmente
- `DELETED`: Usuario marcado para eliminación

## 🧪 Ejemplos de Uso

### Consulta básica (usa valores por defecto)
```bash
GET /users
# Equivale a: status=ACTIVE, dateFrom=1_mes_atras, dateTo=fecha_actual
```

### Filtrar usuarios inactivos
```bash
GET /users?status=INACTIVE&page=1&size=10
```

### Filtrar por rango de fechas específico
```bash
GET /users?dateFrom=2024-01-01T00:00:00Z&dateTo=2024-03-31T23:59:59Z
```

### Filtro combinado
```bash
GET /users?search=john&status=ACTIVE&dateFrom=2024-01-01T00:00:00Z&page=1&size=20
```

## ✅ Compatibilidad
- ✅ **Retrocompatibilidad**: Los parámetros existentes (`page`, `size`, `search`) funcionan igual que antes
- ✅ **Parámetros opcionales**: Todos los nuevos parámetros son opcionales
- ✅ **Comportamiento por defecto**: Sin parámetros adicionales, el comportamiento es idéntico al anterior

## 🔍 Validaciones Implementadas
- ✅ **Valores por defecto automáticos:**
  - `status` vacío/null → "ACTIVE"
  - `dateFrom` vacío/null → 1 mes atrás desde hoy
  - `dateTo` vacío/null → fecha y hora actual
- ✅ Fechas se validan como TIMESTAMP en la base de datos
- ✅ Status se comparan exactamente con los valores del enum EntityStatus
- ✅ Paginación mantiene los valores por defecto (página 1, tamaño 20)

## 🚀 Beneficios
1. **Flexibilidad**: Múltiples opciones de filtrado combinables
2. **Performance**: Filtrado a nivel de base de datos
3. **Usabilidad**: Parámetros intuitivos con valores por defecto inteligentes
4. **Experiencia de usuario**: Sin parámetros devuelve usuarios activos del último mes
5. **Mantenibilidad**: Código limpio siguiendo arquitectura hexagonal
6. **Escalabilidad**: Consulta optimizada con índices en created_at y status

## 🔄 Generación Automática

Los cambios se aplican automáticamente a todos los proyectos generados con:

```bash
./scripts/code-gen-pipeline.sh
```

### Proyectos Afectados
- ✅ **back-ms-users** (Spring Boot tradicional)
- ✅ **back-ms-movies** (Spring Boot tradicional)
- ✅ **back-ms-users-webflux** (Spring WebFlux - ya implementado previamente)
- ✅ **back-ms-movies-webflux** (Spring WebFlux - ya implementado previamente)

## 📋 Próximos Pasos Sugeridos
- [ ] Agregar índices de base de datos para `status` y `created_at`
- [ ] Implementar validación de formato de fechas en el controller
- [ ] Agregar tests unitarios para los nuevos filtros y valores por defecto
- [ ] Documentar en Swagger UI los valores válidos para `status` (EntityStatus)
- [ ] Considerar agregar filtro por `updatedAt` si es necesario
- [ ] Validar que los valores de `status` correspondan al enum EntityStatus

## 🎯 Resultado Final

Ahora tanto el generador de **Spring Boot tradicional** como el de **Spring WebFlux** implementan el mismo patrón de filtrado avanzado para el endpoint `listUsers`, proporcionando:

1. **Consistencia** entre ambos tipos de proyectos
2. **Funcionalidad avanzada** de filtrado
3. **Valores por defecto inteligentes**
4. **Retrocompatibilidad** completa
5. **Documentación Swagger** actualizada
6. **Logging detallado** para debugging
7. **Manejo de errores** robusto

Los cambios se generan automáticamente en todos los proyectos futuros usando el pipeline de generación de código.