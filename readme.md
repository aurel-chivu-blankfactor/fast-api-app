
# **FastAPI User and Group Management API**

This is a FastAPI-based application that provides endpoints for managing users and groups, with a focus on asynchronous processing, clean architecture, and database interactions using SQLite.

## **Features**
- CRUD operations for **users** and **groups**.
- Asynchronous integration with the **GitHub API** to fetch URLs and populate user details.
- Background tasks for processing additional user data post-creation.
- SQLite database with relationships between users and groups (many-to-many).
- Clear separation of concerns between routers, services, and repository layers.

---

## **Project Structure**
```plaintext
app/
├── api/
│   └── v1/
│       ├── routers/
│       │   ├── group.py         # Routers for group endpoints
│       │   ├── user.py          # Routers for user endpoints
├── core/
│   ├── database.py              # Database connection and initialization
├── models/
│   ├── association_tables.py    # Association tables (e.g., user_group)
│   ├── group.py                 # Group SQLAlchemy model
│   ├── user.py                  # User SQLAlchemy model
├── repository/
│   ├── group.py                 # Database interactions for groups
│   ├── user.py                  # Database interactions for users
├── schemas/
│   ├── group.py                 # Pydantic schemas for groups
│   ├── user.py                  # Pydantic schemas for users
├── services/
│   ├── group.py                 # Business logic for groups
│   ├── user.py                  # Business logic for users
└── main.py                      # Entry point for the application
```

---

## **Setup and Installation**

### **Requirements**
- Python 3.10 or higher
- SQLite (bundled with Python)

### **Installation**
1. Clone the repository:
   ```bash
   git https://github.com/aurel-chivu-blankfactor/fast-api-app.git
   cd fast-api-app
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
---

## **Endpoints**

### **User Endpoints**
| Method | Endpoint                 | Description                          |
|--------|--------------------------|--------------------------------------|
| POST   | `/user/`                 | Create a new user                    |
| GET    | `/users/`                | Retrieve all users                   |
| GET    | `/user/{user_uuid}`      | Retrieve a user by UUID              |
| PATCH  | `/user/{user_uuid}`      | Update user details                  |
| DELETE | `/user/{user_uuid}`      | Delete a user                        |

### **Group Endpoints**
| Method | Endpoint                 | Description                          |
|--------|--------------------------|--------------------------------------|
| POST   | `/group/`                | Create a new group                   |
| GET    | `/groups/`               | Retrieve all groups                  |
| GET    | `/group/{group_uuid}`    | Retrieve a group by UUID             |
| PATCH  | `/group/{group_uuid}`    | Update group details                 |
| DELETE | `/group/{group_uuid}`    | Delete a group                       |

---

## **Key Features**

### **Asynchronous GitHub API Integration**
When a user is created, the application:
1. Adds the user to the database (without URLs).
2. Launches a background task to fetch URLs from the GitHub API.
3. Updates the user's `urls` field in the database with the GitHub response.

**Example GitHub Response**:
```json
{
  "current_user_url": "https://api.github.com/user",
  "current_user_authorizations_html_url": "https://github.com/settings/connections/applications{/client_id}",
  "authorizations_url": "https://api.github.com/authorizations",
  ...
}
```

### **Database Schema**
- **User Table**:
  - `uuid`: Primary key.
  - `name`: User's name.
  - `urls`: JSONB field populated with GitHub API data.
- **Group Table**:
  - `uuid`: Primary key.
  - `name`: Name of the group (`regular`, `admin`).
- **User-Group Association**:
  - Many-to-many relationship between users and groups.

---

## **Sample Requests**

### Create a User
**Request**:
```json
POST /user/
{
  "name": "John Doe",
  "group_uuid": "123e4567-e89b-12d3-a456-426614174000"
}
```

**Response**:
```json
{
  "uuid": "789e1234-e89b-45f6-98cd-426614174abc",
  "name": "John Doe",
  "urls": {},
  "groups": ["admin"]
}
```

---

### Retrieve All Users
**Request**:
```json
GET /users/
```

**Response**:
```json
[
  {
    "uuid": "789e1234-e89b-45f6-98cd-426614174abc",
    "name": "John Doe",
    "urls": {"current_user_url": "https://api.github.com/user"},
    "groups": ["admin"]
  }
]
```

---

## **Development Notes**
### **Best Practices Followed**
1. **Separation of Concerns**:
   - Repository: Handles direct database interactions.
   - Service: Contains business logic.
   - Router: Handles client-facing endpoints.

2. **Asynchronous Processing**:
   - Background tasks for non-blocking operations.

3. **Type Safety**:
   - Pydantic schemas enforce type validation for inputs and outputs.

4. **SQLite Compatibility**:
   - Utilizes SQLite's JSON field for `urls`.

---

## **Run the Application**
Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

Visit the interactive API documentation at:
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---
