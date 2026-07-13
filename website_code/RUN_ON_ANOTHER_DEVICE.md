# Run This Project on Another Device

This guide runs the project with:
- Backend: `new_3omda` (Express + MongoDB)
- Frontend dashboard: `newwwwwwwwww_3omda/gait-sentinel-main` (Vite + React)

## 1) Prerequisites

- Node.js `18+` (recommended: latest LTS)
- npm `9+`
- MongoDB (local) OR MongoDB Atlas URI
- A Gmail account with:
  - 2-Step Verification enabled
  - App Password generated (for OTP email sending)

## 2) Copy Project to New Device

Copy or clone this folder to the new machine:

`C:\Users\LOQ\Desktop\New folder (12)`

Required app folders:
- `new_3omda`
- `newwwwwwwwww_3omda\gait-sentinel-main`

## 3) Backend Setup (`new_3omda`)

Open terminal:

```powershell
cd "C:\Users\LOQ\Desktop\New folder (12)\new_3omda"
npm.cmd install
```

Create/update `.env` in `new_3omda` with valid values:

```env
PORT=5000
NODE_ENV=development
MOOD=DEV

MONGODB_URI=mongodb://127.0.0.1:27017/gait-recognition

ACCESS_TOKEN_SIGNATURE=replace_with_strong_random_secret_1
REFRESH_TOKEN_SIGNATURE=replace_with_strong_random_secret_2
ACCESS_TOKEN_EXPIRES_IN=1h
REFRESH_TOKEN_EXPIRES_IN=30d

EMAIL=your_real_gmail@gmail.com
APP_PASSWORD=your_16_char_google_app_password
EMAIL_FROM=your_real_gmail@gmail.com

CORS_ORIGIN=http://localhost:5173,http://127.0.0.1:5173
```

Notes:
- `APP_PASSWORD` is Google App Password, not Gmail normal password.
- If you use Atlas, replace `MONGODB_URI` with your Atlas connection string.

Run backend:

```powershell
npm.cmd run dev
```

Expected log:
- `DB connected successfully`
- `Example app listening on port 5000!`

If MongoDB is unavailable, the backend now exits immediately with a clear error instead of continuing in a broken state.

## 4) Frontend Setup (`gait-sentinel-main`)

Open another terminal:

```powershell
cd "C:\Users\LOQ\Desktop\New folder (12)\newwwwwwwwww_3omda\gait-sentinel-main"
npm.cmd install
```

Create `.env` (optional but recommended) in `gait-sentinel-main`:

```env
VITE_API_BASE_URL=http://localhost:5000/api
VITE_SERVER_BASE_URL=http://localhost:5000
```

Run frontend on fixed port:

```powershell
npm.cmd run dev -- --host --port 5173 --strictPort
```

Open:
- `http://localhost:5173`

## 5) Quick Health Checks

Backend health:

```powershell
curl http://localhost:5000/
```

Frontend:
- Open signup page: `http://localhost:5173/signup`
- Click `Test API Connection` (if button exists)

## 6) Verify Signup/Login Flow

1. Signup from frontend.
2. OTP should be sent to the configured Gmail inbox.
3. Confirm OTP on OTP screen.
4. Login with same email/password.
5. You should be redirected to dashboard and token stored in browser `localStorage`.

## 7) Common Issues and Fixes

### Port already in use

Kill running Node processes, then restart:

```powershell
Get-Process -Name node,npm -ErrorAction SilentlyContinue | Stop-Process -Force
```

### CORS error

- Ensure backend `.env` has:
  - `CORS_ORIGIN=http://localhost:5173,http://127.0.0.1:5173`
- Restart backend after `.env` changes.

### Gmail OTP error `535-5.7.8 BadCredentials`

- Make sure `EMAIL` is real Gmail.
- Make sure `APP_PASSWORD` is App Password from Google Account Security.
- Do not use normal Gmail password.

### MongoDB connection failure

- Start local MongoDB service, or
- Use valid `MONGODB_URI` from Atlas with correct user/password and network access.

Useful Windows checks:

```powershell
Get-Service | Where-Object { $_.Name -like "*mongo*" -or $_.DisplayName -like "*mongo*" }
Start-Service MongoDB
```

If `MongoDB` is not the exact service name on your machine, use the service name returned by the first command.

## 8) Production/Shared-Network Notes

- Replace localhost URLs with server IP/domain in:
  - Backend `CORS_ORIGIN`
  - Frontend `VITE_API_BASE_URL`, `VITE_SERVER_BASE_URL`
- Use HTTPS and strong secrets for token signatures.

## 9) Docker: Start All Apps Together

This repo now includes the Docker files below. You can use them directly or recreate them on another machine.

### 9.1 Create backend Dockerfile

File: `new_3omda/Dockerfile`

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
EXPOSE 5000
CMD ["npm", "run", "start"]
```

### 9.2 Create frontend Dockerfile

File: `newwwwwwwwww_3omda/gait-sentinel-main/Dockerfile`

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "--port", "5173", "--strictPort"]
```

### 9.3 Create docker compose

File: `docker-compose.yml` (at root: `New folder (12)`)

```yaml
version: "3.9"
services:
  mongo:
    image: mongo:7
    container_name: gait-mongo
    restart: unless-stopped
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

  backend:
    build:
      context: ./new_3omda
    container_name: gait-backend
    restart: unless-stopped
    env_file:
      - ./new_3omda/.env
    environment:
      - PORT=5000
      - MONGODB_URI=mongodb://mongo:27017/gait-recognition
      - CORS_ORIGIN=http://localhost:5173,http://127.0.0.1:5173
    depends_on:
      - mongo
    ports:
      - "5000:5000"

  frontend:
    build:
      context: ./newwwwwwwwww_3omda/gait-sentinel-main
    container_name: gait-frontend
    restart: unless-stopped
    environment:
      - VITE_API_BASE_URL=http://localhost:5000/api
      - VITE_SERVER_BASE_URL=http://localhost:5000
    depends_on:
      - backend
    ports:
      - "5173:5173"

volumes:
  mongo_data:
```

### 9.4 Start all services

From root folder:

```powershell
cd "C:\Users\LOQ\Desktop\New folder (12)"
docker compose up --build -d
```

Check status:

```powershell
docker compose ps
```

Open app:
- Frontend: `http://localhost:5173`
- Backend: `http://localhost:5000`

Stop all services:

```powershell
docker compose down
```

Stop and remove Mongo volume too:

```powershell
docker compose down -v
```
