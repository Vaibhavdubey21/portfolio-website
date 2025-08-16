# Portfolio Website Deployment Guide

This guide will help you deploy your Flask portfolio website to Vercel and GitHub.

## Prerequisites

1. **GitHub Account** - For hosting your code
2. **Vercel Account** - For hosting your website
3. **Gmail Account** - For email functionality (optional)

## Step 1: Prepare Your Code for Deployment

### 1.1 Update Email Configuration

Before deploying, update the email configuration in `app.py`:

```python
# Email Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-actual-email@gmail.com'  # Your Gmail
app.config['MAIL_PASSWORD'] = 'your-app-password'           # Gmail App Password
app.config['MAIL_DEFAULT_SENDER'] = 'your-actual-email@gmail.com'
```

**To get Gmail App Password:**

1. Go to your Google Account settings
2. Enable 2-Factor Authentication
3. Generate an App Password for "Mail"
4. Use this password in the configuration

### 1.2 Create Environment Variables (Optional)

For better security, you can use environment variables:

```python
import os

app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'your-email@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'your-app-password')
```

## Step 2: Deploy to GitHub

### 2.1 Initialize Git Repository

```bash
git init
git add .
git commit -m "Initial commit: Portfolio website"
```

### 2.2 Create GitHub Repository

1. Go to [GitHub](https://github.com)
2. Click "New repository"
3. Name it `portfolio-website`
4. Don't initialize with README (we already have one)
5. Click "Create repository"

### 2.3 Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/portfolio-website.git
git branch -M main
git push -u origin main
```

## Step 3: Deploy to Vercel

### 3.1 Create Vercel Configuration

Create a file named `vercel.json` in your project root:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

### 3.2 Create WSGI Entry Point

Create a file named `wsgi.py` in your project root:

```python
from app import app

if __name__ == "__main__":
    app.run()
```

### 3.3 Deploy to Vercel

#### Method 1: Using Vercel CLI

1. Install Vercel CLI:

```bash
npm install -g vercel
```

2. Login to Vercel:

```bash
vercel login
```

3. Deploy:

```bash
vercel
```

#### Method 2: Using Vercel Dashboard

1. Go to [Vercel](https://vercel.com)
2. Sign up/Login with your GitHub account
3. Click "New Project"
4. Import your GitHub repository
5. Configure the project:
   - **Framework Preset**: Other
   - **Build Command**: Leave empty
   - **Output Directory**: Leave empty
   - **Install Command**: `pip install -r requirements.txt`
6. Click "Deploy"

### 3.4 Set Environment Variables (Optional)

If you're using environment variables for email:

1. Go to your Vercel project dashboard
2. Click "Settings" → "Environment Variables"
3. Add:
   - `MAIL_USERNAME`: Your Gmail address
   - `MAIL_PASSWORD`: Your Gmail app password

## Step 4: Database Setup

### 4.1 Local Development

For local development, the SQLite database will be created automatically:

```bash
python app.py
```

### 4.2 Production (Vercel)

Vercel uses serverless functions, so the database will be recreated on each request. For production, consider:

1. **Using a cloud database** (PostgreSQL on Railway, Supabase, etc.)
2. **Using Vercel KV** for simple data storage
3. **Using external file storage** for uploads

## Step 5: Custom Domain (Optional)

### 5.1 Add Custom Domain on Vercel

1. Go to your Vercel project dashboard
2. Click "Settings" → "Domains"
3. Add your custom domain
4. Follow the DNS configuration instructions

## Step 6: Post-Deployment

### 6.1 Access Admin Panel

1. Visit your deployed website
2. Go to `/admin/login`
3. Use default credentials:
   - Username: `admin`
   - Password: `admin123`
4. **Important**: Change the password immediately!

### 6.2 Update Content

1. Add your profile information
2. Upload your photo
3. Add your skills, projects, experience, education, and certificates
4. Upload your resume
5. Add social media links

## Troubleshooting

### Common Issues

1. **Email not working**: Check Gmail app password and enable "Less secure app access"
2. **File uploads not working**: Vercel has read-only filesystem, use external storage
3. **Database issues**: Use cloud database for production
4. **Build errors**: Check Python version compatibility

### Vercel Limitations

- **File System**: Read-only, files uploaded during runtime will be lost
- **Database**: No persistent storage, consider external database
- **File Uploads**: Use external services like AWS S3, Cloudinary, etc.

## Alternative Deployment Options

### 1. Railway

- Supports persistent storage
- Easy database integration
- Good for Flask applications

### 2. Heroku

- Traditional hosting platform
- Supports PostgreSQL
- More expensive but reliable

### 3. DigitalOcean App Platform

- Good performance
- Supports various databases
- Reasonable pricing

## Security Considerations

1. **Change default admin password** immediately after deployment
2. **Use environment variables** for sensitive information
3. **Enable HTTPS** (automatic with Vercel)
4. **Regular backups** of your database
5. **Keep dependencies updated**

## Maintenance

1. **Regular updates**: Keep Flask and dependencies updated
2. **Backup data**: Regularly backup your database
3. **Monitor logs**: Check Vercel function logs for errors
4. **Performance**: Monitor website performance and optimize

## Support

If you encounter issues:

1. Check Vercel function logs
2. Verify environment variables
3. Test locally first
4. Check Flask documentation
5. Review Vercel documentation

---

**Happy Deploying! 🚀**
