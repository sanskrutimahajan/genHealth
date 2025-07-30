# Deployment Guide - Make Your API Publicly Accessible

## 🚀 Quick Deployment Options

### Option 1: Railway (Recommended - Free & Easy)
1. **Sign up** at [railway.app](https://railway.app)
2. **Connect your GitHub** repository
3. **Add PostgreSQL** database from Railway dashboard
4. **Set environment variables**:
   ```
   DATABASE_URL=your_railway_postgres_url
   ```
5. **Deploy** - Railway will automatically detect Python and deploy

### Option 2: Render (Free Tier Available)
1. **Sign up** at [render.com](https://render.com)
2. **Create new Web Service**
3. **Connect your GitHub** repository
4. **Configure**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. **Add PostgreSQL** database
6. **Set environment variables**
7. **Deploy**

### Option 3: Heroku (Paid)
1. **Install Heroku CLI**
2. **Create app**: `heroku create your-app-name`
3. **Add PostgreSQL**: `heroku addons:create heroku-postgresql:mini`
4. **Deploy**: `git push heroku main`

### Option 4: DigitalOcean App Platform
1. **Sign up** at [digitalocean.com](https://digitalocean.com)
2. **Create new App**
3. **Connect GitHub** repository
4. **Configure** build and run commands
5. **Add database** if needed
6. **Deploy**

## 🔧 Environment Setup for Production

### Required Environment Variables:
```bash
DATABASE_URL=postgresql://username:password@host:port/database
SECRET_KEY=your-secret-key-here
```

### Database Setup:
- **PostgreSQL** is recommended for production
- **SQLite** works for development but not recommended for production

## 📋 Pre-Deployment Checklist

- [ ] All dependencies are in `requirements.txt`
- [ ] Environment variables are configured
- [ ] Database is set up and accessible
- [ ] API endpoints are working locally
- [ ] PDF upload functionality is tested

## 🧪 Testing Your Deployed API

Once deployed, test your API:

1. **Health Check**: `https://your-app-url.railway.app/`
2. **API Docs**: `https://your-app-url.railway.app/docs`
3. **PDF Upload**: Use the `/upload/` endpoint
4. **View Orders**: `https://your-app-url.railway.app/orders/`
5. **View Activity Logs**: `https://your-app-url.railway.app/activity-logs/`

## 🔒 Security Considerations

- Use HTTPS in production
- Set strong SECRET_KEY
- Configure CORS properly
- Use environment variables for sensitive data
- Consider rate limiting for production

## 📊 Monitoring

- Monitor API response times
- Check error logs
- Monitor database performance
- Set up alerts for downtime

## 🆘 Troubleshooting

### Common Issues:
1. **Database Connection**: Check DATABASE_URL format
2. **Port Issues**: Use `$PORT` environment variable
3. **Dependencies**: Ensure all packages are in requirements.txt
4. **File Upload**: Check file size limits

### Debug Commands:
```bash
# Check logs
heroku logs --tail  # (Heroku)
railway logs        # (Railway)

# Check environment
echo $DATABASE_URL
```

## 🎯 Next Steps After Deployment

1. **Test all endpoints** on the live URL
2. **Upload your PDF** and verify extraction works
3. **Check activity logs** are being recorded
4. **Share the API URL** with stakeholders
5. **Monitor performance** and usage 