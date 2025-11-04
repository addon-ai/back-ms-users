$version: "2"
namespace com.example.userservice
use aws.protocols#restJson1

@title("User Service API")
@cors(origin: "*")
@restJson1
@documentation("A service for managing user accounts with full CRUD operations and search capabilities. This service provides comprehensive user management functionality including user registration and authentication, profile management and updates, user search and listing with pagination, and account status management (active, inactive, suspended).")
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

// === OPERATIONS ===

@http(method: "POST", uri: "/users", code: 201)
@idempotent
@documentation("Creates a new user account. Registers a new user with the provided information. The username and email must be unique across the system. Password requirements include minimum length of 6 characters.")
operation CreateUser {
    input: CreateUserRequest,
    output: UserResponse,
    errors: [ValidationError, ConflictError]
}

@http(method: "GET", uri: "/users/{userId}")
@readonly
@documentation("Retrieves a user by their unique identifier. Returns the complete user profile information including status and timestamps. The user ID must be a valid UUID format.")
operation GetUser {
    input: GetUserRequest,
    output: UserResponse,
    errors: [NotFoundError]
}

@http(method: "PUT", uri: "/users/{userId}")
@idempotent
@documentation("Updates an existing user's profile information. Allows partial updates to user profile fields including first name, last name, and email address. All fields are optional in the update request.")
operation UpdateUser {
    input: UpdateUserRequest, 
    output: UserResponse,
    errors: [NotFoundError, ValidationError]
}

@http(method: "DELETE", uri: "/users/{userId}")
@idempotent
@documentation("Deletes a user account. Permanently removes a user account from the system. This operation cannot be undone. Consider using status updates for soft deletion instead.")
operation DeleteUser {
    input: DeleteUserRequest,
    output: DeleteUserResponse,
    errors: [NotFoundError]
}

@http(method: "GET", uri: "/users")
@readonly
@documentation("Lists users with pagination and search capabilities. Returns a paginated list of users with optional search functionality. Search can be performed across username, email, first name, and last name fields. Supports pagination with configurable page size (max 100 users per page).")
operation ListUsers {
    input: ListUsersRequest,
    output: ListUsersResponse
}

// === INPUT STRUCTURES ===

structure CreateUserRequest {
    @required
    @length(min: 3, max: 50)
    username: String,

    @required
    @pattern("^[^@]+@[^@]+\\.[^@]+$")
    email: String,

    @required
    @length(min: 6, max: 100)
    password: String,

    @length(min: 1, max: 100)
    firstName: String,

    @length(min: 1, max: 100) 
    lastName: String
}

structure GetUserRequest {
    @httpLabel
    @required
    userId: String
}

structure UpdateUserRequest {
    @httpLabel
    @required
    userId: String,

    @length(min: 1, max: 100)
    firstName: String,

    @length(min: 1, max: 100)
    lastName: String,

    @pattern("^[^@]+@[^@]+\\.[^@]+$") 
    email: String
}

structure DeleteUserRequest {
    @httpLabel
    @required
    userId: String
}

structure ListUsersRequest {
    @httpQuery("page")
    @range(min: 1)
    page: Integer = 1,

    @httpQuery("size")
    @range(min: 1, max: 100)
    size: Integer = 20,

    @httpQuery("search")
    @length(max: 100)
    search: String
}

// === OUTPUT STRUCTURES ===

structure UserResponse {
    @required
    userId: String,

    @required
    username: String,

    @required
    email: String,

    firstName: String,
    lastName: String,

    @required
    status: UserStatus,

    @required
    createdAt: Timestamp,

    @required
    updatedAt: Timestamp
}

structure DeleteUserResponse {
    @required
    message: String,

    @required
    deleted: Boolean
}

structure ListUsersResponse {
    @required
    users: UserList,

    @required
    page: Integer,

    @required
    size: Integer,

    @required
    total: Integer,

    @required
    totalPages: Integer
}

list UserList {
    member: UserResponse
}

// === ERRORS ===

@error("client")
@httpError(400)
structure ValidationError {
    @required
    message: String,

    field: String
}

@error("client") 
@httpError(404)
structure NotFoundError {
    @required
    message: String
}

@error("client")
@httpError(409)
structure ConflictError {
    @required
    message: String
}

// === ENUMS ===

enum UserStatus {
    ACTIVE = "ACTIVE",
    INACTIVE = "INACTIVE",
    SUSPENDED = "SUSPENDED"
}