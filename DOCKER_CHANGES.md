# Database Fix Summary

I updated the `docker-compose.yml` file to fix the database startup error. Here is a simple breakdown of the changes:

What was fixed?
The database wouldn't start because the latest version of Postgres (v18+) changed how it handles files.

The 2 Simple Changes:
1. I changed the database storage folder from `/var/lib/postgresql/data` to just `/var/lib/postgresql`.
2. I removed the lines that were trying to share the Postgres program files (the "binaries") from my computer into the containers. This prevents "missing file" errors and ensures that both the Database and pgAdmin run smoothly without crashing.