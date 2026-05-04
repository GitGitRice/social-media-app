This is a comprehensive roadmap that transitions your project from a local prototype to a multi-user, cloud-hosted social application. Below is the breakdown of implementation tasks for Week 1 and a summary of the advanced social features for Week 2.

### **Week 1: Core Infrastructure & Social Foundation**

#### **1. Cloud Deployment (EC2 & Infrastructure)**
* **Infrastructure Setup:** Provision an AWS EC2 instance and configure **AWS Systems Manager (SSM) Session Manager** to allow the team to manage the server without distributing SSH keys.
* **Database Migration:** Setup a **PostgreSQL** instance (via Docker or AWS RDS) to handle concurrent user writes safely.
* **Containerization:** Create a `Dockerfile` and `docker-compose.yml` to package the FastAPI app and Postgres database.
* **Environment Management:** Use `.env` files and `python-dotenv` to externalize database URLs and API keys.
* **CI/CD Pipeline:** Create a GitHub Action script to automate the deployment process (build and push image) on every `git push`.
* **Process Management:** Configure the app to run as a background service (using Docker's restart policy or `systemd`) so it persists after logging out of the EC2 instance.
* **Documentation:** Write a `DEPLOY.md` covering environment variables, setup commands, and troubleshooting.

#### **2. Post Management & Relationship Mapping**
* **SQLModel Schema:** Define the `Post` model with an `author_id` foreign key and an index on `created_at`.
* **Relationship Linking:** Use SQLModel `Relationship` attributes to link `User` and `Post` objects for easier server-side browsing.
* **API Endpoints:** Implement `POST /posts` (Create) and `GET /posts` (Global list).

#### **3. Server-Side Authentication (The Gatekeeper)**
* **Security Models:** Update the `User` model to include a `hashed_password` field (using `passlib` for hashing).
* **JWT Implementation:** Create a `POST /token` endpoint to exchange credentials for a JSON Web Token.
* **Dependency Injection:** Create a `get_current_user` dependency to protect routes and identify the "Actor."
* **Protected Routes:** Update user and post routes to require a valid token, and implement `GET /users/me` to verify session validity.

#### **4. Client-Side Integration (CLI App)**
* **Session Management:** Update the `client_api` module to store the JWT in a local `.session_token` file.
* **Auth Flow:** Implement `questionary` dialogs for Login and Logout in the main menu.
* **Authenticated Requests:** Update all API calls to automatically include the `Authorization: Bearer <token>` header.

#### **5. Following & The Personalized Feed**
* **Social Database Logic:** Create the `Follow` junction table with a **Compound Primary Key** (`follower_id`, `followed_id`).
* **Social API:** Implement `POST /users/{id}/follow` and `DELETE /users/{id}/follow`.
* **Calculated Responses:** Create a `UserDetail` Pydantic model that includes an `is_following` boolean to inform the CLI menu state.
* **Feed Algorithm:** Implement `GET /posts/feed` which queries the database for posts specifically from authors the current user follows.
* **Feed UI:** Create a dedicated "Home Feed" dialog in the console app using `Rich` tables to display the personalized content.



---

### **Week 2: Interaction & Content Lifecycle (Brief Overview)**

* **Commenting System:** Users can respond to posts. This requires a new `Comment` SQLModel linked to both a `User` and a `Post`.
* **Reaction System (Likes):** Implementation of "Like" functionality for both posts and comments using junction tables to prevent duplicate likes.
* **Content Management (CRUD):** Allowing users to edit their own posts/comments (Update) or remove them entirely (Delete).
* **Account Management:** Implementation of "Delete User," which must handle "cascading deletes" (deciding if a user's posts should disappear if their account is deleted).
* **Advanced UI Refinement:** Updating the CLI to handle nested data, such as displaying comments underneath a post when viewed in detail.



### **Why this order works:**
By finishing the **Deployment** and **Authentication** in Week 1, your team will have a "live" environment where everyone can register accounts and follow each other immediately. Week 2 then focuses purely on making the content more interactive and manageable.