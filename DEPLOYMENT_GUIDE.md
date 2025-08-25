# Django Deployment Guide

## Local Development Setup

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Start development server:**
   ```bash
   python manage.py runserver
   ```

## Production Deployment (Vercel)

### Prerequisites
- Vercel account
- Vercel CLI installed (`npm i -g vercel`)

### Deployment Steps

1. **Build the project:**
   ```bash
   python manage.py collectstatic --noinput
   ```

2. **Deploy to Vercel:**
   ```bash
   vercel --prod
   ```

3. **Set environment variables in Vercel dashboard:**
   - `DJANGO_SECRET_KEY`: Your secret key
   - `DJANGO_DEBUG`: `False`
   - `ALLOWED_HOSTS`: Your domain(s)

### Environment Variables for Production

```env
DJANGO_SECRET_KEY=your-very-secure-secret-key
DJANGO_DEBUG=False
ALLOWED_HOSTS=your-domain.vercel.app,your-custom-domain.com
```

## Security Checklist

- [ ] Use environment variables for sensitive data
- [ ] Set `DEBUG=False` in production
- [ ] Configure proper ALLOWED_HOSTS
- [ ] Enable HTTPS redirects
- [ ] Use secure cookies
- [ ] Set up proper CORS configuration
- [ ] Use CSRF protection
- [ ] Set HSTS headers

## Database Considerations

For production, consider using:
- PostgreSQL (recommended for production)
- MySQL
- Cloud databases (AWS RDS, Google Cloud SQL, etc.)

Update `DATABASES` setting in production:
```python
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
}
```

## Monitoring and Maintenance

- Set up error tracking (Sentry, etc.)
- Monitor performance
- Regular backups
- Keep dependencies updated
- Security audits

## Troubleshooting

### Common Issues:

1. **Static files not loading:**
   - Run `python manage.py collectstatic`
   - Check STATIC_ROOT and STATIC_URL settings

2. **Database connection issues:**
   - Verify database URL format
   - Check database permissions

3. **HTTPS redirect issues:**
   - Ensure `SECURE_SSL_REDIRECT = True` in production
   - Check proxy settings if behind load balancer

4. **CORS issues:**
   - Verify CORS_ALLOWED_ORIGINS includes your frontend domain
