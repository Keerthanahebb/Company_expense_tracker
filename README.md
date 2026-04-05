##  Run Project Using Docker

### 1. Clone Repository
git clone <your-repo>
cd EXPENSE-TRACKER

### 2. Create .env file
Add:
DATABASE_URL=your_supabase_url

### 3. Build Docker Image
docker build -t expense-app .

### 4. Run Container
docker run -p 8000:8000 --env-file .env expense-app

### 5. Open API
http://localhost:8000/docs
