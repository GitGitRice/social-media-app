# REST APIs

| Method | Endpoint | Replaces / Purpose |
|---|---|---|
| POST | /auth/token | Login (Keep separate for security). |
| GET | /users | Discovery (Search). |
| GET | /users/\{id\} | All Profile views (Me, Others, Stats, Bio). |
| POST | /users/\{id\}/follow | Follow/Unfollow toggle. |
| GET | /posts | Global, My Feed, and User History (using filters). |
| POST | /posts | Create Post. |
| GET | /posts/\{id\} | Post Details + Comments + Likes (Nested). |
| POST | /posts/\{id\}/comment | Add Comment. |
| POST | /posts/\{id\}/like | Like Toggle. |