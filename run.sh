 #!/bin/bash
 python src/db.py
 gunicorn wsgi:app
