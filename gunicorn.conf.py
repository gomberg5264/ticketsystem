import multiprocessing

# Server Socket
# Use Heroku's PORT environment variable if set, otherwise default to 8000 for local development
bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"

# Workers and Threads
workers = multiprocessing.cpu_count() * 2 + 1  # number of worker processes
threads = 2  # number of threads per worker

# Security
timeout = 120  # timeout in seconds
keepalive = 5  # keeps the connection alive for 5 seconds

# Logging
loglevel = "info"  # log level: debug, info, warning, error, critical
accesslog = "-"  # access log - "-" means log to stdout
errorlog = "-"  # error log - "-" means log to stderr

# Environment Variables
raw_env = [
    "FLASK_ENV=production",
    "DATABASE_URL=your_database_url_here"
]

# Forwarded allow ips
forwarded_allow_ips = '*'