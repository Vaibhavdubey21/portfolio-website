from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Email Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'  # Change this to your email
app.config['MAIL_PASSWORD'] = 'your-app-password'     # Change this to your app password
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
mail = Mail(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

# Database Models
class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200))
    about = db.Column(db.Text)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    location = db.Column(db.String(100))
    photo = db.Column(db.String(200))
    linkedin = db.Column(db.String(200))
    github = db.Column(db.String(200))
    twitter = db.Column(db.String(200))

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    percentage = db.Column(db.Integer, default=0)
    category = db.Column(db.String(50))

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(200))
    link = db.Column(db.String(200))
    github_link = db.Column(db.String(200))
    technologies = db.Column(db.String(200))

class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200))
    location = db.Column(db.String(100))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    current = db.Column(db.Boolean, default=False)
    description = db.Column(db.Text)

class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    degree = db.Column(db.String(200), nullable=False)
    institution = db.Column(db.String(200))
    location = db.Column(db.String(100))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    current = db.Column(db.Boolean, default=False)
    description = db.Column(db.Text)

class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    issuer = db.Column(db.String(200))
    date_earned = db.Column(db.Date)
    link = db.Column(db.String(200))
    image = db.Column(db.String(200))

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(200), nullable=False)
    original_name = db.Column(db.String(200), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text)

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    profile = Profile.query.first()
    skills = Skill.query.all()
    projects = Project.query.all()
    experiences = Experience.query.order_by(Experience.start_date.desc()).all()
    education = Education.query.order_by(Education.start_date.desc()).all()
    certificates = Certificate.query.order_by(Certificate.date_earned.desc()).all()
    resume = Resume.query.order_by(Resume.upload_date.desc()).first()
    
    return render_template('index.html', 
                         profile=profile, 
                         skills=skills, 
                         projects=projects,
                         experiences=experiences,
                         education=education,
                         certificates=certificates,
                         resume=resume)

@app.route('/resume/<int:id>')
def view_resume(id):
    resume = Resume.query.get_or_404(id)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], resume.file_name)
    
    if os.path.exists(file_path):
        # For PDF files, display in browser
        if resume.file_name.lower().endswith('.pdf'):
            return send_file(file_path, as_attachment=False, download_name=resume.original_name)
        else:
            # For other files, force download
            return send_file(file_path, as_attachment=True, download_name=resume.original_name)
    else:
        flash('Resume file not found')
        return redirect(url_for('index'))

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        admin = Admin.query.filter_by(username=username).first()
        if admin and check_password_hash(admin.password_hash, password):
            login_user(admin)
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    profile = Profile.query.first()
    skills_count = Skill.query.count()
    projects_count = Project.query.count()
    experiences_count = Experience.query.count()
    education_count = Education.query.count()
    certificates_count = Certificate.query.count()
    resume_count = Resume.query.count()
    
    return render_template('admin/dashboard.html',
                         profile=profile,
                         skills_count=skills_count,
                         projects_count=projects_count,
                         experiences_count=experiences_count,
                         education_count=education_count,
                         certificates_count=certificates_count,
                         resume_count=resume_count)

# Profile Management
@app.route('/admin/profile', methods=['GET', 'POST'])
@login_required
def admin_profile():
    profile = Profile.query.first()
    if not profile:
        profile = Profile(name="Your Name", title="Web Developer")
        db.session.add(profile)
        db.session.commit()
    
    if request.method == 'POST':
        profile.name = request.form['name']
        profile.title = request.form['title']
        profile.about = request.form['about']
        profile.email = request.form['email']
        profile.phone = request.form['phone']
        profile.location = request.form['location']
        profile.linkedin = request.form['linkedin']
        profile.github = request.form['github']
        profile.twitter = request.form['twitter']
        
        # Handle photo upload
        if 'photo' in request.files and request.files['photo'].filename:
            file = request.files['photo']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                profile.photo = filename
        
        db.session.commit()
        flash('Profile updated successfully!')
        return redirect(url_for('admin_profile'))
    
    return render_template('admin/profile.html', profile=profile)

# Skills Management
@app.route('/admin/skills')
@login_required
def admin_skills():
    skills = Skill.query.all()
    return render_template('admin/skills.html', skills=skills)

@app.route('/admin/skills/add', methods=['GET', 'POST'])
@login_required
def add_skill():
    if request.method == 'POST':
        skill = Skill(
            name=request.form['name'],
            percentage=int(request.form['percentage']),
            category=request.form['category']
        )
        db.session.add(skill)
        db.session.commit()
        flash('Skill added successfully!')
        return redirect(url_for('admin_skills'))
    
    return render_template('admin/add_skill.html')

@app.route('/admin/skills/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_skill(id):
    skill = Skill.query.get_or_404(id)
    if request.method == 'POST':
        skill.name = request.form['name']
        skill.percentage = int(request.form['percentage'])
        skill.category = request.form['category']
        db.session.commit()
        flash('Skill updated successfully!')
        return redirect(url_for('admin_skills'))
    
    return render_template('admin/edit_skill.html', skill=skill)

@app.route('/admin/skills/delete/<int:id>')
@login_required
def delete_skill(id):
    skill = Skill.query.get_or_404(id)
    db.session.delete(skill)
    db.session.commit()
    flash('Skill deleted successfully!')
    return redirect(url_for('admin_skills'))

# Projects Management
@app.route('/admin/projects')
@login_required
def admin_projects():
    projects = Project.query.all()
    return render_template('admin/projects.html', projects=projects)

@app.route('/admin/projects/add', methods=['GET', 'POST'])
@login_required
def add_project():
    if request.method == 'POST':
        project = Project(
            title=request.form['title'],
            description=request.form['description'],
            link=request.form['link'],
            github_link=request.form['github_link'],
            technologies=request.form['technologies']
        )
        
        if 'image' in request.files and request.files['image'].filename:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                project.image = filename
        
        db.session.add(project)
        db.session.commit()
        flash('Project added successfully!')
        return redirect(url_for('admin_projects'))
    
    return render_template('admin/add_project.html')

@app.route('/admin/projects/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    project = Project.query.get_or_404(id)
    if request.method == 'POST':
        project.title = request.form['title']
        project.description = request.form['description']
        project.link = request.form['link']
        project.github_link = request.form['github_link']
        project.technologies = request.form['technologies']
        
        if 'image' in request.files and request.files['image'].filename:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                project.image = filename
        
        db.session.commit()
        flash('Project updated successfully!')
        return redirect(url_for('admin_projects'))
    
    return render_template('admin/edit_project.html', project=project)

@app.route('/admin/projects/delete/<int:id>')
@login_required
def delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!')
    return redirect(url_for('admin_projects'))

# Experience Management
@app.route('/admin/experience')
@login_required
def admin_experience():
    experiences = Experience.query.order_by(Experience.start_date.desc()).all()
    return render_template('admin/experience.html', experiences=experiences)

@app.route('/admin/experience/add', methods=['GET', 'POST'])
@login_required
def add_experience():
    if request.method == 'POST':
        experience = Experience(
            title=request.form['title'],
            company=request.form['company'],
            location=request.form['location'],
            start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%d').date(),
            description=request.form['description']
        )
        
        if request.form.get('current'):
            experience.current = True
        elif request.form['end_date']:
            experience.end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
        
        db.session.add(experience)
        db.session.commit()
        flash('Experience added successfully!')
        return redirect(url_for('admin_experience'))
    
    return render_template('admin/add_experience.html')

@app.route('/admin/experience/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_experience(id):
    experience = Experience.query.get_or_404(id)
    if request.method == 'POST':
        experience.title = request.form['title']
        experience.company = request.form['company']
        experience.location = request.form['location']
        experience.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        experience.description = request.form['description']
        
        if request.form.get('current'):
            experience.current = True
            experience.end_date = None
        elif request.form['end_date']:
            experience.current = False
            experience.end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
        
        db.session.commit()
        flash('Experience updated successfully!')
        return redirect(url_for('admin_experience'))
    
    return render_template('admin/edit_experience.html', experience=experience)

@app.route('/admin/experience/delete/<int:id>')
@login_required
def delete_experience(id):
    experience = Experience.query.get_or_404(id)
    db.session.delete(experience)
    db.session.commit()
    flash('Experience deleted successfully!')
    return redirect(url_for('admin_experience'))

# Education Management
@app.route('/admin/education')
@login_required
def admin_education():
    education = Education.query.order_by(Education.start_date.desc()).all()
    return render_template('admin/education.html', education=education)

@app.route('/admin/education/add', methods=['GET', 'POST'])
@login_required
def add_education():
    if request.method == 'POST':
        education = Education(
            degree=request.form['degree'],
            institution=request.form['institution'],
            location=request.form['location'],
            start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%d').date(),
            description=request.form['description']
        )
        
        if request.form.get('current'):
            education.current = True
        elif request.form['end_date']:
            education.end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
        
        db.session.add(education)
        db.session.commit()
        flash('Education added successfully!')
        return redirect(url_for('admin_education'))
    
    return render_template('admin/add_education.html')

@app.route('/admin/education/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_education(id):
    education = Education.query.get_or_404(id)
    if request.method == 'POST':
        education.degree = request.form['degree']
        education.institution = request.form['institution']
        education.location = request.form['location']
        education.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        education.description = request.form['description']
        
        if request.form.get('current'):
            education.current = True
            education.end_date = None
        elif request.form['end_date']:
            education.current = False
            education.end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
        
        db.session.commit()
        flash('Education updated successfully!')
        return redirect(url_for('admin_education'))
    
    return render_template('admin/edit_education.html', education=education)

@app.route('/admin/education/delete/<int:id>')
@login_required
def delete_education(id):
    education = Education.query.get_or_404(id)
    db.session.delete(education)
    db.session.commit()
    flash('Education deleted successfully!')
    return redirect(url_for('admin_education'))

# Certificates Management
@app.route('/admin/certificates')
@login_required
def admin_certificates():
    certificates = Certificate.query.order_by(Certificate.date_earned.desc()).all()
    return render_template('admin/certificates.html', certificates=certificates)

@app.route('/admin/certificates/add', methods=['GET', 'POST'])
@login_required
def add_certificate():
    if request.method == 'POST':
        certificate = Certificate(
            name=request.form['name'],
            issuer=request.form['issuer'],
            date_earned=datetime.strptime(request.form['date_earned'], '%Y-%m-%d').date(),
            link=request.form['link']
        )
        
        if 'image' in request.files and request.files['image'].filename:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                certificate.image = filename
        
        db.session.add(certificate)
        db.session.commit()
        flash('Certificate added successfully!')
        return redirect(url_for('admin_certificates'))
    
    return render_template('admin/add_certificate.html')

@app.route('/admin/certificates/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_certificate(id):
    certificate = Certificate.query.get_or_404(id)
    if request.method == 'POST':
        certificate.name = request.form['name']
        certificate.issuer = request.form['issuer']
        certificate.date_earned = datetime.strptime(request.form['date_earned'], '%Y-%m-%d').date()
        certificate.link = request.form['link']
        
        if 'image' in request.files and request.files['image'].filename:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                certificate.image = filename
        
        db.session.commit()
        flash('Certificate updated successfully!')
        return redirect(url_for('admin_certificates'))
    
    return render_template('admin/edit_certificate.html', certificate=certificate)

@app.route('/admin/certificates/delete/<int:id>')
@login_required
def delete_certificate(id):
    certificate = Certificate.query.get_or_404(id)
    db.session.delete(certificate)
    db.session.commit()
    flash('Certificate deleted successfully!')
    return redirect(url_for('admin_certificates'))

# Resume Management
@app.route('/admin/resume')
@login_required
def admin_resume():
    resumes = Resume.query.order_by(Resume.upload_date.desc()).all()
    return render_template('admin/resume.html', resumes=resumes)

@app.route('/admin/resume/upload', methods=['GET', 'POST'])
@login_required
def upload_resume():
    if request.method == 'POST':
        if 'resume_file' not in request.files:
            flash('No file selected')
            return redirect(request.url)
        
        file = request.files['resume_file']
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        
        if file and allowed_resume_file(file.filename):
            filename = secure_filename(file.filename)
            # Add timestamp to avoid filename conflicts
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{filename}"
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            resume = Resume(
                file_name=filename,
                original_name=file.filename,
                description=request.form.get('description', '')
            )
            db.session.add(resume)
            db.session.commit()
            flash('Resume uploaded successfully!')
            return redirect(url_for('admin_resume'))
        else:
            flash('Invalid file type. Please upload PDF, DOC, or DOCX files.')
            return redirect(request.url)
    
    return render_template('admin/upload_resume.html')

@app.route('/admin/resume/delete/<int:id>')
@login_required
def delete_resume(id):
    resume = Resume.query.get_or_404(id)
    
    # Delete file from filesystem
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], resume.file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
    
    db.session.delete(resume)
    db.session.commit()
    flash('Resume deleted successfully!')
    return redirect(url_for('admin_resume'))

@app.route('/download/resume/<int:id>')
def download_resume(id):
    resume = Resume.query.get_or_404(id)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], resume.file_name)
    
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True, download_name=resume.original_name)
    else:
        flash('Resume file not found')
        return redirect(url_for('index'))

@app.route('/contact', methods=['POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        try:
            # Send email to admin
            msg = Message(
                subject=f"Portfolio Contact: {subject}",
                sender=app.config['MAIL_DEFAULT_SENDER'],
                recipients=[app.config['MAIL_DEFAULT_SENDER']]
            )
            msg.body = f"""
New message from your portfolio website:

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}

---
This message was sent from your portfolio contact form.
            """
            mail.send(msg)
            
            # Send confirmation email to user
            confirmation_msg = Message(
                subject="Thank you for contacting me!",
                sender=app.config['MAIL_DEFAULT_SENDER'],
                recipients=[email]
            )
            confirmation_msg.body = f"""
Dear {name},

Thank you for reaching out to me through my portfolio website. I have received your message and will get back to you soon.

Your message:
Subject: {subject}
Message: {message}

Best regards,
[Your Name]
            """
            mail.send(confirmation_msg)
            
            flash(f'Thank you {name}! Your message has been sent successfully. Check your email for confirmation.')
            
        except Exception as e:
            flash(f'Sorry {name}, there was an error sending your message. Please try again later.')
            print(f"Email error: {e}")
        
        return redirect(url_for('index') + '#contact')

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_resume_file(filename):
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Initialize database and create admin user
@app.cli.command("init-db")
def init_db():
    db.create_all()
    
    # Create admin user if it doesn't exist
    admin = Admin.query.filter_by(username='admin').first()
    if not admin:
        admin = Admin(
            username='admin',
            password_hash=generate_password_hash('admin123')
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created: username='admin', password='admin123'")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Create admin user if it doesn't exist
        admin = Admin.query.filter_by(username='admin').first()
        if not admin:
            admin = Admin(
                username='admin',
                password_hash=generate_password_hash('admin123')
            )
            db.session.add(admin)
            db.session.commit()
    
    app.run(debug=True)
