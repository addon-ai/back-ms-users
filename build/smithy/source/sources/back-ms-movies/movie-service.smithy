$version: "2"

namespace com.example.movieservice

use aws.protocols#restJson1

@title("Movie Service API")
@cors(origin: "*")
@restJson1
@documentation("A comprehensive service for managing movie rentals with catalog and transaction processing. This service provides movie catalog management (CRUD operations), rental transaction processing, inventory tracking and availability management, late fee calculation and payment processing, and user rental history and status tracking.")
service MovieService {
    version: "2023-01-01",
    operations: [
        CreateMovie,
        GetMovie,
        UpdateMovie,
        DeleteMovie,
        ListMovies,
        CreateRental,
        UpdateRental,
        GetRental,
        ListRentals
    ]
}

// Movie Operations

@http(method: "POST", uri: "/movies")
@documentation("Creates a new movie in the rental catalog with complete information including title, director, genre, release year, duration, available copies, and rental price. Validates movie information and ensures no duplicate titles exist.")
operation CreateMovie {
    input: CreateMovieRequest,
    output: CreateMovieResponse,
    errors: [ValidationError, ConflictError]
}

@http(method: "GET", uri: "/movies/{movieId}")
@documentation("Retrieves a movie by its unique identifier. Returns complete movie information including availability status, rental price, and current inventory levels.")
operation GetMovie {
    input: GetMovieRequest,
    output: GetMovieResponse,
    errors: [NotFoundError]
}

@http(method: "PUT", uri: "/movies/{movieId}")
@documentation("Updates an existing movie's information. Allows partial updates to movie catalog information including title, director, genre, availability, and pricing. All fields are optional.")
operation UpdateMovie {
    input: UpdateMovieRequest,
    output: UpdateMovieResponse,
    errors: [ValidationError, NotFoundError]
}

@http(method: "DELETE", uri: "/movies/{movieId}")
@documentation("Removes a movie from the catalog. Permanently removes a movie from the rental catalog. This operation should only be performed if no active rentals exist for the movie.")
operation DeleteMovie {
    input: DeleteMovieRequest,
    output: DeleteMovieResponse,
    errors: [NotFoundError]
}

@http(method: "GET", uri: "/movies")
@documentation("Lists movies with filtering and pagination. Returns a paginated list of movies with optional filtering by genre and director. Supports pagination for efficient catalog browsing.")
operation ListMovies {
    input: ListMoviesRequest,
    output: ListMoviesResponse
}

// Rental Operations

@http(method: "POST", uri: "/rentals")
@documentation("Creates a new movie rental transaction. Processes a new rental request by checking movie availability, calculating rental price based on duration, and creating a rental record with due date calculation. Updates movie inventory automatically.")
operation CreateRental {
    input: CreateRentalRequest,
    output: CreateRentalResponse,
    errors: [ValidationError, NotFoundError, ConflictError]
}

@http(method: "PUT", uri: "/rentals/{rentalId}")
@documentation("Updates a rental transaction (typically for returns). Updates rental information including return date, late fees, and status. Automatically calculates late fees based on return date and updates movie inventory when rental is returned.")
operation UpdateRental {
    input: UpdateRentalRequest,
    output: UpdateRentalResponse,
    errors: [NotFoundError]
}

@http(method: "GET", uri: "/rentals/{rentalId}")
@documentation("Retrieves a rental transaction by its unique identifier. Returns complete rental information including dates, pricing, late fees, and current status.")
operation GetRental {
    input: GetRentalRequest,
    output: GetRentalResponse,
    errors: [NotFoundError]
}

@http(method: "GET", uri: "/rentals")
@documentation("Lists rental transactions with filtering and pagination. Returns a paginated list of rentals with optional filtering by user ID and rental status. Useful for rental history and management.")
operation ListRentals {
    input: ListRentalsRequest,
    output: ListRentalsResponse
}

// Movie Structures
structure CreateMovieRequest {
    @httpPayload
    body: CreateMovieRequestContent
}

structure CreateMovieRequestContent {
    @required
    title: String,
    
    @required
    director: String,
    
    @required
    genre: String,
    
    @required
    releaseYear: Integer,
    
    @required
    duration: Integer,
    
    description: String,
    
    @required
    availableCopies: Integer,
    
    @required
    rentalPrice: Double
}

structure CreateMovieResponse {
    @httpPayload
    body: CreateMovieResponseContent
}

structure CreateMovieResponseContent {
    @required
    movieId: String,
    
    @required
    title: String,
    
    @required
    director: String,
    
    @required
    genre: String,
    
    @required
    releaseYear: Integer,
    
    @required
    duration: Integer,
    
    description: String,
    
    @required
    availableCopies: Integer,
    
    @required
    rentalPrice: Double,
    
    @required
    createdAt: String,
    
    @required
    status: String
}

structure GetMovieRequest {
    @httpLabel
    @required
    movieId: String
}

structure GetMovieResponse {
    @httpPayload
    body: GetMovieResponseContent
}

structure GetMovieResponseContent {
    @required
    movieId: String,
    
    @required
    title: String,
    
    @required
    director: String,
    
    @required
    genre: String,
    
    @required
    releaseYear: Integer,
    
    @required
    duration: Integer,
    
    description: String,
    
    @required
    availableCopies: Integer,
    
    @required
    rentalPrice: Double,
    
    @required
    createdAt: String,
    
    @required
    updatedAt: String,
    
    @required
    status: String
}

structure UpdateMovieRequest {
    @httpLabel
    @required
    movieId: String,
    
    @httpPayload
    body: UpdateMovieRequestContent
}

structure UpdateMovieRequestContent {
    title: String,
    director: String,
    genre: String,
    releaseYear: Integer,
    duration: Integer,
    description: String,
    availableCopies: Integer,
    rentalPrice: Double
}

structure UpdateMovieResponse {
    @httpPayload
    body: UpdateMovieResponseContent
}

structure UpdateMovieResponseContent {
    @required
    movieId: String,
    
    @required
    title: String,
    
    @required
    director: String,
    
    @required
    genre: String,
    
    @required
    releaseYear: Integer,
    
    @required
    duration: Integer,
    
    description: String,
    
    @required
    availableCopies: Integer,
    
    @required
    rentalPrice: Double,
    
    @required
    updatedAt: String,
    
    @required
    status: String
}

structure DeleteMovieRequest {
    @httpLabel
    @required
    movieId: String
}

structure DeleteMovieResponse {
    @httpPayload
    body: DeleteMovieResponseContent
}

structure DeleteMovieResponseContent {
    @required
    deleted: Boolean,
    
    @required
    message: String
}

structure ListMoviesRequest {
    @httpQuery("page")
    page: Integer,
    
    @httpQuery("size")
    size: Integer,
    
    @httpQuery("genre")
    genre: String,
    
    @httpQuery("director")
    director: String
}

structure ListMoviesResponse {
    @httpPayload
    body: ListMoviesResponseContent
}

structure ListMoviesResponseContent {
    @required
    movies: MovieList,
    
    @required
    page: Integer,
    
    @required
    size: Integer,
    
    @required
    total: Integer,
    
    @required
    totalPages: Integer
}

// Rental Structures
structure CreateRentalRequest {
    @httpPayload
    body: CreateRentalRequestContent
}

structure CreateRentalRequestContent {
    @required
    movieId: String,
    
    @required
    userId: String,
    
    @required
    rentalDays: Integer
}

structure CreateRentalResponse {
    @httpPayload
    body: CreateRentalResponseContent
}

structure CreateRentalResponseContent {
    @required
    rentalId: String,
    
    @required
    movieId: String,
    
    @required
    userId: String,
    
    @required
    rentalDate: String,
    
    @required
    dueDate: String,
    
    @required
    totalPrice: Double,
    
    @required
    createdAt: String,
    
    @required
    status: String
}

structure UpdateRentalRequest {
    @httpLabel
    @required
    rentalId: String,
    
    @httpPayload
    body: UpdateRentalRequestContent
}

structure UpdateRentalRequestContent {
    returnDate: String,
    lateFee: Double,
    status: String
}

structure UpdateRentalResponse {
    @httpPayload
    body: UpdateRentalResponseContent
}

structure UpdateRentalResponseContent {
    @required
    rentalId: String,
    
    @required
    returnDate: String,
    
    @required
    lateFee: Double,
    
    @required
    totalAmount: Double,
    
    @required
    createdAt: String,
    
    @required
    updatedAt: String,
    
    @required
    status: String
}

structure GetRentalRequest {
    @httpLabel
    @required
    rentalId: String
}

structure GetRentalResponse {
    @httpPayload
    body: GetRentalResponseContent
}

structure GetRentalResponseContent {
    @required
    rentalId: String,
    
    @required
    movieId: String,
    
    @required
    userId: String,
    
    @required
    rentalDate: String,
    
    @required
    dueDate: String,
    
    returnDate: String,
    
    @required
    totalPrice: Double,
    
    lateFee: Double,
    
    @required
    createdAt: String,
    
    @required
    updatedAt: String,
    
    @required
    status: String
}

structure ListRentalsRequest {
    @httpQuery("page")
    page: Integer,
    
    @httpQuery("size")
    size: Integer,
    
    @httpQuery("userId")
    userId: String,
    
    @httpQuery("status")
    status: String
}

structure ListRentalsResponse {
    @httpPayload
    body: ListRentalsResponseContent
}

structure ListRentalsResponseContent {
    @required
    rentals: RentalList,
    
    @required
    page: Integer,
    
    @required
    size: Integer,
    
    @required
    total: Integer,
    
    @required
    totalPages: Integer
}

// Common Structures
structure MovieResponse {
    @required
    movieId: String,
    
    @required
    title: String,
    
    @required
    director: String,
    
    @required
    genre: String,
    
    @required
    releaseYear: Integer,
    
    @required
    duration: Integer,
    
    description: String,
    
    @required
    availableCopies: Integer,
    
    @required
    rentalPrice: Double,
    
    @required
    createdAt: String,
    
    @required
    updatedAt: String,
    
    @required
    status: String
}

structure RentalResponse {
    @required
    rentalId: String,
    
    @required
    movieId: String,
    
    @required
    userId: String,
    
    @required
    rentalDate: String,
    
    @required
    dueDate: String,
    
    returnDate: String,
    
    @required
    totalPrice: Double,
    
    lateFee: Double,
    
    @required
    createdAt: String,
    
    @required
    updatedAt: String,
    
    @required
    status: String
}

list MovieList {
    member: MovieResponse
}

list RentalList {
    member: RentalResponse
}

// Error Structures
@error("client")
@httpError(400)
structure ValidationError {
    @required
    message: String,
    
    @required
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

structure ValidationErrorResponseContent {
    @required
    message: String,
    
    @required
    field: String
}

structure NotFoundErrorResponseContent {
    @required
    message: String
}

structure ConflictErrorResponseContent {
    @required
    message: String
}