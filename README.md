Student Portal – Student Registration & Admin Management System
A web-based Student Portal developed using Python and FastAPI that provides a platform for student registration and administrative management.

This project was developed as part of my learning journey at Innomatics Research Labs, focusing on backend development, database integration, authentication, and dynamic web applications.
🚀 Features
- Student Registration – Register students through a web-based interface.
- Admin Management – Supports administrative management of student information.
- Database Integration – Stores application data using SQLite and SQLAlchemy.
- Session Management – Uses Session Middleware to manage user sessions.
- Secure Password Hashing – Implements Argon2 password hashing using pwdlib.
- Dynamic Templates – Renders web pages using Jinja2 templates.
- Environment Configuration – Uses environment variables for application configuration.
🛠️ Technologies Used
- Python
- FastAPI
- SQLAlchemy
- SQLite
- HTML5
- CSS3
- Jinja2 Templates
- Session Middleware
- pwdlib (Argon2)
- python-dotenv
📂 Project Structure
student-portal/
│
├── screen_shots/
├── static/
│   └── css/
├── templates/
├── main.py
├── database.py
├── models.py
├── requirements.txt
├── .gitignore
└── README.md


⚙️ Installation & Setup
1. Clone the Repository
git clone https://github.com/yugendar123/student-portal.git


2. Navigate to the Project Directory
cd student-portal


3. Create a Virtual Environment
python -m venv venv


4. Activate the Virtual Environment

Windows:
venv\Scripts\activate


5. Install Dependencies
pip install -r requirements.txt


6. Configure Environment Variables

Create the required environment file and configure the variables referenced in the application.

7. Run the Application
uvicorn main:app --reload


8. Open in Browser

http://127.0.0.1:8000
📸 Screenshots
Project screenshots are available in the screen_shots/ directory.
🎯 Learning Outcomes
Through this project, I gained practical experience in:
- Building web applications using FastAPI.
- Working with SQLAlchemy and SQLite.
- Creating and managing database models.
- Implementing session management.
- Understanding secure password hashing.
- Creating dynamic web pages using Jinja2.
- Organizing backend applications using modular Python files.
- Managing dependencies and environment variables.
- Using Git and GitHub for version control.
🔮 Future Enhancements
- Student profile management.
- Improved admin dashboard.
- Role-based access control.
- Advanced search and filtering.
- Responsive user interface.
- Cloud deployment.
👨‍💻 Developer
Yugendar Gadicherla

B.Tech – Computer Science and Engineering

GitHub: https://github.com/yugendar123

Project Repository: https://github.com/yugendar123/student-portal

⭐ If you find this project interesting, feel free to explore the repository!
