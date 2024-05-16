# Prishni ERP Portal

ERP portal with admin, teacher, and student views. It is built using the Django web framework and MongoDB database.

## Features

- Admin view, teacher view, and student view.
- Admin creates teacher accounts.
- Teachers create student accounts.
- Students can log in to their dashboard and view their teachers and certificates.
- Certificate creation and viewing functionality for teachers.
- Hierarchy-based system ensures that only admin can create teacher accounts, and only teachers can create student accounts.

## Getting Started

To run this ERP portal, ensure that you have Python, Django, and MongoDB installed on your computer.

1. Clone this repository to your local machine:

```bash
git clone https://github.com/your-username/prishni-erp.git

2. Navigate to the project directory:
  cd erp-portal

3. Install the required dependencies:
  pip install -r requirements.txt

4. Set up MongoDB:
- Install MongoDB on your system.
- Start the MongoDB server.

5. Run the development server:
  python manage.py runserver

6. Access the admin signup page in your browser:
  http://127.0.0.1:8000/adminSignup

```

7. Create the admin account.
8. Log in to the admin panel using the admin credentials.
9. Create teacher accounts and assign them teacher IDs (which will be used as passwords).
10. Teachers can then create student accounts using the student's date of birth as the password and email as the ID for login.

## Usage
- Log in to the admin panel using the admin credentials.
- Create teacher accounts and assign them teacher IDs.
- Teachers can log in using their teacher IDs and create student accounts.
- Teachers can create certificates and view certificates of students.
- Students can log in using their email IDs and date of birth as passwords.
- Students can view their teachers and certificates on their dashboard.

  
Feel free to modify this README file according to your project requirements.


