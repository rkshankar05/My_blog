# My_blog

A Django blog application with user authentication, OTP-based signup, profile pages, image uploads, blog search, password reset emails, and protected blog editing/deletion.

## Features

- User signup with email OTP verification
- Login, logout, and password reset flow
- Auto logout after inactivity
- Create, edit, delete, and view blog posts
- Owner-only edit/delete permissions
- Drag-and-drop image upload for blog images
- Profile editing with profile image upload
- Blog search by title, content, and username
- Safer delete confirmation page

## Tech Stack

- Python
- Django 5.2.1
- SQLite for local development
- Pillow for image validation
- SMTP email support

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r my_blog/requirements.txt
```

3. Create a `.env` file in the project root or inside `my_blog/` with your email settings:

```env
SECRET_KEY=replace-this-with-a-secure-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
SESSION_COOKIE_AGE=900
```

4. Run migrations:

```bash
cd my_blog
python manage.py migrate
```

5. Start the development server:

```bash
python manage.py runserver
```

Open the app at:

```text
http://127.0.0.1:8000/
```

## Notes

- Local database files, uploaded media, virtual environments, cache files, and secrets are ignored by git.
- Use a Gmail app password or another SMTP provider for email features.
- Keep `DEBUG=False` and set a strong `SECRET_KEY` before deploying.
