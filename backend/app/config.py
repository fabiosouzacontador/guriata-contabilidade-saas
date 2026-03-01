import os

# Environment Variables Configuration

# Database URL
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///default.db')

# JWT Settings
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
JWT_EXPIRATION_DELTA = os.getenv('JWT_EXPIRATION_DELTA', 3600)  # in seconds

# Google OAuth Configuration
GOOGLE_OAUTH_CLIENT_ID = os.getenv('GOOGLE_OAUTH_CLIENT_ID', 'your_google_client_id')
GOOGLE_OAUTH_CLIENT_SECRET = os.getenv('GOOGLE_OAUTH_CLIENT_SECRET', 'your_google_client_secret')
