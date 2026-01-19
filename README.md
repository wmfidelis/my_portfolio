# Django Portfolio Project

A comprehensive portfolio website built with Django featuring a blog, todo list, weather app, and personal portfolio showcase.

## Features

- **Blog**: Full-featured blog with CRUD operations
- **Todo App**: Task management system with user authentication
- **Weather App**: Real-time weather data using OpenWeatherMap API
- **Portfolio Site**: Personal portfolio with projects showcase and contact form
- **User Authentication**: Secure login, registration, and password reset
- **PostgreSQL Database**: Production-ready database
- **Redis Caching**: Improved performance with Redis cache
- **Bootstrap 5**: Modern, responsive UI

## Tech Stack

- Django 5.0
- PostgreSQL
- Redis (caching)
- Bootstrap 5
- Gunicorn
- WhiteNoise (static files)
- Heroku (deployment)

## Local Setup

### Prerequisites

- Python 3.11+
- PostgreSQL
- Redis (optional, for caching)

### Installation Steps

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd my_portfolio
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create PostgreSQL database**
```bash
psql -U postgres
CREATE DATABASE portfolio_db;
\q
```

5. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your actual values
```

6. **Generate Django secret key**
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

7. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

8. **Create superuser**
```bash
python manage.py createsuperuser
```

9. **Collect static files**
```bash
python manage.py collectstatic
```

10. **Run development server**
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`

## Environment Variables

Create a `.env` file with the following variables:

```
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=portfolio_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

OPENWEATHER_API_KEY=your-openweather-api-key
REDIS_URL=redis://127.0.0.1:6379/1

EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## Getting API Keys

### OpenWeatherMap API
1. Visit [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Generate an API key
4. Add to `.env` file

## Heroku Deployment

### Prerequisites
- Heroku CLI installed
- Git repository initialized

### Deployment Steps

1. **Login to Heroku**
```bash
heroku login
```

2. **Create Heroku app**
```bash
heroku create your-app-name
```

3. **Add PostgreSQL addon**
```bash
heroku addons:create heroku-postgresql:essential-0
```

4. **Add Redis addon (optional)**
```bash
heroku addons:create heroku-redis:mini
```

5. **Set environment variables**
```bash
heroku config:set SECRET_KEY='your-secret-key'
heroku config:set DEBUG=False
heroku config:set OPENWEATHER_API_KEY='your-api-key'
heroku config:set EMAIL_HOST_USER='your-email'
heroku config:set EMAIL_HOST_PASSWORD='your-password'
```

6. **Deploy to Heroku**
```bash
git add .
git commit -m "Initial commit"
git push heroku main
```

7. **Run migrations on Heroku**
```bash
heroku run python manage.py migrate
```

8. **Create superuser on Heroku**
```bash
heroku run python manage.py createsuperuser
```

9. **Open your app**
```bash
heroku open
```

## Project Structure

```
my_portfolio/
├── apps/
│   ├── blog/           # Blog application
│   ├── todo/           # Todo application
│   ├── weather/        # Weather API integration
│   └── portfolio_site/ # Main portfolio site
├── my_portfolio/       # Project settings
├── static/             # Static files (CSS, JS, images)
├── media/              # User uploads
├── templates/          # Global templates
├── requirements.txt    # Python dependencies
├── Procfile           # Heroku process file
├── runtime.txt        # Python version
└── manage.py          # Django management script
```

## Usage

### Admin Panel
Access the admin panel at `/admin/` with your superuser credentials.

### Blog
- Create, edit, and delete blog posts
- Comment on posts (authenticated users)
- Category and tag filtering

### Todo
- Create and manage tasks
- Mark tasks as complete
- Filter by status

### Weather
- Search weather by city
- View current conditions and forecast

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License

## Support

For issues and questions, please open an issue on GitHub.