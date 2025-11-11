"""
Simple Mock API Server using Flask
This mimics ReqRes.in API for testing purposes

Run with: python mock_api_server.py
API will be available at: http://localhost:5000
"""

from datetime import datetime

from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory database
USERS = {
    1: {
        "id": 1,
        "email": "user1@gmail.com",
        "first_name": "User1",
        "last_name": "One",
        "avatar": "https://reqres.in/img/faces/1-image.jpg",
    },
    2: {
        "id": 2,
        "email": "user2@gmail.com",
        "first_name": "User2",
        "last_name": "Two",
        "avatar": "https://reqres.in/img/faces/2-image.jpg",
    },
    3: {
        "id": 3,
        "email": "user3@gmail.com",
        "first_name": "User3",
        "last_name": "Three",
        "avatar": "https://reqres.in/img/faces/3-image.jpg",
    },
    4: {
        "id": 4,
        "email": "user4@gmail.com",
        "first_name": "User4",
        "last_name": "Four",
        "avatar": "https://reqres.in/img/faces/4-image.jpg",
    },
    5: {
        "id": 5,
        "email": "user5@gmail.com",
        "first_name": "User5",
        "last_name": "Five",
        "avatar": "https://reqres.in/img/faces/5-image.jpg",
    },
    6: {
        "id": 6,
        "email": "user6@gmail.com",
        "first_name": "User6",
        "last_name": "Six",
        "avatar": "https://reqres.in/img/faces/6-image.jpg",
    },
    7: {
        "id": 7,
        "email": "user7@gmail.com",
        "first_name": "User7",
        "last_name": "Seven",
        "avatar": "https://reqres.in/img/faces/7-image.jpg",
    },
    8: {
        "id": 8,
        "email": "user8@gmail.com",
        "first_name": "User8",
        "last_name": "Eight",
        "avatar": "https://reqres.in/img/faces/8-image.jpg",
    },
    9: {
        "id": 9,
        "email": "user9@gmail.com",
        "first_name": "User9",
        "last_name": "Nine",
        "avatar": "https://reqres.in/img/faces/9-image.jpg",
    },
    10: {
        "id": 10,
        "email": "user10@gmail.com",
        "first_name": "User10",
        "last_name": "Ten",
        "avatar": "https://reqres.in/img/faces/10-image.jpg",
    },
    11: {
        "id": 11,
        "email": "user11@gmail.com",
        "first_name": "User11",
        "last_name": "Eleven",
        "avatar": "https://reqres.in/img/faces/11-image.jpg",
    },
    12: {
        "id": 12,
        "email": "user12@gmail.com",
        "first_name": "User12",
        "last_name": "Twelve",
        "avatar": "https://reqres.in/img/faces/12-image.jpg",
    },
}

RESOURCES = {
    1: {
        "id": 1,
        "name": "resource1",
        "year": 2000,
        "color": "#98B2D1",
        "pantone_value": "15-4020",
    },
    2: {
        "id": 2,
        "name": "resource2",
        "year": 2001,
        "color": "#C74375",
        "pantone_value": "17-2031",
    },
    3: {
        "id": 3,
        "name": "resource3",
        "year": 2002,
        "color": "#BF1932",
        "pantone_value": "19-1664",
    },
    4: {
        "id": 4,
        "name": "resource4",
        "year": 2003,
        "color": "#7BC4C4",
        "pantone_value": "14-4811",
    },
    5: {
        "id": 5,
        "name": "resource5",
        "year": 2004,
        "color": "#E2583E",
        "pantone_value": "17-1456",
    },
    6: {
        "id": 6,
        "name": "resource6",
        "year": 2005,
        "color": "#53B0AE",
        "pantone_value": "15-5217",
    },
}

next_user_id = 13


# Helper function for pagination
def paginate(items_dict, page=1, per_page=6):
    items = list(items_dict.values())
    total = len(items)
    total_pages = (total + per_page - 1) // per_page

    start = (page - 1) * per_page
    end = start + per_page

    return {
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": total_pages,
        "data": items[start:end],
    }


# ========== USER ENDPOINTS ==========


@app.route("/api/users", methods=["GET"])
def get_users():
    """GET /api/users - Get list of users with pagination"""
    page = int(request.args.get("page", 1))
    delay = int(request.args.get("delay", 0))

    # Simulate delay if requested
    if delay > 0:
        import time

        time.sleep(delay)

    response = paginate(USERS, page=page)
    response["support"] = {
        "url": "https://reqres.in/#support-heading",
        "text": "Some text displayed!",
    }

    return jsonify(response), 200


@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """GET /api/users/{id} - Get single user"""
    user = USERS.get(user_id)

    if user:
        return (
            jsonify(
                {
                    "data": user,
                    "support": {
                        "url": "https://reqres.in/#support-heading",
                        "text": "Some text displayed!",
                    },
                }
            ),
            200,
        )
    else:
        return jsonify({}), 404


@app.route("/api/users", methods=["POST"])
def create_user():
    """POST /api/users - Create new user"""
    global next_user_id

    data = request.get_json()

    new_user = {
        "name": data.get("name"),
        "job": data.get("job"),
        "id": str(next_user_id),
        "createdAt": datetime.utcnow().isoformat() + "Z",
    }

    # Add to in-memory database
    USERS[next_user_id] = {
        "id": next_user_id,
        "email": data.get("email", f"user{next_user_id}@example.com"),
        "first_name": data.get("name", "Unknown").split()[0],
        "last_name": (
            data.get("name", "Unknown").split()[-1]
            if len(data.get("name", "").split()) > 1
            else ""
        ),
        "avatar": f"https://reqres.in/img/faces/{next_user_id}-image.jpg",
    }

    next_user_id += 1

    return jsonify(new_user), 201


@app.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    """PUT /api/users/{id} - Update user"""
    data = request.get_json()

    response = {
        "name": data.get("name"),
        "job": data.get("job"),
        "updatedAt": datetime.utcnow().isoformat() + "Z",
    }

    # Update in-memory database if user exists
    if user_id in USERS:
        USERS[user_id].update(
            {
                "first_name": data.get("name", "Unknown").split()[0],
                "last_name": (
                    data.get("name", "Unknown").split()[-1]
                    if len(data.get("name", "").split()) > 1
                    else ""
                ),
            }
        )

    return jsonify(response), 200


@app.route("/api/users/<int:user_id>", methods=["PATCH"])
def patch_user(user_id):
    """PATCH /api/users/{id} - Partially update user"""
    data = request.get_json()

    response = data.copy()
    response["updatedAt"] = datetime.utcnow().isoformat() + "Z"

    return jsonify(response), 200


@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """DELETE /api/users/{id} - Delete user"""
    # Remove from in-memory database
    if user_id in USERS:
        del USERS[user_id]

    return "", 204


# ========== RESOURCE ENDPOINTS ==========


@app.route("/api/unknown", methods=["GET"])
def get_resources():
    """GET /api/unknown - Get list of resources"""
    page = int(request.args.get("page", 1))
    response = paginate(RESOURCES, page=page)

    response["support"] = {
        "url": "https://reqres.in/#support-heading",
        "text": "Some text displayed!",
    }

    return jsonify(response), 200


@app.route("/api/unknown/<int:resource_id>", methods=["GET"])
def get_resource(resource_id):
    """GET /api/unknown/{id} - Get single resource"""
    resource = RESOURCES.get(resource_id)

    if resource:
        return (
            jsonify(
                {
                    "data": resource,
                    "support": {
                        "url": "https://reqres.in/#support-heading",
                        "text": "Some text displayed!",
                    },
                }
            ),
            200,
        )
    else:
        return jsonify({}), 404


# ========== AUTHENTICATION ENDPOINTS ==========


@app.route("/api/register", methods=["POST"])
def register():
    """POST /api/register - Register user"""
    data = request.get_json()

    if not data.get("email") or not data.get("password"):
        return jsonify({"error": "Missing email or password"}), 400

    # Only accept specific test emails
    valid_emails = ["eve.holt@reqres.in", "george.bluth@reqres.in"]

    if data.get("email") not in valid_emails:
        return jsonify({"error": "Note: Only defined users succeed registration"}), 400

    return jsonify({"id": 4, "token": "QpwL5tke4Pnpja7X4"}), 200


@app.route("/api/login", methods=["POST"])
def login():
    """POST /api/login - Login user"""
    data = request.get_json()

    if not data.get("email") or not data.get("password"):
        return jsonify({"error": "Missing email or password"}), 400

    # Accept any valid-looking email/password
    return jsonify({"token": "QpwL5tke4Pnpja7X4"}), 200


# ========== HEALTH CHECK ==========


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return (
        jsonify(
            {
                "status": "healthy",
                "message": "Mock API server is running",
                "total_users": len(USERS),
                "total_resources": len(RESOURCES),
            }
        ),
        200,
    )


@app.route("/", methods=["GET"])
def home():
    """Home page with API documentation"""
    return (
        jsonify(
            {
                "message": "Mock ReqRes API Server",
                "endpoints": {
                    "users": {
                        "GET /api/users": "List users (supports ?page=N and ?delay=N)",
                        "GET /api/users/{id}": "Get single user",
                        "POST /api/users": "Create user",
                        "PUT /api/users/{id}": "Update user",
                        "PATCH /api/users/{id}": "Partially update user",
                        "DELETE /api/users/{id}": "Delete user",
                    },
                    "resources": {
                        "GET /api/unknown": "List resources",
                        "GET /api/unknown/{id}": "Get single resource",
                    },
                    "auth": {
                        "POST /api/register": "Register (email + password required)",
                        "POST /api/login": "Login (email + password required)",
                    },
                    "health": {"GET /health": "Health check"},
                },
                "note": "This is a mock API for testing. All operations work without authentication.",
            }
        ),
        200,
    )


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🚀 Mock API Server Starting...")
    print("=" * 60)
    print("📍 Server running at: http://localhost:5000")
    print(f"📊 Total users: {len(USERS)}")
    print(f"📊 Total resources: {len(RESOURCES)}")
    print("\n📚 Available Endpoints:")
    print("   GET    http://localhost:5000/api/users")
    print("   GET    http://localhost:5000/api/users/{id}")
    print("   POST   http://localhost:5000/api/users")
    print("   PUT    http://localhost:5000/api/users/{id}")
    print("   PATCH  http://localhost:5000/api/users/{id}")
    print("   DELETE http://localhost:5000/api/users/{id}")
    print("   GET    http://localhost:5000/api/unknown")
    print("   POST   http://localhost:5000/api/register")
    print("   POST   http://localhost:5000/api/login")
    print("\n💡 Press Ctrl+C to stop the server")
    print("=" * 60 + "\n")

    app.run(debug=True, port=5000)
