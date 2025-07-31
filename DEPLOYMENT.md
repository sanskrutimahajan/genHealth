# Railway Deployment Guide - GenHealth API

## 🚂 **Railway Deployment (Recommended)**

Railway is the easiest and most reliable platform for deploying your GenHealth API. It offers automatic deployments from GitHub and handles all the infrastructure setup for you.

## 📋 **Prerequisites**

- GitHub account with your GenHealth repository
- Railway account (free tier available)

## 🚀 **Step-by-Step Deployment**

### **Step 1: Prepare Your Repository**
Ensure your repository has these files:
- ✅ `requirements.txt` - Python dependencies
- ✅ `Procfile` - Railway startup command
- ✅ `app/main.py` - FastAPI application
- ✅ All other application files

### **Step 2: Sign Up for Railway**
1. **Go to** [railway.app](https://railway.app)
2. **Sign up** with your GitHub account
3. **Verify your email** if required

### **Step 3: Create New Project**
1. **Click** "New Project" button
2. **Select** "Deploy from GitHub repo"
3. **Choose** your `genHealth` repository
4. **Click** "Deploy Now"

### **Step 4: Wait for Initial Deploy**
- Railway will automatically detect it's a Python project
- It will install dependencies from `requirements.txt`
- It will use the `Procfile` to start your app
- **Wait** for the green "Deployed" status

### **Step 5: Add PostgreSQL Database**
1. **Click** "New" button in your project
2. **Select** "Database" → "PostgreSQL"
3. **Wait** for it to be created (takes 1-2 minutes)
4. **Copy** the connection URL from the database settings

### **Step 6: Configure Environment Variables**
1. **Go to** your web service settings
2. **Add environment variable**:
   ```
   DATABASE_URL=your_postgres_connection_url
   ```
3. **Save** the changes

### **Step 7: Redeploy (if needed)**
- Railway will automatically redeploy when you add environment variables
- **Wait** for the deployment to complete

## ✅ **Verification Steps**

### **Test Your Live API**
1. **Visit** your Railway URL (e.g., `https://your-app-name.railway.app`)
2. **Check** the root endpoint returns API info
3. **Visit** `/docs` to see the Swagger UI
4. **Test** the `/upload/` endpoint with a PDF
5. **Check** `/orders/` and `/activity-logs/` endpoints

### **Expected Response from Root Endpoint**
```json
{
  "message": "GenHealth API is running!",
  "docs": "/docs",
  "endpoints": {
    "orders": "/orders/",
    "upload": "/upload/",
    "activity_logs": "/activity-logs/"
  }
}
```

## 🔧 **Railway Configuration**

### **Procfile Content**
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### **Environment Variables**
- `DATABASE_URL` - PostgreSQL connection string
- `PORT` - Automatically set by Railway

### **Build Process**
Railway automatically:
1. **Detects** Python project
2. **Installs** dependencies from `requirements.txt`
3. **Runs** the command from `Procfile`
4. **Exposes** the service on the provided URL

## 📊 **Monitoring Your Deployment**

### **Railway Dashboard Features**
- **Real-time logs** - View application logs
- **Deployment history** - Track all deployments
- **Environment variables** - Manage configuration
- **Database management** - View and manage PostgreSQL
- **Custom domains** - Add your own domain (optional)

### **Health Checks**
- **Automatic restarts** if the application crashes
- **Load balancing** for high availability
- **SSL certificates** automatically provisioned

## 🆘 **Troubleshooting**

### **Common Issues**

#### **Deployment Fails**
- **Check logs** in Railway dashboard
- **Verify** all dependencies are in `requirements.txt`
- **Ensure** `Procfile` is correct

#### **Database Connection Issues**
- **Verify** `DATABASE_URL` is set correctly
- **Check** PostgreSQL service is running
- **Ensure** connection string format is correct

#### **PDF Upload Not Working**
- **Check** if OCR dependencies are installed
- **Verify** file size limits
- **Test** with a simple PDF first

### **Debug Commands**
```bash
# Check Railway logs
railway logs

# Check environment variables
railway variables

# Redeploy manually
railway up
```

## 🎯 **Post-Deployment**

### **Share Your API**
- **API URL**: `https://your-app-name.railway.app`
- **Documentation**: `https://your-app-name.railway.app/docs`
- **GitHub Repository**: Your repository URL

### **For Interviews**
You can now confidently share:
- ✅ **Live API URL** for demonstration
- ✅ **Working PDF upload** with OCR
- ✅ **CRUD operations** for orders
- ✅ **Activity logging** functionality
- ✅ **Production-ready** deployment

## 💡 **Railway Benefits**

- **Free tier** available for development
- **Automatic deployments** from GitHub
- **Built-in PostgreSQL** database
- **SSL certificates** included
- **Global CDN** for fast access
- **Easy scaling** as needed
- **Professional dashboard** for monitoring

Your GenHealth API is now deployed and ready for production use! 🚀 