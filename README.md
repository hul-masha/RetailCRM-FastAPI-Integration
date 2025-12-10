# RetailCRM FastAPI Integration

Microservice for integration with RetailCRM API via FastAPI.

## 📋 Requirements

- Python 3.11+
- Docker & Docker Compose
- RetailCRM API key

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone git@github.com:hul-masha/RetailCRM-FastAPI-Integration.git
cd retailcrm-fastapi
```
### 2. Configure environment variables
```bash
cp .env.example .env
```
#### Edit the .env file:
```bash
RETAILCRM_API_URL=https://your-domain.retailcrm.ru
RETAILCRM_API_KEY=your_api_key_here
```
### 3. Run with Docker Compose
```bash
docker-compose up -d --build
```
#### The application will be available at: http://localhost:8000
### 4. Verify the installation
```bash
curl http://localhost:8000/health
```
## 📚 API Documentation
### After launching, documentation is available at:
#### Swagger UI: http://localhost:8000/docs
