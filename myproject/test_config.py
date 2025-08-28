from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse


class TestProjectConfiguration(TestCase):
    def test_settings_configuration(self):
        """Test that settings are properly configured"""
        self.assertIn("core", settings.INSTALLED_APPS)
        self.assertIn("django.contrib.admin", settings.INSTALLED_APPS)
        self.assertIn("django.contrib.auth", settings.INSTALLED_APPS)

        self.assertTrue(hasattr(settings, "SECRET_KEY"))
        self.assertTrue(hasattr(settings, "DEBUG"))
        self.assertTrue(hasattr(settings, "DATABASES"))

    def test_url_patterns(self):
        """Test that URL patterns resolve correctly"""
        # Test admin URL
        admin_url = reverse("admin:index")
        self.assertEqual(admin_url, "/admin/")

        # Test core URLs
        home_url = reverse("core:home")
        self.assertEqual(home_url, "/")

        posts_url = reverse("core:post_list")
        self.assertEqual(posts_url, "/posts/")

    def test_static_and_media_settings(self):
        """Test static and media file configurations"""
        self.assertTrue(hasattr(settings, "STATIC_URL"))
        self.assertTrue(hasattr(settings, "STATIC_ROOT"))
        self.assertTrue(hasattr(settings, "MEDIA_URL"))
        self.assertTrue(hasattr(settings, "MEDIA_ROOT"))

        self.assertEqual(settings.STATIC_URL, "/static/")
        self.assertEqual(settings.MEDIA_URL, "/media/")


class TestURLConfiguration(TestCase):
    def setUp(self):
        self.client = Client()

    def test_admin_accessible(self):
        """Test that admin interface is accessible"""
        response = self.client.get("/admin/")
        # Should redirect to login or show admin page
        self.assertIn(response.status_code, [200, 302])

    def test_debug_static_urls(self):
        """Test that debug static URL patterns are set up correctly"""
        if settings.DEBUG:
            # In debug mode, static files should be served
            response = self.client.get("/static/test.css")
            # File doesn't exist, but URL pattern should be there (404 is expected)
            self.assertEqual(response.status_code, 404)

            response = self.client.get("/media/test.jpg")
            # File doesn't exist, but URL pattern should be there (404 is expected)
            self.assertEqual(response.status_code, 404)


class TestWSGIConfiguration(TestCase):
    def test_wsgi_module_importable(self):
        """Test that WSGI module can be imported"""
        try:
            from myproject.wsgi import application

            self.assertIsNotNone(application)
        except ImportError:
            self.fail("WSGI application could not be imported")


class TestASGIConfiguration(TestCase):
    def test_asgi_module_importable(self):
        """Test that ASGI module can be imported"""
        try:
            from myproject.asgi import application

            self.assertIsNotNone(application)
        except ImportError:
            self.fail("ASGI application could not be imported")
