#!/usr/bin/env python3
"""
Deployment Guide for Unified Service Management Portal
Covers local, Streamlit Cloud, and Docker deployments
"""

DEPLOYMENT_GUIDE = """
╔══════════════════════════════════════════════════════════════════════════╗
║                    DEPLOYMENT GUIDE                                     ║
║              Unified Service Management Portal                          ║
╚══════════════════════════════════════════════════════════════════════════╝

🚀 DEPLOYMENT OPTIONS:

1. Local Deployment (Development)
2. Streamlit Cloud (Easy Cloud Deployment)
3. Docker (Containerized)
4. Traditional Hosting (VPS/Server)
5. Heroku (PaaS)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 OPTION 1: LOCAL DEPLOYMENT (Development/Testing)
──────────────────────────────────────────────────────

Prerequisites:
  ✓ Python 3.8+
  ✓ pip
  ✓ Git

Steps:
  1. Clone repository
  2. Create virtual environment:
     python -m venv venv
     venv\\Scripts\\activate
  
  3. Install dependencies:
     pip install -r requirements.txt
  
  4. Initialize database:
     python init_app.py
  
  5. Run application:
     streamlit run app.py
  
  6. Access: http://localhost:8501

Performance:
  - Suitable for: Development, testing, small teams
  - Users: 1-10
  - Load: Low

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

☁️ OPTION 2: STREAMLIT CLOUD (Recommended for Easy Deployment)
─────────────────────────────────────────────────────────────────

Prerequisites:
  ✓ GitHub account with repository
  ✓ Streamlit account (free)

Steps:
  1. Push code to GitHub:
     git add .
     git commit -m "Ready for deployment"
     git push origin main
  
  2. Go to: https://share.streamlit.io
  
  3. Click "New app"
  
  4. Select:
     - Repository: your-repo
     - Branch: main
     - Main file path: app.py
  
  5. Click Deploy
  
  6. Get public URL and share

Configuration (Optional):
  Create .streamlit/config.toml:
  
  [server]
  port = 8501
  
  [logger]
  level = "info"

Performance:
  - Suitable for: Production, public access
  - Users: 1-10 concurrent
  - Cost: Free tier available

Limitations:
  - Database persists only during session
  - For persistent data, use external database (recommended)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🐳 OPTION 3: DOCKER DEPLOYMENT
───────────────────────────────

Prerequisites:
  ✓ Docker installed
  ✓ Docker Hub account (optional, for registry)

Step 1: Create Dockerfile
──────────────────────────

Create file named "Dockerfile":

  FROM python:3.9-slim
  
  WORKDIR /app
  
  COPY requirements.txt .
  RUN pip install --no-cache-dir -r requirements.txt
  
  COPY . .
  
  EXPOSE 8501
  
  CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

Step 2: Create .dockerignore
─────────────────────────────

  __pycache__
  *.pyc
  venv/
  .git/
  .env
  *.db

Step 3: Build and Run
─────────────────────

Build image:
  docker build -t service-portal:v1.0 .

Run container:
  docker run -p 8501:8501 \\
    -v $(pwd)/data:/app/data \\
    --name portal \\
    service-portal:v1.0

Access: http://localhost:8501

Stop container:
  docker stop portal

Remove container:
  docker rm portal

Push to Registry (Optional):
  docker tag service-portal:v1.0 yourusername/service-portal:v1.0
  docker push yourusername/service-portal:v1.0

Performance:
  - Suitable for: Production, scaling
  - Users: 10-100+
  - Deployment: Docker Swarm, Kubernetes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🖥️ OPTION 4: TRADITIONAL VPS/SERVER DEPLOYMENT
────────────────────────────────────────────────

Prerequisites:
  ✓ VPS/Server with Ubuntu/CentOS
  ✓ SSH access
  ✓ Domain name (optional)

Step 1: Connect to Server
──────────────────────────
  ssh user@your-server-ip

Step 2: Install Dependencies
──────────────────────────────
  sudo apt update
  sudo apt install python3-pip python3-venv nginx
  
  # For Ubuntu 20.04+
  sudo apt install python3.9

Step 3: Clone Repository
─────────────────────────
  cd /var/www
  git clone https://github.com/yourusername/portal.git
  cd portal

Step 4: Setup Python Environment
─────────────────────────────────
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt

Step 5: Create Systemd Service
───────────────────────────────
  sudo nano /etc/systemd/system/portal.service
  
  Add:
  [Unit]
  Description=Streamlit Portal
  After=network.target
  
  [Service]
  Type=simple
  User=www-data
  WorkingDirectory=/var/www/portal
  ExecStart=/var/www/portal/venv/bin/streamlit run app.py \\
    --server.port=8501 --server.address=localhost
  Restart=always
  
  [Install]
  WantedBy=multi-user.target

Step 6: Start Service
─────────────────────
  sudo systemctl daemon-reload
  sudo systemctl start portal
  sudo systemctl enable portal

Step 7: Configure Nginx Reverse Proxy
──────────────────────────────────────
  sudo nano /etc/nginx/sites-available/portal
  
  Add:
  server {
    listen 80;
    server_name your-domain.com;
    
    location / {
      proxy_pass http://localhost:8501;
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "upgrade";
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
    }
  }

Step 8: Enable Site and SSL
────────────────────────────
  sudo ln -s /etc/nginx/sites-available/portal /etc/nginx/sites-enabled/
  sudo systemctl reload nginx
  
  # Install SSL with Let's Encrypt
  sudo apt install certbot python3-certbot-nginx
  sudo certbot --nginx -d your-domain.com

Performance:
  - Users: 100-1000+
  - Suitable for: Production
  - Scalability: Good

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔧 DATABASE SETUP FOR PRODUCTION
──────────────────────────────────

For Persistent Data (Recommended):

Option A: PostgreSQL
────────────────────
1. Modify database.py to use PostgreSQL
2. Install psycopg2: pip install psycopg2-binary
3. Create connection to PostgreSQL server
4. Run migrations

Option B: Remote SQLite
───────────────────────
1. Store database on network drive
2. Set DATABASE_PATH to network location
3. Use appropriate permissions

Option C: Cloud Database
────────────────────────
1. Use: AWS RDS, Google Cloud SQL, Azure Database
2. Update connection string in config
3. Set up backups

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 DEPLOYMENT CHECKLIST
───────────────────────

Pre-Deployment:
  □ All tests pass
  □ Code reviewed
  □ Documentation updated
  □ Dependencies listed
  □ Environment variables configured
  □ Database backed up
  □ Security audit completed

Deployment:
  □ Pull latest code
  □ Install dependencies
  □ Run database migrations
  □ Start application
  □ Verify application loads
  □ Test core functionality
  □ Check database connectivity

Post-Deployment:
  □ Monitor application logs
  □ Check performance metrics
  □ Verify backups working
  □ Document deployment notes
  □ Set up monitoring alerts
  □ Schedule maintenance window

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔒 SECURITY BEST PRACTICES
──────────────────────────

Production Deployment:
  ✓ Use HTTPS/SSL (Let's Encrypt)
  ✓ Set strong environment variables
  ✓ Use secrets management
  ✓ Enable firewall rules
  ✓ Regular security updates
  ✓ Log monitoring and alerts
  ✓ Database encryption
  ✓ Regular backups
  ✓ Rate limiting
  ✓ Input validation

Environment Variables (.env):
  SECRET_KEY=your-secret-key
  DATABASE_URL=postgresql://...
  MAIL_SERVER=smtp.gmail.com
  MAIL_PORT=587
  MAIL_USERNAME=your-email@gmail.com
  MAIL_PASSWORD=your-app-password

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 MONITORING & MAINTENANCE
────────────────────────────

Setup Monitoring:
  1. Application performance monitoring (APM)
  2. Log aggregation (ELK Stack, Splunk)
  3. Uptime monitoring (UptimeRobot)
  4. Error tracking (Sentry)
  5. Performance metrics (New Relic, Datadog)

Regular Maintenance:
  - Weekly: Review logs
  - Weekly: Check backups
  - Monthly: Security updates
  - Monthly: Performance review
  - Quarterly: Full security audit

Backup Strategy:
  - Daily database backups
  - Weekly full backups
  - Monthly off-site backups
  - Test restore procedures monthly

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚨 TROUBLESHOOTING COMMON ISSUES
──────────────────────────────────

Issue: Application won't start
  → Check Python version: python --version
  → Verify dependencies: pip list
  → Check logs: streamlit run app.py

Issue: Database connection error
  → Verify database path/URL
  → Check file permissions
  → Ensure database exists

Issue: Memory issues with Docker
  → Increase memory limit: docker run -m 2g
  → Optimize application code
  → Use container orchestration (Kubernetes)

Issue: Slow performance
  → Profile application
  → Optimize database queries
  → Enable caching
  → Scale horizontally

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 RECOMMENDATION FOR HACKATHON:

For quick deployment in hackathon:
  1. Use Streamlit Cloud (easiest)
  2. Push to GitHub
  3. Connect to Streamlit Cloud
  4. Get shareable public URL
  5. Done! 🎉

For production after hackathon:
  1. Switch to PostgreSQL database
  2. Deploy on Docker with Kubernetes
  3. Set up monitoring and backups
  4. Implement SSL/TLS
  5. Set up CI/CD pipeline

╔══════════════════════════════════════════════════════════════════════════╗
║                    Ready to Deploy! 🚀                                  ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

if __name__ == "__main__":
    print(DEPLOYMENT_GUIDE)
