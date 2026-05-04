### **Week 1: Core Infrastructure & Social Foundation**

#### **1. Cloud Deployment (EC2 & Infrastructure)**
* **Infrastructure Setup:** Provision an AWS EC2 instance and configure **AWS Systems Manager (SSM) Session Manager** to allow the team to manage the server without distributing SSH keys.
* **Database Migration:** Setup a **PostgreSQL** instance (via Docker or AWS RDS) to handle concurrent user writes safely.
* **Containerization:** Create a `Dockerfile` and `docker-compose.yml` to package the FastAPI app and Postgres database.
* **Environment Management:** Use `.env` files and `python-dotenv` to externalize database URLs and API keys.
* **CI/CD Pipeline:** Create a GitHub Action script to automate the deployment process (build and push image) on every `git push`.
* **Process Management:** Configure the app to run as a background service (using Docker's restart policy or `systemd`) so it persists after logging out of the EC2 instance.
* **Documentation:** Write a `DEPLOY.md` covering environment variables, setup commands, and troubleshooting.

#### **2. Post & User Profile Management**
*   **SQLModel Schema:** Define `Post` with `author_id` and `created_at` (indexed).
*   **Relationship Linking:** Map `User` to `Post` using SQLModel relationships for user profiles.
*   **API Endpoints:**
    *   `POST /posts` (Create Post)
    *   `GET /posts` (Global Feed)
    *   `GET /posts/{post_id}` (Fetch Single Post)
    *   `GET /users/{id}/posts` (User Profile Posts)
*   **Database CRUD Implementation:**
    *   `create_post(post_data, user_id)`: Insert new post.
    *   `get_posts(offset, limit)`: Fetch paginated list of all public posts.
    *   `get_post_by_id(post_id)`: Fetch a single record.
    *   `get_posts_by_user(user_id, offset, limit)`: Filter `Post` table by `author_id`.

#### **3. Server-Side Authentication (The Gatekeeper)**
*   **Security Models:** Update the `User` model to include a `hashed_password` field (using `passlib` for hashing).
*   **JWT Implementation:** Create a `POST /token` endpoint to exchange credentials for a JSON Web Token (OAuth2), and integrate a `get_current_user` dependency.
*   **Dependency Injection:** Create a `get_current_user` dependency to protect routes and identify the "Actor."
*   **Protected Routes:** Update user and post routes to require a valid token, and implement `GET /users/me` to verify session validity.
*   **Database CRUD Implementation:**
    *   `get_user_by_username(username)`: Required for credential verification.
    *   `update_user_last_login(user_id)`: Track session activity.

#### **4. Client-Side Authentication & Integration (CLI App)**
*   **CLI Logic:** Implement Login/Logout dialogs; save JWT to `.session_token`.
*   **API Module:** Update `client_api` to handle session headers automatically.
*   **Authenticated Requests:** Update all API calls to automatically include the `Authorization: Bearer <token>` header.
*   **Database CRUD Implementation:**
    *   `create_user(user_create_data)`: Handle registration (hashing password before insert).
    *   `get_user_me(user_id)`: Retrieve the profile of the current token holder.

#### **5. Following & The Personalized Feed**
*   **Social Schema:** Create `Follow` junction table (Compound Primary Key: `follower_id`, `followed_id`).
*   **API Endpoints:** Implement `POST /users/{id}/follow` and `DELETE /users/{id}/follow`.
*   **Calculated Responses:** Create a `UserDetail` Pydantic model that includes an `is_following` boolean to inform the CLI menu state.
*   **Feed Algorithm:** Implement `GET /posts/feed` which queries the database for posts specifically from authors the current user follows.
*   **Feed UI:** Create a dedicated "Home Feed" dialog in the console app using `Rich` tables to display the personalized content.
*   **Database CRUD Implementation:**
    *   `add_follow(follower_id, followed_id)`: Create relationship.
    *   `remove_follow(follower_id, followed_id)`: Delete relationship.
    *   `is_following(follower_id, followed_id)`: Boolean check for UI menu logic.
    *   `get_followed_posts(follower_id, offset, limit)`: The Feed Query — select posts where `author_id` is in the list of users followed by `follower_id`.



---

### **Week 2: Interaction & Content Lifecycle (Brief Overview)**

* **Commenting System:** Users can respond to posts. This requires a new `Comment` SQLModel linked to both a `User` and a `Post`.
* **Reaction System (Likes):** Implementation of "Like" functionality for both posts and comments using junction tables to prevent duplicate likes.
* **Content Management (CRUD):** Allowing users to edit their own posts/comments (Update) or remove them entirely (Delete).
* **Account Management:** Implementation of "Delete User," which must handle "cascading deletes" (deciding if a user's posts should disappear if their account is deleted).
* **Advanced UI Refinement:** Updating the CLI to handle nested data, such as displaying comments underneath a post when viewed in detail.