# Using and Maintaining API Documentation

This guide explains how to use, maintain, and update the Studio Caju API documentation.

## Running the Documentation Server

To start the documentation server locally:

```bash
# From the backend directory
python -m mkdocs serve -f mkdocs.yml
```

This will start a local server at http://127.0.0.1:8000 where you can view the documentation.

Alternatively, you can use the task command:

```bash
# From the backend directory
task docs-serve
```

## Building the Documentation

To build the documentation site for production:

```bash
# From the backend directory
python -m mkdocs build -f mkdocs.yml
```

Or use the task command:

```bash
# From the backend directory
task docs-build
```

This will create a `site` directory with the static documentation website.

## Adding New Documentation

1. Create a new Markdown file in the `docs` directory or a subdirectory
2. Add the new file to the navigation structure in `mkdocs.yml`
3. Follow the existing formatting and structure patterns

### Example: Adding a New API Endpoint

To document a new API endpoint:

1. Create a new Markdown file or add to an existing one
2. Follow this format for API endpoints:

```markdown
## Endpoint Name

**URL**: `/api/v1/resource`

**Method**: `GET`

**Auth required**: Yes/No

**Permissions required**: Admin/User/None

### Request

```json
{
  "property": "value"
}
```

### Response

```json
{
  "property": "value"
}
```

### Error Responses

* **400 Bad Request**: If the request is malformed
* **401 Unauthorized**: If authentication is required
* **403 Forbidden**: If the user doesn't have permission
* **404 Not Found**: If the resource doesn't exist
```

## Documenting Code with mkdocstrings

To document Python code, use the `mkdocstrings` plugin:

1. Write Google-style docstrings in your Python code
2. Reference the code in your documentation file:

```markdown
::: module.path.to.function
    options:
      show_source: true
```

## Maintaining Changelog

Keep the `changelog.md` file updated with all changes to the API. Use the following format:

1. Version or date section
2. Added, Changed, Deprecated, Removed, Fixed, and Security subsections
3. Brief description of each change 