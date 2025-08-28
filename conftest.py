import django
import pytest
from django.conf import settings


def pytest_configure(config):  # noqa: ARG001
    """Configure Django for pytest"""
    if not settings.configured:
        settings.configure(
            DEBUG=True,
            DATABASES={
                "default": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": ":memory:",
                }
            },
            INSTALLED_APPS=[
                "django.contrib.admin",
                "django.contrib.auth",
                "django.contrib.contenttypes",
                "django.contrib.sessions",
                "django.contrib.messages",
                "django.contrib.staticfiles",
                "core",
            ],
            MIDDLEWARE=[
                "django.middleware.security.SecurityMiddleware",
                "django.contrib.sessions.middleware.SessionMiddleware",
                "django.middleware.common.CommonMiddleware",
                "django.middleware.csrf.CsrfViewMiddleware",
                "django.contrib.auth.middleware.AuthenticationMiddleware",
                "django.contrib.messages.middleware.MessageMiddleware",
                "django.middleware.clickjacking.XFrameOptionsMiddleware",
            ],
            ROOT_URLCONF="core.urls",
            TEMPLATES=[
                {
                    "BACKEND": "django.template.backends.django.DjangoTemplates",
                    "DIRS": [],
                    "APP_DIRS": True,
                    "OPTIONS": {
                        "context_processors": [
                            "django.template.context_processors.debug",
                            "django.template.context_processors.request",
                            "django.contrib.auth.context_processors.auth",
                            "django.contrib.messages.context_processors.messages",
                        ],
                    },
                },
            ],
            SECRET_KEY="test-key",
            USE_TZ=True,
            LOGIN_URL="/login/",
        )
    django.setup()


@pytest.fixture
def user():
    """Create a test user"""
    from django.contrib.auth.models import User

    return User.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )


@pytest.fixture
def category():
    """Create a test category"""
    from core.models import Category

    return Category.objects.create(
        name="Test Category", slug="test-category", description="A test category"
    )


@pytest.fixture
def tag():
    """Create a test tag"""
    from core.models import Tag

    return Tag.objects.create(name="Test Tag", slug="test-tag")


@pytest.fixture
def post(user, category):
    """Create a test post"""
    from core.models import Post

    return Post.objects.create(
        title="Test Post",
        slug="test-post",
        author=user,
        category=category,
        content="This is test content",
        excerpt="Test excerpt",
        is_published=True,
    )


@pytest.fixture
def profile(user):
    """Create a test profile"""
    from core.models import Profile

    return Profile.objects.create(user=user, bio="Test bio", location="Test City")
