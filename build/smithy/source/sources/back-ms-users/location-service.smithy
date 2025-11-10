$version: "2"

namespace com.example.userservice

use aws.protocols#restJson1

@title("Location Service API")
@cors(origin: "*")
@restJson1
@documentation("A comprehensive service for managing user locations and geographic data with full CRUD operations. This service provides user location management (home, work, billing, shipping addresses), geographic data hierarchy (countries, regions, cities, neighborhoods), location type categorization and validation, geospatial coordinates support (latitude/longitude), and postal code and address validation.")
service LocationService {
    version: "2023-01-01",
    operations: [
        CreateLocation,
        GetLocation,
        UpdateLocation,
        DeleteLocation,
        ListLocations,
        GetCountries,
        GetRegionsByCountry,
        GetCitiesByRegion,
        GetNeighborhoodsByCity
    ]
}

// Location Operations

@http(method: "POST", uri: "/locations")
@documentation("Creates a new location for a user. Registers a new location with complete address information including geographic hierarchy (country, region, city, neighborhood) and optional geospatial coordinates. Supports multiple location types per user.")
operation CreateLocation {
    input: CreateLocationRequest,
    output: CreateLocationResponse,
    errors: [ValidationError, ConflictError]
}

@http(method: "GET", uri: "/locations/{locationId}")
@documentation("Retrieves a location by its unique identifier. Returns complete location information including resolved geographic hierarchy with country, region, city, and neighborhood details.")
operation GetLocation {
    input: GetLocationRequest,
    output: GetLocationResponse,
    errors: [NotFoundError]
}

@http(method: "PUT", uri: "/locations/{locationId}")
@documentation("Updates an existing location's information. Allows partial updates to location fields including address, geographic references, coordinates, and location type. All fields are optional.")
operation UpdateLocation {
    input: UpdateLocationRequest,
    output: UpdateLocationResponse,
    errors: [ValidationError, NotFoundError]
}

@http(method: "DELETE", uri: "/locations/{locationId}")
@documentation("Deletes a location. Permanently removes a location from the system. This operation cannot be undone. Consider using status updates for soft deletion instead.")
operation DeleteLocation {
    input: DeleteLocationRequest,
    output: DeleteLocationResponse,
    errors: [NotFoundError]
}

@http(method: "GET", uri: "/locations")
@documentation("Lists locations with filtering and pagination. Returns a paginated list of locations with optional filtering by user ID and location type. Supports pagination for efficient data retrieval.")
operation ListLocations {
    input: ListLocationsRequest,
    output: ListLocationsResponse
}

// Geographic Data Operations

@http(method: "GET", uri: "/countries")
@documentation("Retrieves list of available countries. Returns all countries in the system with optional search functionality. Used for populating country selection in location forms.")
operation GetCountries {
    input: GetCountriesRequest,
    output: GetCountriesResponse
}

@http(method: "GET", uri: "/countries/{countryId}/regions")
@documentation("Retrieves regions within a specific country. Returns all regions (states, provinces) that belong to the specified country. Used for cascading geographic selection in location forms.")
operation GetRegionsByCountry {
    input: GetRegionsByCountryRequest,
    output: GetRegionsByCountryResponse,
    errors: [NotFoundError]
}

@http(method: "GET", uri: "/regions/{regionId}/cities")
@documentation("Retrieves cities within a specific region. Returns all cities that belong to the specified region. Used for cascading geographic selection in location forms.")
operation GetCitiesByRegion {
    input: GetCitiesByRegionRequest,
    output: GetCitiesByRegionResponse,
    errors: [NotFoundError]
}

@http(method: "GET", uri: "/cities/{cityId}/neighborhoods")
@documentation("Retrieves neighborhoods within a specific city. Returns all neighborhoods that belong to the specified city. Used for detailed address specification in location forms.")
operation GetNeighborhoodsByCity {
    input: GetNeighborhoodsByCityRequest,
    output: GetNeighborhoodsByCityResponse,
    errors: [NotFoundError]
}

// Location Structures
structure CreateLocationRequest {
    @httpPayload
    body: CreateLocationRequestContent
}

structure CreateLocationRequestContent {
    @required
    userId: String,
    
    @required
    countryId: String,
    
    @required
    regionId: String,
    
    @required
    cityId: String,
    
    neighborhoodId: String,
    
    @required
    address: String,
    
    postalCode: String,
    
    latitude: Double,
    
    longitude: Double,
    
    @required
    locationType: LocationType
}

structure CreateLocationResponse {
    @httpPayload
    body: CreateLocationResponseContent
}

structure CreateLocationResponseContent {
    @required
    locationId: String,
    
    @required
    userId: String,
    
    @required
    countryId: String,
    
    @required
    regionId: String,
    
    @required
    cityId: String,
    
    neighborhoodId: String,
    
    @required
    address: String,
    
    postalCode: String,
    
    latitude: Double,
    
    longitude: Double,
    
    @required
    locationType: LocationType,
    
    @required
    createdAt: String,
    
    @required
    status: String
}

structure GetLocationRequest {
    @httpLabel
    @required
    locationId: String
}

structure GetLocationResponse {
    @httpPayload
    body: GetLocationResponseContent
}

structure GetLocationResponseContent {
    @required
    locationId: String,
    
    @required
    userId: String,
    
    @required
    country: CountryInfo,
    
    @required
    region: RegionInfo,
    
    @required
    city: CityInfo,
    
    neighborhood: NeighborhoodInfo,
    
    @required
    address: String,
    
    postalCode: String,
    
    latitude: Double,
    
    longitude: Double,
    
    @required
    locationType: LocationType,
    
    @required
    createdAt: String,
    
    @required
    updatedAt: String,
    
    @required
    status: String
}

structure UpdateLocationRequest {
    @httpLabel
    @required
    locationId: String,
    
    @httpPayload
    body: UpdateLocationRequestContent
}

structure UpdateLocationRequestContent {
    countryId: String,
    regionId: String,
    cityId: String,
    neighborhoodId: String,
    address: String,
    postalCode: String,
    latitude: Double,
    longitude: Double,
    locationType: LocationType
}

structure UpdateLocationResponse {
    @httpPayload
    body: UpdateLocationResponseContent
}

structure UpdateLocationResponseContent {
    @required
    locationId: String,
    
    @required
    userId: String,
    
    @required
    country: CountryInfo,
    
    @required
    region: RegionInfo,
    
    @required
    city: CityInfo,
    
    neighborhood: NeighborhoodInfo,
    
    @required
    address: String,
    
    postalCode: String,
    
    latitude: Double,
    
    longitude: Double,
    
    @required
    locationType: LocationType,
    
    @required
    updatedAt: String,
    
    @required
    status: String
}

structure DeleteLocationRequest {
    @httpLabel
    @required
    locationId: String
}

structure DeleteLocationResponse {
    @httpPayload
    body: DeleteLocationResponseContent
}

structure DeleteLocationResponseContent {
    @required
    deleted: Boolean,
    
    @required
    message: String
}

structure ListLocationsRequest {
    @httpQuery("page")
    page: Integer,
    
    @httpQuery("size")
    size: Integer,
    
    @httpQuery("userId")
    userId: String,
    
    @httpQuery("locationType")
    locationType: LocationType
}

structure ListLocationsResponse {
    @httpPayload
    body: ListLocationsResponseContent
}

structure ListLocationsResponseContent {
    @required
    locations: LocationList,
    
    @required
    page: Integer,
    
    @required
    size: Integer,
    
    @required
    total: Integer,
    
    @required
    totalPages: Integer
}

// Geographic Data Structures
structure GetCountriesRequest {
    @httpQuery("search")
    search: String
}

structure GetCountriesResponse {
    @httpPayload
    body: GetCountriesResponseContent
}

structure GetCountriesResponseContent {
    @required
    countries: CountryList
}

structure GetRegionsByCountryRequest {
    @httpLabel
    @required
    countryId: String
}

structure GetRegionsByCountryResponse {
    @httpPayload
    body: GetRegionsByCountryResponseContent
}

structure GetRegionsByCountryResponseContent {
    @required
    regions: RegionList
}

structure GetCitiesByRegionRequest {
    @httpLabel
    @required
    regionId: String
}

structure GetCitiesByRegionResponse {
    @httpPayload
    body: GetCitiesByRegionResponseContent
}

structure GetCitiesByRegionResponseContent {
    @required
    cities: CityList
}

structure GetNeighborhoodsByCityRequest {
    @httpLabel
    @required
    cityId: String
}

structure GetNeighborhoodsByCityResponse {
    @httpPayload
    body: GetNeighborhoodsByCityResponseContent
}

structure GetNeighborhoodsByCityResponseContent {
    @required
    neighborhoods: NeighborhoodList
}

// Common Structures
structure LocationResponse {
    @required
    locationId: String,
    
    @required
    userId: String,
    
    @required
    country: CountryInfo,
    
    @required
    region: RegionInfo,
    
    @required
    city: CityInfo,
    
    neighborhood: NeighborhoodInfo,
    
    @required
    address: String,
    
    postalCode: String,
    
    latitude: Double,
    
    longitude: Double,
    
    @required
    locationType: LocationType,
    
    @required
    status: String
}

structure CountryInfo {
    @required
    countryId: String,
    
    @required
    name: String,
    
    @required
    code: String,
    
    @required
    status: String,
    
    @required
    createdAt: String,
    
    @required
    updatedAt: String
}

structure RegionInfo {
    @required
    regionId: String,
    
    @required
    name: String,
    
    @required
    code: String,
    
    @required
    countryId: String,
    
    @required
    status: String,
    
    @required
    createdAt: String,
    
    @required
    updatedAt: String
}

structure CityInfo {
    @required
    cityId: String,
    
    @required
    name: String,
    
    @required
    regionId: String,
    
    @required
    status: String,
    
    @required
    createdAt: String,
    
    @required
    updatedAt: String
}

structure NeighborhoodInfo {
    @required
    neighborhoodId: String,
    
    @required
    name: String,
    
    @required
    cityId: String,
    
    @required
    status: String,
    
    @required
    createdAt: String,
    
    @required
    updatedAt: String
}

structure CountryResponse {
    @required
    countryId: String,
    
    @required
    name: String,
    
    @required
    code: String,
    
    @required
    status: String,
    
    @required
    createdAt: String,
    
    @required
    updatedAt: String
}

structure RegionResponse {
    @required
    regionId: String,
    
    @required
    name: String,
    
    @required
    code: String,
    
    @required
    countryId: String,
    
    @required
    status: String,
    
    @required
    createdAt: String,
    
    @required
    updatedAt: String
}

structure CityResponse {
    @required
    cityId: String,
    
    @required
    name: String,
    
    @required
    regionId: String,
    
    @required
    status: String,
    
    @required
    createdAt: String,
    
    @required
    updatedAt: String
}

structure NeighborhoodResponse {
    @required
    neighborhoodId: String,
    
    @required
    name: String,
    
    @required
    cityId: String,
    
    @required
    status: String,
    
    @required
    createdAt: String,
    
    @required
    updatedAt: String
}

// Lists
list LocationList {
    member: LocationResponse
}

list CountryList {
    member: CountryResponse
}

list RegionList {
    member: RegionResponse
}

list CityList {
    member: CityResponse
}

list NeighborhoodList {
    member: NeighborhoodResponse
}

// Enums
enum LocationType {
    HOME = "HOME",
    WORK = "WORK",
    BILLING = "BILLING",
    SHIPPING = "SHIPPING",
    OTHER = "OTHER"
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