### Part 1.
1. Create FastAPI base project
2. Create User model (id, name, age(min=0, max=100), email)
3. Create Game model (id, name)
4. Create Endpoints:
	- Get games (get list of all games and users who connected to these games)
	- Get me (get info about current user and info about all connected games)
	- Connect to game. When user send this request. Need to create one obj like User - Game.

### Part 2 (Advanced).
1. Use SQLAlchemy for store your models
2. Use docker for run your code


Run:  `docker-compose up -d`

Link:  `http://0.0.0.0:8000/`
