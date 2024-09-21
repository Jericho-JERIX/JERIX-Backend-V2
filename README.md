## Install

```
# Build the image
docker build -t jerix-backend:latest .

# Run the container with auto-restart
docker run -d --restart=always --name jerix-backend-container -p 8000:8000 jerix-backend:latest --env-file ./.env
```