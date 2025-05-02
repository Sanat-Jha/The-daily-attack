# The Daily Attack

A modern, feature-rich blogging platform built with Django and Tailwind CSS.

## Overview

The Daily Attack is a blogging platform that allows editors to create, edit, and publish articles while providing viewers with a clean, responsive interface to read content. The platform includes user management with different permission levels, tagging functionality, search capabilities, API access, and AI content suggestion.

## Features

### User Management
- **User Types**: Two user roles - Editors and Viewers
- **Authentication**: Login, logout, and signup functionality

### Content Management
- **Post Creation**: Rich text editor for creating blog posts
- **Draft System**: Save posts as drafts before publishing
- **Tagging**: Add tags to posts for better categorization
- **Publishing Workflow**: Transition from draft to published state

### Integrated Gemini
- **Title suggestion**: Get Title suggestions from Gemini AI based on your content.
- **Content suggestion suggestion**: Get content improvement suggestions from AI.


### User Interface
- **User-friendly Design**: Built with Tailwind CSS for a modern.
- **Search Functionality**: Search posts by title or content
- **Tag Filtering**: View posts by specific tags
- **Dashboard**: Personalized dashboard for editors and viewers

### API Access
- **API Key Management**: Editors can generate API keys
- **API Documentation**: Comprehensive documentation for API endpoints
- **Programmatic Access**: Create and retrieve posts via API

### Social Integration
- **LinkedIn Sharing**: Share published posts directly to LinkedIn

## Project Structure

```
TheDailyAttack/
├── blog/                   # Main application
│   ├── models.py           # Data models (Post, Tag, UserProfile, APIKey)
│   ├── views.py            # View functions
│   ├── forms.py            # Form definitions
│   ├── urls.py             # URL routing
│   ├── middleware.py       # Custom middleware
│   ├── serializers.py      # API serializers
│   ├── signals.py          # Django signals
│   └── templatetags/       # Custom template tags
├── dailyattack/            # Project settings
│   ├── settings.py         # Django settings
│   ├── urls.py             # Project URL configuration
│   ├── asgi.py             # ASGI configuration
│   └── wsgi.py             # WSGI configuration
└── templates/              # HTML templates
    ├── base.html           # Base template
    └── blog/               # Blog-specific templates
        ├── home.html       # Homepage template
        ├── post_detail.html # Post detail page
        ├── post_edit.html  # Post editor
        ├── dashboard.html  # User dashboard
        └── api_docs.html   # API documentation
```

## Key Components

### Models

1. **Post**
   - Core content model with title, content, author, status (draft/published)
   - Includes timestamps and tag relationships

2. **Tag**
   - Simple model for categorizing posts

3. **UserProfile**
   - Extends Django's User model
   - Defines user types (viewer/editor)

4. **APIKey**
   - Manages API access for editors
   - Includes validation to ensure only editors can have API keys

### Views

1. **Content Views**
   - Home page, post detail, tag filtering, search

2. **Editor Views**
   - Post creation, editing, publishing
   - Protected with `@editor_required` decorator

3. **User Management**
   - Signup, profile creation, user status checking

4. **API Documentation**
   - Documentation for API endpoints

### Middleware

- **UserProfileMiddleware**
  - Automatically creates profiles for authenticated users

### Template Tags

- **is_editor**
  - Helper function to check if a user has editor privileges

## Setup Instructions

### Prerequisites
- Python 3.8+
- Django 5.1+
- Database (SQLite for development, PostgreSQL recommended for production)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/TheDailyAttack.git
cd TheDailyAttack
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Access the site at http://127.0.0.1:8000/

## Usage

### For Viewers
1. Browse published posts on the home page
2. Search for specific content using the search bar
3. Filter posts by tags
4. Create an account to access additional features

### For Editors
1. Log in to your editor account
2. Access your dashboard to see your posts
3. Create new posts using the editor
4. Save posts as drafts or publish immediately
5. Edit and manage your existing posts
6. Generate an API key for programmatic access

### API Usage
1. Generate an API key from your dashboard
2. Use the key in the Authorization header for API requests
3. Refer to the API documentation for available endpoints


## Contributors

- [Sanat Kumar Jha]
```

