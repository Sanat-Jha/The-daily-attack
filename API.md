I'll update the API.md file to provide detailed documentation that matches the API endpoints we've implemented. This will include all the endpoints, authentication requirements, and example requests/responses.

```markdown:c:\Users\sanat\Desktop\The daily attack\API.md
# The Daily Attack API Documentation

## Introduction

The Daily Attack API provides programmatic access to blog posts and allows authorized users to create new posts. This documentation describes the available endpoints and how to use them.

## Authentication

Some endpoints require authentication using an API key. To authenticate, include your API key in the request headers:

```
X-API-Key: your-api-key
```

You can generate an API key from your dashboard if you have an editor account.

## Endpoints

### List All Posts

**URL:** `/api/posts/`

**Method:** GET

**Authentication:** None (public endpoint)

**Description:** Returns a list of all published posts.

**Example Request:**
```bash
curl -X GET http://yourdomain.com/api/posts/
```

**Example Response:**
```json
[
  {
    "id": 1,
    "title": "Sample Post",
    "content": "This is a sample post content.",
    "status": "published",
    "created_at": "2023-06-01T12:00:00Z",
    "published_at": "2023-06-01T14:00:00Z",
    "author": "username",
    "tags": [
      {"name": "sample"},
      {"name": "example"}
    ]
  },
  {
    "id": 2,
    "title": "Another Post",
    "content": "Content of another post.",
    "status": "published",
    "created_at": "2023-06-02T10:00:00Z",
    "published_at": "2023-06-02T11:00:00Z",
    "author": "username",
    "tags": [
      {"name": "example"}
    ]
  }
]
```

### Get a Specific Post

**URL:** `/api/posts/{id}/`

**Method:** GET

**Authentication:** None (public endpoint)

**Description:** Returns details of a specific published post.

**Example Request:**
```bash
curl -X GET http://yourdomain.com/api/posts/1/
```

**Example Response:**
```json
{
  "id": 1,
  "title": "Sample Post",
  "content": "This is a sample post content.",
  "status": "published",
  "created_at": "2023-06-01T12:00:00Z",
  "published_at": "2023-06-01T14:00:00Z",
  "author": "username",
  "tags": [
    {"name": "sample"},
    {"name": "example"}
  ]
}
```

### Create a New Post

**URL:** `/api/posts/create/`

**Method:** POST

**Authentication:** Required (API Key)

**Description:** Creates a new blog post.

**Request Headers:**
```
Content-Type: application/json
X-API-Key: your-api-key
```

**Request Body:**
```json
{
  "title": "New Post Title",
  "content": "Content of the new post",
  "status": "draft", 
  "tags": ["tag1", "tag2"]
}
```

Note: `status` can be either "draft" or "published". If omitted, it defaults to "draft".

**Example Request:**
```bash
curl -X POST http://yourdomain.com/api/posts/create/ \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "title": "New Post Title",
    "content": "Content of the new post",
    "status": "draft",
    "tags": ["tag1", "tag2"]
  }'
```

**Example Response:**
```json
{
  "id": 3,
  "title": "New Post Title",
  "content": "Content of the new post",
  "status": "draft",
  "created_at": "2023-06-03T10:00:00Z",
  "published_at": null,
  "author": "username",
  "tags": [
    {"name": "tag1"},
    {"name": "tag2"}
  ]
}
```



I'll add details about the search endpoint to the API.md file. Let me update it for you:

```markdown:c:\Users\sanat\Desktop\The daily attack\API.md
# The Daily Attack API Documentation

## Introduction

The Daily Attack API provides programmatic access to blog posts and allows authorized users to create new posts. This documentation describes the available endpoints and how to use them.

## Authentication

Some endpoints require authentication using an API key. To authenticate, include your API key in the request headers:

```
X-API-Key: your-api-key
```

You can generate an API key from your dashboard if you have an editor account.

## Endpoints

### List All Posts

**URL:** `/api/posts/`

**Method:** GET

**Authentication:** None (public endpoint)

**Description:** Returns a list of all published posts.

**Example Request:**
```bash
curl -X GET http://yourdomain.com/api/posts/
```

**Example Response:**
```json
[
  {
    "id": 1,
    "title": "Sample Post",
    "content": "This is a sample post content.",
    "status": "published",
    "created_at": "2023-06-01T12:00:00Z",
    "published_at": "2023-06-01T14:00:00Z",
    "author": "username",
    "tags": [
      {"name": "sample"},
      {"name": "example"}
    ]
  },
  {
    "id": 2,
    "title": "Another Post",
    "content": "Content of another post.",
    "status": "published",
    "created_at": "2023-06-02T10:00:00Z",
    "published_at": "2023-06-02T11:00:00Z",
    "author": "username",
    "tags": [
      {"name": "example"}
    ]
  }
]
```

### Search Posts

**URL:** `/api/posts/search/`

**Method:** GET

**Authentication:** None (public endpoint)

**Description:** Returns a list of published posts matching the search query.

**Parameters:**
- `q` (required): The search query string

**Example Request:**
```bash
curl -X GET "http://yourdomain.com/api/posts/search/?q=example"
```

**Example Response:**
```json
[
  {
    "id": 1,
    "title": "Sample Post",
    "content": "This is a sample post content with example.",
    "status": "published",
    "created_at": "2023-06-01T12:00:00Z",
    "published_at": "2023-06-01T14:00:00Z",
    "author": "username",
    "tags": [
      {"name": "sample"},
      {"name": "example"}
    ]
  },
  {
    "id": 2,
    "title": "Another Example Post",
    "content": "Content of another post.",
    "status": "published",
    "created_at": "2023-06-02T10:00:00Z",
    "published_at": "2023-06-02T11:00:00Z",
    "author": "username",
    "tags": [
      {"name": "example"}
    ]
  }
]
```
