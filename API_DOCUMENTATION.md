# LegacyMap API Documentation

## Base URL
```
http://localhost:8000
```

## Endpoints

### 1. Upload and Analyze (Recommended)
**POST** `/upload-analyze`

Upload a ZIP file containing source code and get detailed analysis with function/class information.

#### Request
- **Content-Type:** multipart/form-data
- **Parameter:** `file` (required) - ZIP file containing source code

#### Example Request (cURL)
```bash
curl -X POST -F "file=@project.zip" http://localhost:8000/upload-analyze
```

#### Response (Success - 200)
```json
{
  "status": "success",
  "repo_id": "f3a2c1b9",
  "total_files": 12,
  "total_edges": 23,
  "total_loc": 3456,
  "nodes": {
    "services/auth.js": {
      "loc": 145,
      "imports": ["./db.js", "../utils/logger.js"],
      "imported_by": ["main.js", "api.js"],
      "imports_count": 2,
      "imported_by_count": 2,
      "risk": 9.5,
      "functions_classes": [
        {
          "name": "authenticate",
          "type": "function",
          "line_start": 15,
          "language": "javascript"
        }
      ]
    }
  },
  "edges": [
    {
      "source": "main.js",
      "target": "services/auth.js"
    }
  ],
  "top_10_risky": [
    {
      "file": "services/auth.js",
      "risk": 9.5,
      "loc": 145,
      "imported_by": 2,
      "imports": 2,
      "functions_classes": [...]
    }
  ]
}
```

#### Response (Error - 400)
```json
{
  "status": "error",
  "detail": "Please upload a ZIP file"
}
```

#### Response (Error - 500)
```json
{
  "status": "error",
  "detail": "Error details here"
}
```

---

### 2. Basic Upload
**POST** `/upload`

Simple file upload endpoint that returns dependency graph.

#### Request
- **Content-Type:** multipart/form-data
- **Parameter:** `file` (required) - ZIP file

#### Response (Success - 200)
```json
{
  "summary": {
    "total_files": 12,
    "total_loc": 3456,
    "top_5_risky": [
      {
        "path": "services/auth.js",
        "risk": 9.5,
        "loc": 145,
        "imported_by": 2
      }
    ]
  },
  "nodes": { ... },
  "edges": [ ... ],
  "components": [ ... ]
}
```

---

### 3. Get Function Details
**GET** `/function-details/{repo_id}/{file_path}/{function_name}`

Get detailed information about where a function is called and its dependencies.

#### Path Parameters
- `repo_id` (string) - Repository ID from upload response
- `file_path` (string) - URL-encoded file path (e.g., "services%2Fauth.js")
- `function_name` (string) - Function name to lookup

#### Example Request
```bash
curl http://localhost:8000/function-details/f3a2c1b9/services%2Fauth.js/authenticate
```

#### Response (Success - 200)
```json
{
  "status": "success",
  "function_name": "authenticate",
  "file": "services/auth.js",
  "call_sites_table": {
    "title": "Where \"authenticate\" is called",
    "columns": ["File", "Line Number", "Code"],
    "rows": [
      {
        "file": "main.js",
        "line": 42,
        "code": "const user = authenticate(token);"
      },
      {
        "file": "api.js",
        "line": 89,
        "code": "router.post('/login', authenticate);"
      }
    ],
    "count": 2
  },
  "dependencies_table": {
    "title": "What \"authenticate\" depends on",
    "columns": ["Dependency Name", "Line Number", "Code"],
    "rows": [
      {
        "name": "validateToken",
        "line": 18,
        "code": "const valid = validateToken(token);"
      },
      {
        "name": "checkPermissions",
        "line": 22,
        "code": "checkPermissions(user);"
      }
    ],
    "count": 2
  }
}
```

#### Response (Error - 404)
```json
{
  "status": "error",
  "detail": "Repository not found"
}
```

---

## Data Structures

### Node Object
Represents a source file with its metadata.

```json
{
  "path": "services/auth.js",
  "loc": 145,
  "imports": ["./db.js", "../utils/logger.js"],
  "imported_by": ["main.js", "api.js"],
  "imports_count": 2,
  "imported_by_count": 2,
  "risk": 9.5,
  "functions_classes": [
    {
      "name": "authenticate",
      "type": "function",
      "line_start": 15,
      "language": "javascript",
      "parent_class": null
    }
  ]
}
```

### Edge Object
Represents a dependency between two files.

```json
{
  "source": "main.js",
  "target": "services/auth.js"
}
```

### Risk Calculation
Risk score is calculated as:
```
risk = (loc / 10) + (imported_by_count * 3) + (imports_count * 2)
```

**Formula breakdown:**
- `loc / 10` - File complexity (LOC normalized)
- `imported_by_count * 3` - High coupling inbound (breaking this breaks many)
- `imports_count * 2` - High coupling outbound (tight dependencies)

**Example:**
```
File: services/auth.js
- Lines of code: 145 → 145/10 = 14.5
- Imported by 2 files → 2 * 3 = 6
- Imports 3 files → 3 * 2 = 6
- Total risk = 14.5 + 6 + 6 = 26.5
```

---

## Supported File Types

### Source Files
- JavaScript: `.js`, `.jsx`
- TypeScript: `.ts`, `.tsx`
- Python: `.py`

### Analysis Includes
- Function definitions and calls
- Class definitions and methods
- Import/require statements
- Dependency relationships
- Code metrics (LOC, complexity)

---

## Error Codes

| Code | Message | Meaning |
|------|---------|---------|
| 400 | Upload a zip file | File is not ZIP format |
| 404 | Repository not found | Repo ID not found in cache |
| 404 | File not found | File path doesn't exist |
| 500 | Error details | Server error (see details) |

---

## Rate Limiting

Currently no rate limiting. In production, recommend:
- Max 100 requests/minute per IP
- Max file size: 100MB
- Max execution time: 60 seconds

---

## CORS Headers

**Allowed Origins (Development):**
- `http://localhost:3000`
- `http://localhost:3001`
- `http://127.0.0.1:3000`
- `http://127.0.0.1:3001`

**Allowed Methods:** GET, POST, PUT, DELETE, OPTIONS

**Allowed Headers:** *

---

## Health Check

**Endpoint:** `GET /docs`

Check if API is running:
```bash
curl http://localhost:8000/docs
```

Response: Interactive API documentation (Swagger UI)

---

## Example Usage

### 1. Upload and Analyze
```bash
# Create test project
mkdir test_project
echo "function hello() { console.log('hi'); }" > test_project/app.js
zip -r test.zip test_project

# Upload
curl -X POST -F "file=@test.zip" http://localhost:8000/upload-analyze
```

### 2. Parse Response
```javascript
const response = await fetch('http://localhost:8000/upload-analyze', {
  method: 'POST',
  body: formData
});
const data = await response.json();
console.log(`Found ${data.total_files} files`);
console.log(`Total LOC: ${data.total_loc}`);
console.log(`Risky files:`, data.top_10_risky);
```

### 3. Get Function Details
```javascript
const repoId = data.repo_id;
const filePath = 'test_project/app.js';
const funcName = 'hello';

const response = await fetch(
  `http://localhost:8000/function-details/${repoId}/${encodeURIComponent(filePath)}/${funcName}`
);
const details = await response.json();
console.log(`Function called in:`, details.call_sites_table);
console.log(`Function depends on:`, details.dependencies_table);
```

---

## Best Practices

1. **File Organization:**
   - Keep uploads under 100MB
   - Exclude `node_modules`, `.git`, build folders
   - ZIP all source files together

2. **Analysis:**
   - First-time analysis takes longer (1-5 seconds for typical projects)
   - Caching happens in memory during session
   - Results expire when server restarts

3. **Error Handling:**
   - Always check `response.ok` before processing
   - Log `detail` field for debugging
   - Retry on 500 errors

4. **Performance:**
   - Batch queries when possible
   - Cache results on frontend
   - Use `/upload-analyze` for detailed info in one request

---

## Limitations

1. **Performance:** Analyzed projects should be < 100MB
2. **Memory:** Large projects may use significant memory
3. **Timeout:** Analysis must complete within session
4. **Storage:** Temporary files cleaned up after analysis
5. **Cache:** Function details cache expires after session

---

## Future Enhancements

- [ ] Database persistence
- [ ] Incremental analysis
- [ ] Visualization generation
- [ ] Export reports (PDF, HTML)
- [ ] Diff analysis between versions
- [ ] Complexity metrics (cyclomatic, cognitive)
- [ ] Dead code detection
- [ ] Security vulnerability scanning
