# PyJava WebFlux Backend Code Generator

Generador de código para aplicaciones reactivas Spring Boot con WebFlux basado en arquitectura hexagonal.

## Descripción

Esta librería genera proyectos Spring Boot reactivos utilizando Spring WebFlux y R2DBC para persistencia reactiva. Está basada en la librería `pyjava-backend-codegen` pero adaptada para generar aplicaciones completamente reactivas.

## Características

- **Spring WebFlux**: Framework reactivo para aplicaciones web
- **R2DBC**: Acceso reactivo a bases de datos relacionales
- **Project Reactor**: Programación reactiva con Mono y Flux
- **Arquitectura Hexagonal**: Separación clara de responsabilidades
- **Clean Architecture**: Principios de arquitectura limpia
- **MapStruct**: Mapeo automático entre objetos
- **OpenAPI 3**: Documentación automática de APIs
- **Spring Security**: Seguridad reactiva
- **Testing**: Soporte completo para testing reactivo

## Diferencias con pyjava-backend-codegen

| Aspecto | pyjava-backend-codegen | pyjava-webflux-backend-codegen |
|---------|------------------------|--------------------------------|
| Framework Web | Spring MVC | Spring WebFlux |
| Persistencia | JPA/Hibernate | R2DBC |
| Tipos de retorno | Objetos síncronos | Mono/Flux |
| Base de datos | JDBC | R2DBC drivers |
| Transacciones | @Transactional | Reactive transactions |
| Testing | MockMvc | WebTestClient |

## Dependencias principales

- Spring Boot 3.2.5
- Spring WebFlux 3.2.5
- Spring Data R2DBC 3.2.5
- R2DBC PostgreSQL 1.0.4.RELEASE
- Project Reactor 3.6.5
- SpringDoc OpenAPI WebFlux 2.1.0

## Uso

### Configuración

Utiliza el archivo `libs/config/params-webflux.json` para configurar los proyectos a generar:

```json
[
    {
        "project": {
            "general": {
                "name": "back-ms-users-webflux",
                "folder": "back-ms-users-webflux",
                "description": "Reactive microservice for users management with Spring WebFlux"
            },
            "dependencies": {
                "springWebflux": "3.2.5",
                "springDataR2dbc": "3.2.5",
                "r2dbcPostgresql": "1.0.4.RELEASE"
            }
        }
    }
]
```

### Generación de código

```bash
# Generar proyectos WebFlux
python -m libs.pyjava-webflux-backend-codegen libs/config/params-webflux.json
```

## Estructura generada

```
proyecto-webflux/
├── src/main/java/
│   ├── application/
│   │   ├── dto/           # DTOs reactivos
│   │   ├── mapper/        # Mappers
│   │   └── service/       # Servicios reactivos (Mono/Flux)
│   ├── domain/
│   │   ├── model/         # Entidades de dominio
│   │   └── ports/         # Puertos reactivos
│   └── infrastructure/
│       ├── controller/    # Controladores WebFlux
│       ├── entity/        # Entidades R2DBC
│       ├── repository/    # Repositorios R2DBC
│       └── config/        # Configuración reactiva
└── src/test/java/         # Tests reactivos
```

## Ejemplos de código generado

### Controlador reactivo

```java
@RestController
@RequestMapping("/users")
public class UserController {
    
    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Mono<CreateUserResponseContent> createUser(
            @Valid @RequestBody CreateUserRequestContent request) {
        return userUseCase.create(request);
    }
    
    @GetMapping("/{userId}")
    public Mono<GetUserResponseContent> getUser(@PathVariable String userId) {
        return userUseCase.get(userId);
    }
}
```

### Repositorio R2DBC

```java
@Repository
public interface UserRepository extends R2dbcRepository<UserDbo, String> {
    
    @Query("SELECT * FROM users WHERE name ILIKE :search LIMIT :limit OFFSET :offset")
    Flux<UserDbo> findBySearchTerm(@Param("search") String search, 
                                   @Param("limit") Long limit, 
                                   @Param("offset") Long offset);
}
```

### Servicio reactivo

```java
@Service
public class CreateUserService implements CreateUserUseCase {
    
    @Override
    public Mono<CreateUserResponseContent> execute(CreateUserRequestContent request) {
        User user = userMapper.fromCreateRequest(request);
        
        return userRepositoryPort.existsById(user.getUserId())
                .flatMap(exists -> {
                    if (exists) {
                        return Mono.error(new ConflictException("User already exists"));
                    }
                    return userRepositoryPort.save(user);
                })
                .map(userMapper::toDto);
    }
}
```

## Configuración de base de datos

### R2DBC PostgreSQL

```yaml
spring:
  r2dbc:
    url: r2dbc:postgresql://localhost:5432/database
    username: user
    password: password
```

### Configuración reactiva

```java
@Configuration
@EnableR2dbcRepositories
public class R2dbcConfig extends AbstractR2dbcConfiguration {
    
    @Override
    public ConnectionFactory connectionFactory() {
        return new PostgresqlConnectionFactory(
            PostgresqlConnectionConfiguration.builder()
                .host("localhost")
                .port(5432)
                .database("database")
                .username("user")
                .password("password")
                .build());
    }
}
```

## Testing

### WebTestClient

```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class UserControllerTest {
    
    @Autowired
    private WebTestClient webTestClient;
    
    @Test
    void shouldCreateUser() {
        CreateUserRequestContent request = new CreateUserRequestContent();
        
        webTestClient.post()
                .uri("/users")
                .bodyValue(request)
                .exchange()
                .expectStatus().isCreated()
                .expectBody(CreateUserResponseContent.class);
    }
}
```

### StepVerifier

```java
@Test
void shouldFindUserById() {
    Mono<User> userMono = userRepository.findById("user-id");
    
    StepVerifier.create(userMono)
            .expectNextMatches(user -> user.getId().equals("user-id"))
            .verifyComplete();
}
```

## Ventajas de la programación reactiva

1. **Escalabilidad**: Mejor manejo de concurrencia
2. **Eficiencia**: Uso óptimo de recursos
3. **Backpressure**: Control de flujo automático
4. **Non-blocking**: Operaciones no bloqueantes
5. **Composabilidad**: Fácil composición de operaciones asíncronas

## Consideraciones

- **Curva de aprendizaje**: Requiere conocimiento de programación reactiva
- **Debugging**: Más complejo que el código síncrono
- **Ecosistema**: Asegúrate de que todas las dependencias soporten reactive streams
- **Base de datos**: Requiere drivers R2DBC compatibles

## Soporte de bases de datos

- PostgreSQL (R2DBC PostgreSQL)
- H2 (para testing)
- MySQL (R2DBC MySQL) - próximamente
- Microsoft SQL Server (R2DBC MSSQL) - próximamente

## Contribución

Para contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature
3. Implementa los cambios
4. Añade tests
5. Envía un pull request

## Licencia

MIT License
