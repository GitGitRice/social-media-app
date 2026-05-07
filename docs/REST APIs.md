# REST APIs

| Method | Endpoint | Replaces / Purpose |
|---|---|---|
| POST | /api/token | Login (Keep separate for security). |
| GET | /api/users/me | Get my own profile |
| GET | /api/users | Discovery (Search). |
| GET | /api/users/\{id\} | All Profile views (Me, Others, Stats, Bio). |
| GET | /api/users/{\id\}/followers | Returns a list of users who follow the user|
| GET | /api/users/{\id\}/following | Returns a list of users who wom the user is following |
| POST | /api/users/\{id\}/follow | Follow/Unfollow toggle. |
| GET | /api/posts | Global, My Feed, and User History (using filters). |
| POST | /api/posts | Create Post. |
| GET | /api/posts/\{id\} | Post Details + Comments + Likes (Nested). |
| POST | /api/posts/\{id\}/comment | Add Comment. |
| POST | /api/posts/\{id\}/like | Like Toggle. |
