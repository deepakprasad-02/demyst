FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

COPY entry.sh /entry.sh
RUN chmod +x /entry.sh

# Use the entrypoint script
ENTRYPOINT ["/entry.sh"]

# Default to running main.py if no argument is provided
CMD ["main"]


