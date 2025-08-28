#!/usr/bin/env python
import os
from datetime import timedelta

import django
from django.utils import timezone

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from django.contrib.auth.models import User  # noqa: E402

from core.models import Category, Comment, Post, Profile, Tag  # noqa: E402


def create_sample_data():
    print("Creating sample data...")

    # Create users
    if not User.objects.filter(username="john_doe").exists():
        john = User.objects.create_user(
            username="john_doe",
            email="john@example.com",
            password="password123",
            first_name="John",
            last_name="Doe",
        )
        Profile.objects.create(
            user=john,
            bio="A passionate writer and Django enthusiast. Love sharing knowledge about web development.",
            location="New York, USA",
            website="https://johndoe.dev",
        )
        print("Created user: john_doe")

    if not User.objects.filter(username="jane_smith").exists():
        jane = User.objects.create_user(
            username="jane_smith",
            email="jane@example.com",
            password="password123",
            first_name="Jane",
            last_name="Smith",
        )
        Profile.objects.create(
            user=jane,
            bio="Software engineer and tech blogger. Interested in AI and machine learning.",
            location="San Francisco, CA",
            website="https://janesmith.tech",
        )
        print("Created user: jane_smith")

    # Get users
    john = User.objects.get(username="john_doe")
    jane = User.objects.get(username="jane_smith")
    admin = User.objects.get(username="admin")

    # Create categories
    categories_data = [
        (
            "Web Development",
            "web-development",
            "Articles about web development, frameworks, and best practices.",
        ),
        ("Python", "python", "Everything related to Python programming language."),
        ("Django", "django", "Django framework tutorials, tips, and tricks."),
        (
            "JavaScript",
            "javascript",
            "JavaScript programming and modern web technologies.",
        ),
        ("Technology", "technology", "Latest trends and news in technology."),
    ]

    categories = []
    for name, slug, desc in categories_data:
        category, created = Category.objects.get_or_create(
            name=name, slug=slug, defaults={"description": desc}
        )
        categories.append(category)
        if created:
            print(f"Created category: {name}")

    # Create tags
    tags_data = [
        "beginner",
        "tutorial",
        "advanced",
        "tips",
        "best-practices",
        "framework",
        "backend",
        "frontend",
        "api",
        "database",
        "security",
        "performance",
        "deployment",
        "testing",
        "debugging",
    ]

    tags = []
    for tag_name in tags_data:
        tag, created = Tag.objects.get_or_create(name=tag_name, slug=tag_name)
        tags.append(tag)
        if created:
            print(f"Created tag: {tag_name}")

    # Create posts
    posts_data = [
        {
            "title": "Getting Started with Django: A Complete Beginner's Guide",
            "slug": "getting-started-django-complete-beginners-guide",
            "author": john,
            "category": categories[2],  # Django
            "content": """
Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. In this comprehensive guide, we'll walk through everything you need to know to get started with Django development.

## What is Django?

Django is a free and open-source web framework written in Python. It follows the model-template-view (MTV) architectural pattern and emphasizes the principle of "Don't Repeat Yourself" (DRY).

## Setting Up Your Development Environment

Before we start building with Django, we need to set up our development environment:

1. **Install Python**: Make sure you have Python 3.8 or later installed
2. **Create a virtual environment**: `python -m venv myenv`
3. **Activate the virtual environment**: `source myenv/bin/activate` (Linux/Mac) or `myenv\\Scripts\\activate` (Windows)
4. **Install Django**: `pip install django`

## Creating Your First Django Project

Once Django is installed, you can create your first project:

```bash
django-admin startproject mysite
cd mysite
python manage.py runserver
```

This will create a new Django project and start the development server on http://127.0.0.1:8000/.

## Understanding Django's Structure

Django projects are organized into apps, which are Python packages that contain models, views, templates, and other components for a specific functionality.

## Next Steps

In the following tutorials, we'll explore Django's key concepts including models, views, templates, and URL routing. Stay tuned for more advanced topics!
            """,
            "excerpt": "Learn Django from scratch with this comprehensive beginner's guide. We'll cover installation, project setup, and key concepts.",
            "tags": [0, 1, 5],  # beginner, tutorial, framework
            "is_published": True,
            "published_at": timezone.now() - timedelta(days=5),
        },
        {
            "title": "Django Models Deep Dive: Advanced Database Relationships",
            "slug": "django-models-deep-dive-advanced-database-relationships",
            "author": jane,
            "category": categories[2],  # Django
            "content": """
Django's Object-Relational Mapping (ORM) is one of its most powerful features. In this article, we'll explore advanced database relationships and how to optimize your Django models for better performance.

## Understanding Django Model Relationships

Django provides several types of relationships between models:

### One-to-One Relationships

One-to-one relationships are used when one model extends another. For example, a User model might have a one-to-one relationship with a Profile model.

```python
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    avatar = models.ImageField(upload_to='avatars/')
```

### Foreign Key Relationships

Foreign keys create a many-to-one relationship. Many posts can belong to one category:

```python
class Post(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    content = models.TextField()
```

### Many-to-Many Relationships

Many-to-many relationships allow multiple instances of one model to be related to multiple instances of another:

```python
class Post(models.Model):
    title = models.CharField(max_length=200)
    tags = models.ManyToManyField(Tag, blank=True)
```

## Performance Optimization

When working with relationships, it's important to optimize your queries:

- Use `select_related()` for foreign key and one-to-one relationships
- Use `prefetch_related()` for many-to-many and reverse foreign key relationships
- Consider database indexes for frequently queried fields

## Conclusion

Understanding Django's relationship types and optimization techniques is crucial for building efficient web applications. Practice these concepts in your next Django project!
            """,
            "excerpt": "Master Django model relationships and learn optimization techniques for better database performance.",
            "tags": [2, 9, 11],  # advanced, database, performance
            "is_published": True,
            "published_at": timezone.now() - timedelta(days=3),
        },
        {
            "title": "Modern JavaScript ES6+ Features Every Developer Should Know",
            "slug": "modern-javascript-es6-features-every-developer-should-know",
            "author": john,
            "category": categories[3],  # JavaScript
            "content": """
JavaScript has evolved significantly since ES6 (ECMAScript 2015). In this article, we'll explore the most important modern JavaScript features that every developer should master.

## Arrow Functions

Arrow functions provide a concise way to write function expressions:

```javascript
// Traditional function
function add(a, b) {
    return a + b;
}

// Arrow function
const add = (a, b) => a + b;
```

## Template Literals

Template literals make string interpolation and multi-line strings much easier:

```javascript
const name = 'John';
const age = 30;

const message = `Hello, my name is ${name} and I'm ${age} years old.`;
```

## Destructuring Assignment

Destructuring allows you to extract values from arrays and objects:

```javascript
// Array destructuring
const [first, second] = [1, 2, 3];

// Object destructuring
const {name, age} = {name: 'John', age: 30, city: 'New York'};
```

## Async/Await

Async/await makes working with promises much more readable:

```javascript
async function fetchData() {
    try {
        const response = await fetch('/api/data');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}
```

## Modules

ES6 modules allow you to organize your code into separate files:

```javascript
// math.js
export const add = (a, b) => a + b;
export const multiply = (a, b) => a * b;

// main.js
import { add, multiply } from './math.js';
```

## Conclusion

These ES6+ features make JavaScript code more readable, maintainable, and powerful. Start incorporating them into your projects today!
            """,
            "excerpt": "Discover the most important modern JavaScript features including arrow functions, async/await, and destructuring.",
            "tags": [7, 1, 4],  # frontend, tutorial, best-practices
            "is_published": True,
            "published_at": timezone.now() - timedelta(days=2),
        },
        {
            "title": "Python Best Practices: Writing Clean and Maintainable Code",
            "slug": "python-best-practices-writing-clean-maintainable-code",
            "author": jane,
            "category": categories[1],  # Python
            "content": '''
Writing clean, maintainable Python code is essential for long-term project success. In this article, we'll explore best practices that will make your Python code more professional and easier to maintain.

## Follow PEP 8

PEP 8 is the official style guide for Python code. Following it ensures your code is consistent and readable:

```python
# Good
def calculate_total_price(items):
    total = 0
    for item in items:
        total += item.price
    return total

# Bad
def calculateTotalPrice(items):
    total=0
    for item in items:total+=item.price
    return total
```

## Use Meaningful Variable Names

Choose descriptive names that explain the purpose of variables and functions:

```python
# Good
user_count = len(users)
is_authenticated = check_user_authentication(user)

# Bad
c = len(users)
flag = check_user_authentication(user)
```

## Write Docstrings

Document your functions and classes with clear docstrings:

```python
def calculate_compound_interest(principal, rate, time, compound_frequency):
    """
    Calculate compound interest.

    Args:
        principal (float): Initial amount of money
        rate (float): Annual interest rate (as decimal)
        time (int): Time period in years
        compound_frequency (int): Number of times interest is compounded per year

    Returns:
        float: Final amount after compound interest
    """
    return principal * (1 + rate/compound_frequency) ** (compound_frequency * time)
```

## Use List Comprehensions Wisely

List comprehensions are Pythonic, but don't overuse them:

```python
# Good - simple and readable
squares = [x**2 for x in range(10)]

# Good - with condition
even_squares = [x**2 for x in range(10) if x % 2 == 0]

# Bad - too complex
result = [process(x) for sublist in nested_list for x in sublist if condition(x)]
```

## Handle Exceptions Properly

Use specific exception types and provide meaningful error messages:

```python
try:
    result = risky_operation()
except ValueError as e:
    logger.error(f"Invalid value provided: {e}")
    raise
except ConnectionError as e:
    logger.error(f"Connection failed: {e}")
    return None
```

## Conclusion

Following these best practices will make your Python code more professional, readable, and maintainable. Remember, code is read more often than it's written!
            ''',
            "excerpt": "Learn essential Python best practices for writing clean, maintainable code that follows industry standards.",
            "tags": [4, 13, 1],  # best-practices, testing, tutorial
            "is_published": True,
            "published_at": timezone.now() - timedelta(days=1),
        },
        {
            "title": "Building RESTful APIs with Django REST Framework",
            "slug": "building-restful-apis-django-rest-framework",
            "author": john,
            "category": categories[0],  # Web Development
            "content": """
Django REST Framework (DRF) is a powerful toolkit for building Web APIs in Django. In this tutorial, we'll learn how to create a RESTful API from scratch.

## Installation and Setup

First, install Django REST Framework:

```bash
pip install djangorestframework
```

Add it to your INSTALLED_APPS:

```python
INSTALLED_APPS = [
    # ... other apps
    'rest_framework',
]
```

## Creating Serializers

Serializers convert Django models to JSON and vice versa:

```python
from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at']
        read_only_fields = ['author', 'created_at']
```

## Creating API Views

Use DRF's class-based views for quick API development:

```python
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Post
from .serializers import PostSerializer

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
```

## URL Configuration

Configure your API endpoints:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('api/posts/', views.PostListCreateView.as_view(), name='post-list'),
    path('api/posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
]
```

## Authentication and Permissions

DRF provides various authentication and permission options:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}
```

## Testing Your API

Test your API endpoints:

```python
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Post

class PostAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.post = Post.objects.create(title='Test Post', content='Test content', author=self.user)

    def test_get_post_list(self):
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, 200)
```

## Conclusion

Django REST Framework makes building APIs straightforward and follows Django's "batteries included" philosophy. Start building your APIs today!
            """,
            "excerpt": "Learn how to build RESTful APIs using Django REST Framework with serializers, views, and authentication.",
            "tags": [8, 1, 6],  # api, tutorial, backend
            "is_published": True,
            "published_at": timezone.now() - timedelta(hours=12),
        },
        {
            "title": "The Future of Web Development: Trends to Watch in 2024",
            "slug": "future-web-development-trends-2024",
            "author": jane,
            "category": categories[4],  # Technology
            "content": """
Web development is constantly evolving. As we move through 2024, several trends are shaping the future of how we build web applications. Let's explore the most significant developments.

## Progressive Web Apps (PWAs)

PWAs continue to blur the line between web and mobile apps:

- Offline functionality
- Push notifications
- App-like experience
- Installation without app stores

## WebAssembly (WASM)

WebAssembly is bringing near-native performance to the web:

- Run code written in multiple languages
- High-performance applications in browsers
- Gaming and multimedia applications
- Scientific computing on the web

## Jamstack Architecture

The Jamstack approach is becoming mainstream:

- **J**avaScript for dynamic functionality
- **A**PIs for backend services
- **M**arkup pre-built at deploy time

Benefits include better performance, security, and scalability.

## AI and Machine Learning Integration

AI is being integrated into web development:

- Intelligent chatbots and customer service
- Personalized user experiences
- Automated content generation
- Voice and image recognition

## Micro-Frontends

Large applications are being broken down into smaller, manageable pieces:

- Independent deployment
- Technology diversity
- Team autonomy
- Better scalability

## Web3 and Blockchain Integration

Decentralized web technologies are gaining traction:

- Cryptocurrency payments
- NFT marketplaces
- Decentralized identity
- Smart contracts

## Improved Developer Experience

Tools and frameworks are focusing on developer productivity:

- Hot reloading and fast refresh
- Better debugging tools
- Improved TypeScript integration
- Enhanced build tools (Vite, esbuild)

## Conclusion

The web development landscape is exciting and rapidly changing. Stay curious, keep learning, and experiment with these new technologies to stay ahead of the curve.
            """,
            "excerpt": "Explore the latest trends shaping web development in 2024, from PWAs to WebAssembly and AI integration.",
            "tags": [4, 7, 8],  # best-practices, frontend, api
            "is_published": True,
            "published_at": timezone.now() - timedelta(hours=6),
        },
    ]

    for i, post_data in enumerate(posts_data):
        post, created = Post.objects.get_or_create(
            title=post_data["title"],
            defaults={
                "slug": post_data["slug"],
                "author": post_data["author"],
                "category": post_data["category"],
                "content": post_data["content"],
                "excerpt": post_data["excerpt"],
                "is_published": post_data["is_published"],
                "published_at": post_data["published_at"],
            },
        )

        if created:
            # Add tags
            for tag_index in post_data["tags"]:
                post.tags.add(tags[tag_index])

            # Add some view counts
            post.views_count = (i + 1) * 15
            post.save()

            print(f"Created post: {post_data['title']}")

    # Create some comments
    posts = Post.objects.filter(is_published=True)
    for post in posts[:3]:  # Add comments to first 3 posts
        Comment.objects.get_or_create(
            post=post,
            author=admin,
            content=f"Great article about {post.category.name}! Thanks for sharing.",
            defaults={"is_approved": True},
        )

        Comment.objects.get_or_create(
            post=post,
            author=john if post.author != john else jane,
            content="I found this really helpful. Looking forward to more content like this.",
            defaults={"is_approved": True},
        )

    print("Sample data creation completed!")
    print(f"Created {User.objects.count()} users")
    print(f"Created {Category.objects.count()} categories")
    print(f"Created {Tag.objects.count()} tags")
    print(f"Created {Post.objects.count()} posts")
    print(f"Created {Comment.objects.count()} comments")


if __name__ == "__main__":
    create_sample_data()
