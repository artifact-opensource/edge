# Nginx Deployment Instructions

## Prerequisites
- Nginx installed on your server
- SSL certificates for artifactvirtual.com
- Root or sudo access

## Installation Steps

### 1. Install Nginx (if not already installed)

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install nginx
```

**CentOS/RHEL:**
```bash
sudo yum install nginx
```

### 2. Deploy Configuration Files

```bash
# Copy main configuration
sudo cp infrastructure/nginx/nginx.conf /etc/nginx/nginx.conf

# Copy site configuration
sudo cp infrastructure/nginx/sites-available/artifactvirtual.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/artifactvirtual.conf /etc/nginx/sites-enabled/
```

### 3. Obtain SSL Certificates

**Using Let's Encrypt (Recommended):**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d artifactvirtual.com -d www.artifactvirtual.com
```

**Or update the SSL certificate paths in the configuration:**
```nginx
ssl_certificate /etc/letsencrypt/live/artifactvirtual.com/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/artifactvirtual.com/privkey.pem;
```

### 4. Create Web Root Directory

```bash
sudo mkdir -p /var/www/artifactvirtual
sudo chown -R $USER:$USER /var/www/artifactvirtual
sudo chmod -R 755 /var/www/artifactvirtual
```

### 5. Test Configuration

```bash
sudo nginx -t
```

### 6. Start/Restart Nginx

```bash
sudo systemctl restart nginx
sudo systemctl enable nginx
```

### 7. Configure Firewall

```bash
sudo ufw allow 'Nginx Full'
sudo ufw status
```

## Docker Deployment (Alternative)

### Using Docker Compose

Create `docker-compose.yml`:
```yaml
version: '3'
services:
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./infrastructure/nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./infrastructure/nginx/sites-available:/etc/nginx/sites-available:ro
      - ./infrastructure/nginx/conf.d:/etc/nginx/conf.d:ro
      - /var/www/artifactvirtual:/var/www/artifactvirtual:ro
      - /etc/ssl/certs:/etc/ssl/certs:ro
      - /etc/ssl/private:/etc/ssl/private:ro
    restart: unless-stopped
```

Run:
```bash
docker-compose up -d
```

## Monitoring

### Check Nginx Status
```bash
sudo systemctl status nginx
```

### View Logs
```bash
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Reload Configuration (without downtime)
```bash
sudo nginx -s reload
```

## SSL Certificate Renewal (Let's Encrypt)

Auto-renewal is typically configured automatically. Test renewal:
```bash
sudo certbot renew --dry-run
```

## Troubleshooting

### Test configuration syntax
```bash
sudo nginx -t
```

### Check if Nginx is listening
```bash
sudo netstat -tulpn | grep nginx
```

### Check SELinux (if applicable)
```bash
sudo setsebool -P httpd_can_network_connect 1
```

## Security Best Practices

1. Keep Nginx updated
2. Use strong SSL/TLS configuration
3. Enable rate limiting (already configured)
4. Regular security audits
5. Monitor logs for suspicious activity
6. Use firewall rules
7. Implement fail2ban for brute force protection

## Maintenance

### Update Nginx
```bash
sudo apt update && sudo apt upgrade nginx
```

### Backup Configuration
```bash
sudo cp -r /etc/nginx /backup/nginx-$(date +%Y%m%d)
```

## Support

For issues or questions, contact: support@artifactvirtual.com
