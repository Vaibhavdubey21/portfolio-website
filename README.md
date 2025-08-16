# Portfolio Website with Admin Panel

A dynamic and modern portfolio website built with Python Flask, featuring a comprehensive admin panel for easy content management.

## Features

### 🎨 Frontend Features

- **Modern Responsive Design** - Beautiful gradient design with Bootstrap 5
- **Profile Section** - Display your photo, name, title, and about information
- **Skills Section** - Show your skills with progress bars and categories
- **Projects Section** - Showcase your projects with images and links
- **Experience Section** - Display your work experience with dates
- **Education Section** - Show your educational background
- **Certificates Section** - Display your certifications and achievements
- **Resume Section** - Upload and allow visitors to download your resume
- **Contact Section** - Display contact information and social links
- **Smooth Scrolling** - Smooth navigation between sections

### 🔧 Admin Panel Features

- **Secure Login** - Username/password authentication
- **Dashboard** - Overview of all content with statistics
- **Profile Management** - Edit personal information and upload photo
- **Skills Management** - Add, edit, and delete skills with percentages
- **Projects Management** - Add, edit, and delete projects with images
- **Experience Management** - Add, edit, and delete work experience
- **Education Management** - Add, edit, and delete education details
- **Certificates Management** - Add, edit, and delete certificates
- **Resume Management** - Upload, manage, and delete resume files
- **File Upload** - Support for images and PDF/DOC files

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or download the project**

   ```bash
   # If using git
   git clone <repository-url>
   cd portfolio-website
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**

   ```bash
   python app.py
   ```

4. **Access the website**
   - Portfolio: http://localhost:5000
   - Admin Panel: http://localhost:5000/admin/login

## Default Admin Credentials

- **Username:** admin
- **Password:** admin123

**⚠️ Important:** Change the default password after first login for security.

## File Structure

```
portfolio-website/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Main portfolio page
│   └── admin/            # Admin templates
│       ├── base.html     # Admin base template
│       ├── login.html    # Admin login
│       ├── dashboard.html # Admin dashboard
│       ├── resume.html   # Resume management
│       └── upload_resume.html # Resume upload
├── static/               # Static files
│   └── uploads/          # Uploaded files (created automatically)
└── portfolio.db          # SQLite database (created automatically)
```

## Usage Guide

### 1. First Time Setup

1. Run the application
2. Go to http://localhost:5000/admin/login
3. Login with default credentials (admin/admin123)
4. Start by creating your profile in the Profile section

### 2. Adding Content

- **Profile**: Add your name, title, about, contact info, and photo
- **Skills**: Add your technical skills with proficiency percentages
- **Projects**: Add your projects with descriptions, images, and links
- **Experience**: Add your work experience with company details
- **Education**: Add your educational background
- **Certificates**: Add your certifications and achievements
- **Resume**: Upload your resume file (PDF, DOC, DOCX)

### 3. Managing Content

- Use the admin panel sidebar to navigate between different sections
- Each section has Add, Edit, and Delete functionality
- Images and files are automatically stored in the uploads folder

### 4. Customization

- Edit `templates/base.html` to change colors and styling
- Modify `app.py` to add new features or change functionality
- Update the database models in `app.py` to add new content types

## Security Features

- Password hashing using Werkzeug
- Secure file upload with validation
- Admin-only access to management functions
- File type restrictions for uploads
- Maximum file size limits

## Supported File Types

- **Images**: PNG, JPG, JPEG, GIF (for profile photos, project images, certificates)
- **Documents**: PDF, DOC, DOCX (for resumes)

## Database

The application uses SQLite database (`portfolio.db`) which is created automatically. The database includes tables for:

- Admin users
- Profile information
- Skills
- Projects
- Experience
- Education
- Certificates
- Resumes

## Deployment

To deploy this application:

1. **For Production:**

   - Change the secret key in `app.py`
   - Use a production WSGI server (Gunicorn, uWSGI)
   - Set up a reverse proxy (Nginx, Apache)
   - Use a production database (PostgreSQL, MySQL)

2. **For Simple Hosting:**
   - Platforms like Heroku, PythonAnywhere, or Railway
   - Update the database URI for your hosting platform
   - Configure environment variables for sensitive data

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the port in `app.py` or kill the process using the port
2. **Upload folder not found**: The folder is created automatically, ensure write permissions
3. **Database errors**: Delete `portfolio.db` and restart the application
4. **File upload issues**: Check file size and type restrictions

### Error Logs

Check the console output for error messages when running the application.

## Contributing

Feel free to contribute to this project by:

- Reporting bugs
- Suggesting new features
- Submitting pull requests
- Improving documentation

## License

This project is open source and available under the MIT License.

## Support

If you need help or have questions:

1. Check the troubleshooting section
2. Review the code comments
3. Create an issue in the repository

---

**Happy coding! 🚀**
