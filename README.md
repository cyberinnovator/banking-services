# Banking System

A full-stack banking application with microservices architecture, containerized with Docker and deployed on Kubernetes using Minikube.

## Architecture

### Backend Services
- **Accounts Service** (Port 5001): Customer and account management
- **Loans Service** (Port 5002): Loan applications and management  
- **Transactions Service** (Port 5003): Deposit, withdrawal, and transfer operations

### Frontend
- **React SPA** with Vite, Tailwind CSS, and React Router
- Containerized with Nginx for production deployment
- Vite proxy configuration for local development

### Infrastructure
- **MySQL Database**: Centralized data storage
- **Kubernetes**: Container orchestration via Minikube
- **Helm Charts**: Package management and deployment
- **Nginx Ingress**: API routing and load balancing

## Quick Start

### Prerequisites
- Docker
- Minikube
- Helm
- Node.js 18+ (for frontend development)

### 1. Start Minikube
```bash
minikube start
eval $(minikube docker-env)  # Use Minikube's Docker daemon
```

### 2. Deploy Backend Services
```bash
# Deploy MySQL
helm install mysql-service mysql

# Deploy banking services
helm install banking-system ./banking-system
```

### 3. Setup Database
```bash
# Run database setup
python scripts/setup_database.py

# Seed with sample data
mysql -h $(minikube service mysql-service --url | cut -d'/' -f3) -u root -p banking_system < scripts/seed.sql
```

### 4. Configure Host Mapping
Add to `/etc/hosts`:
```
$(minikube ip) banking-service
```

### 5. Frontend Development
```bash
cd frontend-services
npm install
npm run dev
```

Visit: http://localhost:5173

## API Endpoints

### Accounts
- `GET /api/accounts` - List all accounts
- `POST /api/accounts` - Create new account
- `GET /api/accounts/{id}` - Get account details
- `PUT /api/accounts/{id}` - Update account
- `DELETE /api/accounts/{id}` - Delete account
- `GET /api/customers` - List customers

### Loans
- `GET /api/loans` - List all loans
- `POST /api/loans` - Apply for loan
- `GET /api/loans/{id}` - Get loan details
- `PUT /api/loans/{id}/approve` - Approve loan

### Transactions
- `GET /api/transactions` - List all transactions
- `POST /api/transactions/deposit` - Deposit money
- `POST /api/transactions/withdraw` - Withdraw money
- `POST /api/transactions/transfer` - Transfer between accounts

## Development

### Backend Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run individual services
python app.py  # All services on port 5000
```

### Frontend Development
```bash
cd frontend-services
npm install
npm run dev     # Development server
npm run build   # Production build
```

### Database Management
```bash
# Connect to MySQL
mysql -h $(minikube service mysql-service --url | cut -d'/' -f3) -u root -p

# Run migrations
python scripts/setup_database.py
```

## Deployment

### Build Images
```bash
# Backend services
docker build -t your-registry/accounts-service:latest -f Dockerfile.accounts .
docker build -t your-registry/loans-service:latest -f Dockerfile.loans .
docker build -t your-registry/transactions-service:latest -f Dockerfile.transactions .

# Frontend
docker build -t your-registry/frontend:latest -f frontend-services/Dockerfile frontend-services/
```

### Helm Deployment
```bash
# Update values.yaml with your image registry
helm upgrade --install banking-system ./banking-system

# Update specific service
helm upgrade --install banking-system ./banking-system --set accountsService.tag=v2
```

## Project Structure

```
flask-banking-system/
├── frontend-services/          # React frontend
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── pages/             # Page components
│   │   └── App.jsx            # Main app component
│   ├── Dockerfile             # Frontend container
│   ├── nginx.conf             # Nginx configuration
│   └── vite.config.js         # Vite development config
├── banking-system/            # Helm chart
│   ├── templates/             # Kubernetes manifests
│   └── values.yaml            # Chart values
├── services/                  # Backend services
│   ├── accounts_service.py
│   ├── loans_service.py
│   └── transactions_service.py
├── models/                    # Data models
├── database/                  # Database connection
└── scripts/                   # Database setup scripts
```

## Troubleshooting

### Common Issues

1. **500 Error on /api/accounts**
   - Check database connectivity
   - Verify MySQL service is running
   - Check pod logs: `kubectl logs deploy/accounts-service-deployment`

2. **Frontend not connecting to backend**
   - Ensure `/etc/hosts` maps `banking-service` to Minikube IP
   - Check Ingress is working: `curl http://banking-service/api/accounts`

3. **Pods not updating after image rebuild**
   - Use `kubectl rollout restart deploy/service-name`
   - Or update image tag in Helm values

### Useful Commands
```bash
# Check pod status
kubectl get pods

# View logs
kubectl logs deploy/accounts-service-deployment

# Port forward for debugging
kubectl port-forward svc/accounts-service 5001:5001

# Check Ingress
kubectl get ingress banking-ingress
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request


