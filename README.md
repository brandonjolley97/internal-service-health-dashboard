# Internal Service Health Dashboard

This project is a lightweight dashboard for monitoring and managing the status of background services.  

It includes:
- A FastAPI backend
- A React + Vite frontend 
- A Postgres database
- Automated seeding of example services on first startup
- Backend and frontend tests

The application can be started with a single command using Docker Compose.

## Structure and Design Notes
The backend is built with FastAPI and SQLAlchemy.  It separates models, schemas, CRUD logic, and routes to maintain a clear separation of concerns.  Service status rules are enforced server-side to ensure correctness regardless of client behavior.  Alembic is used for database migrations.  On startup, the backend seeds a small set of example services if none exist.  Seeding will not create duplicate services on restart.

The frontend is built using React, TypeScript, and Vite.  Tailwind CSS is used for styling.  The UI reflects backend business rules.  All API interactions are centralized on a small client helper module to avoid duplication and maintain type safety.

Docker Compose is used to containerize the frontend, backend, and database.  This allows the application to be run without installing Python or Node locally.

## Running the App
This project requires Docker and Docker Compose.  From the repository root, run: ```docker compose up --build```  

Once running, you can access the:
- Frontend at http://localhost:5173/
- Backend API docs at http://localhost:8000/docs 

## Testing
To run backend tests, go to the backend directory and run: ```poetry run pytest```.  These tests validate service status transition rules and service naming constraints.

To run frontend tests, go to the frontend directory and run: ```npm test```.  These tests verify a UI component called StatusBadge renders the correct visual state for each service status.

## AI Review
I used AI tools to assist with unfamiliar parts of the stack and explore implementation approaches.  Generated suggestions were reviewed and adapted as needed.  In one case, an import recommendation caused a circular dependency, which was corrected by restructuring the module imports.