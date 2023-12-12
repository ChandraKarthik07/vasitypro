# gunicorn_config.py
bind = "0.0.0.0:8002"  # Replace with your desired host and port
workers = 2  # You can adjust this based on your server's capabilities
threads = 3  # You can also adjust this based on your server's capabilities
worker_class = "sync"  # You can experiment with other worker classes
reload = True
