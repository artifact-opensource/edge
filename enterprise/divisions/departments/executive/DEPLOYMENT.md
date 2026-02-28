# Deployment Guide

**Version:** 1.0.0  
**Last Updated:** 2026-02-01

---

## Quick Start Deployment

This guide covers deploying Artifact Virtual services using the configured infrastructure.

---

## Prerequisites

### System Requirements
- Linux server (Ubuntu 20.04+ or CentOS 8+ recommended)
- Docker and Docker Compose installed
- Nginx (if not using Docker)
- Minimum 4GB RAM, 2 CPU cores
- 50GB+ disk space

### Access Requirements
- Root or sudo access
- Domain control (artifactvirtual.com)
- SSL certificates
- Git access to this repository

---

## Step 1: Initial Setup

### Clone Repository
```bash
git clone https://github.com/amuzetnoM/private.git
cd private
```

### Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit with your values
nano .env

# Review configuration
cat config.json
```

**Important:** Update all credentials and secrets in `.env`

---

## Step 2: Deploy with Docker Compose

### Using Docker Compose (Recommended)

```bash
cd infrastructure/docker

# Build images
docker-compose build

# Start services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### Verify Deployment
```bash
# Check nginx is running
curl http://localhost/health

# Should return: OK
```

---

## Step 3: Deploy Nginx (Alternative - Direct Installation)

If not using Docker:

```bash
# Install Nginx
sudo apt update
sudo apt install nginx

# Deploy configuration
sudo cp infrastructure/nginx/nginx.conf /etc/nginx/nginx.conf
sudo cp infrastructure/nginx/sites-available/artifactvirtual.conf /etc/nginx/sites-available/

# Enable site
sudo ln -s /etc/nginx/sites-available/artifactvirtual.conf /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
sudo systemctl enable nginx
```

---

## Step 4: SSL/TLS Configuration

### Using Let's Encrypt (Free)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d artifactvirtual.com -d www.artifactvirtual.com

# Certbot will automatically configure Nginx
```

### Using Existing Certificates

Update paths in nginx configuration:
```nginx
ssl_certificate /path/to/your/certificate.crt;
ssl_certificate_key /path/to/your/private.key;
```

---

## Step 5: DNS Configuration

### Point Domain to Server

Add DNS A records:
```
artifactvirtual.com        A    YOUR_SERVER_IP
www.artifactvirtual.com    A    YOUR_SERVER_IP
```

### Verify DNS
```bash
dig artifactvirtual.com
nslookup artifactvirtual.com
```

---

## Step 6: Firewall Configuration

### Configure UFW (Ubuntu)

```bash
# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

### Configure firewalld (CentOS)

```bash
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

---

## Step 7: Verify Deployment

### Health Checks

```bash
# Test HTTP (should redirect to HTTPS)
curl -I http://artifactvirtual.com

# Test HTTPS
curl -I https://artifactvirtual.com

# Test health endpoint
curl https://artifactvirtual.com/health
```

### SSL Testing
```bash
# Test SSL configuration
openssl s_client -connect artifactvirtual.com:443 -servername artifactvirtual.com

# Or use online tool: https://www.ssllabs.com/ssltest/
```

---

## Step 8: Monitoring

### Check Logs

**Docker:**
```bash
docker-compose logs -f nginx
```

**Direct Nginx:**
```bash
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### System Monitoring

```bash
# Check system resources
htop

# Check disk space
df -h

# Check memory
free -h

# Check Docker resources
docker stats
```

---

## Deployment Checklist

- [ ] Server provisioned and accessible
- [ ] Repository cloned
- [ ] .env configured with all credentials
- [ ] Docker and Docker Compose installed (if using Docker)
- [ ] Services started successfully
- [ ] SSL certificates obtained and configured
- [ ] DNS records configured and propagated
- [ ] Firewall rules configured
- [ ] Health checks passing
- [ ] Logs monitored for errors
- [ ] Backup strategy in place
- [ ] Monitoring configured

---

## Troubleshooting

### Service Won't Start

```bash
# Check Docker logs
docker-compose logs

# Check nginx configuration
sudo nginx -t

# Check file permissions
ls -la /var/www/artifactvirtual
```

### SSL Certificate Issues

```bash
# Verify certificate files exist
ls -la /etc/ssl/certs/artifactvirtual.crt
ls -la /etc/ssl/private/artifactvirtual.key

# Check certificate validity
openssl x509 -in /etc/ssl/certs/artifactvirtual.crt -text -noout
```

### DNS Not Resolving

```bash
# Check DNS propagation
dig artifactvirtual.com @8.8.8.8

# Clear local DNS cache
sudo systemd-resolve --flush-caches
```

### Port Already in Use

```bash
# Find process using port 80
sudo lsof -i :80

# Kill process if needed
sudo kill -9 PID
```

---

## Rollback Procedure

If deployment fails:

```bash
# Stop services
docker-compose down

# Or stop nginx
sudo systemctl stop nginx

# Restore previous configuration
git checkout previous-commit

# Restart services
docker-compose up -d
# or
sudo systemctl start nginx
```

---

## Production Deployment Best Practices

1. **Test in staging first**
   - Deploy to staging environment
   - Run full test suite
   - Verify all functionality

2. **Schedule maintenance window**
   - Notify users in advance
   - Deploy during low-traffic periods
   - Have rollback plan ready

3. **Monitor closely**
   - Watch logs during deployment
   - Monitor error rates
   - Check performance metrics

4. **Document changes**
   - Update changelog
   - Document any issues encountered
   - Record rollback procedures used

5. **Backup before deploy**
   - Backup database
   - Backup configuration files
   - Backup current running state

---

## Post-Deployment

### Verify All Services

```bash
# Test main website
curl https://artifactvirtual.com

# Test API (if applicable)
curl https://artifactvirtual.com/api/health

# Test specific features
# [Add specific tests for your services]
```

### Update Documentation

- Update deployment changelog
- Document any custom configurations
- Note any issues and resolutions

### Set Up Monitoring

- Configure uptime monitoring
- Set up alerting
- Enable log aggregation
- Configure performance monitoring

---

## Support

### Getting Help

- **Internal:** it-support@artifactvirtual.com
- **Operations:** ops@artifactvirtual.com
- **Emergency:** See escalation procedures

### Resources

- Infrastructure documentation: `infrastructure/*/README.md`
- Configuration reference: `config.json`
- Department contacts: See `README.md`

---

**Document Owner:** IT Infrastructure & Operations  
**Review Cycle:** After each major deployment  
**Last Deployment:** TBD
