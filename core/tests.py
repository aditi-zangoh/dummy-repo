import pytest
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import CommentForm, ProfileForm
from .models import Category, Comment, Post, Profile, Tag


class TestModels(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.category = Category.objects.create(
            name="Test Category", slug="test-category", description="A test category"
        )
        self.tag = Tag.objects.create(name="Test Tag", slug="test-tag")

    def test_profile_creation(self):
        profile = Profile.objects.create(
            user=self.user, bio="Test bio", location="Test City"
        )
        self.assertEqual(str(profile), f"{self.user.username}'s Profile")
        self.assertEqual(profile.bio, "Test bio")
        self.assertEqual(profile.location, "Test City")

    def test_category_creation(self):
        self.assertEqual(str(self.category), "Test Category")
        self.assertEqual(self.category.slug, "test-category")
        self.assertTrue(self.category.is_active)

    def test_post_creation(self):
        post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            author=self.user,
            category=self.category,
            content="This is a test post content.",
            excerpt="Test excerpt",
            is_published=True,
        )
        post.tags.add(self.tag)

        self.assertEqual(str(post), "Test Post")
        self.assertTrue(post.is_published)
        self.assertIsNotNone(post.published_at)
        self.assertEqual(post.views_count, 0)
        self.assertEqual(post.tags.count(), 1)

    def test_comment_creation(self):
        post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            author=self.user,
            content="Test content",
            is_published=True,
        )

        comment = Comment.objects.create(
            post=post, author=self.user, content="This is a test comment."
        )

        self.assertEqual(
            str(comment), f"Comment by {self.user.username} on {post.title}"
        )
        self.assertTrue(comment.is_approved)
        self.assertIsNone(comment.parent)


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )
        self.post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            author=self.user,
            category=self.category,
            content="This is a test post.",
            is_published=True,
            published_at=timezone.now(),
        )

    def test_home_view(self):
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to Django Blog")

    def test_post_list_view(self):
        response = self.client.get(reverse("core:post_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post")

    def test_post_detail_view(self):
        initial_views = self.post.views_count
        response = self.client.get(
            reverse("core:post_detail", kwargs={"slug": "test-post"})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post")

        # Check that view count was incremented
        self.post.refresh_from_db()
        self.assertEqual(self.post.views_count, initial_views + 1)

    def test_category_detail_view(self):
        response = self.client.get(
            reverse("core:category_detail", kwargs={"slug": "test-category"})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Category")
        self.assertContains(response, "Test Post")

    def test_search_view(self):
        response = self.client.get(reverse("core:search"), {"q": "Test"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post")

    def test_search_view_no_query(self):
        response = self.client.get(reverse("core:search"))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        response = self.client.get(reverse("core:login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")

    def test_register_view(self):
        response = self.client.get(reverse("core:register"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Register")

    def test_profile_view_requires_login(self):
        response = self.client.get(reverse("core:profile"))
        self.assertRedirects(response, "/login/?next=/profile/")

    def test_profile_view_authenticated(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("core:profile"))
        self.assertEqual(response.status_code, 200)


class TestForms(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

    def test_comment_form_valid(self):
        form_data = {"content": "This is a valid comment with enough characters."}
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_comment_form_invalid_short(self):
        form_data = {"content": "Short"}
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Comment must be at least 10 characters long.", form.errors["content"]
        )

    def test_profile_form_valid(self):
        profile = Profile.objects.create(user=self.user)
        form_data = {
            "bio": "Updated bio",
            "location": "Updated location",
            "website": "https://example.com",
            "phone": "+1234567890",
            "first_name": "Test",
            "last_name": "User",
            "email": "updated@example.com",
        }
        form = ProfileForm(data=form_data, instance=profile)
        self.assertTrue(form.is_valid())


class TestAuthentication(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

    def test_user_login(self):
        response = self.client.post(
            reverse("core:login"), {"username": "testuser", "password": "testpass123"}
        )
        self.assertRedirects(response, reverse("core:home"))

    def test_user_login_invalid(self):
        response = self.client.post(
            reverse("core:login"), {"username": "testuser", "password": "wrongpassword"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid username or password")

    def test_user_logout(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("core:logout"))
        self.assertRedirects(response, reverse("core:home"))

    def test_user_register(self):
        response = self.client.post(
            reverse("core:register"),
            {
                "username": "newuser",
                "password1": "complexpassword123",
                "password2": "complexpassword123",
            },
        )
        self.assertRedirects(response, reverse("core:login"))
        self.assertTrue(User.objects.filter(username="newuser").exists())


@pytest.mark.django_db
class TestPostModel:
    def test_post_str_representation(self):
        user = User.objects.create_user(username="testuser", password="testpass")
        post = Post(title="Test Post", author=user)
        assert str(post) == "Test Post"

    def test_post_published_at_auto_set(self):
        user = User.objects.create_user(username="testuser", password="testpass")
        post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            author=user,
            content="Test content",
            is_published=True,
        )
        assert post.published_at is not None

    def test_post_is_new_property(self):
        user = User.objects.create_user(username="testuser", password="testpass")
        post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            author=user,
            content="Test content",
            is_published=True,
            published_at=timezone.now(),
        )
        assert post.is_new is True


@pytest.mark.django_db
class TestCategoryModel:
    def test_category_str_representation(self):
        category = Category(name="Test Category")
        assert str(category) == "Test Category"

    def test_category_ordering(self):
        Category.objects.create(name="Z Category", slug="z-category")
        Category.objects.create(name="A Category", slug="a-category")

        categories = list(Category.objects.all())
        assert categories[0].name == "A Category"
        assert categories[1].name == "Z Category"


class TestAdminFunctionality(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )
        self.post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            author=self.user,
            category=self.category,
            content="Test content",
            is_published=True,
        )

    def test_category_admin_post_count(self):
        from core.admin import CategoryAdmin

        admin_instance = CategoryAdmin(Category, None)
        result = admin_instance.post_count(self.category)
        self.assertEqual(result, 1)

    def test_tag_admin_post_count(self):
        from core.admin import TagAdmin

        tag = Tag.objects.create(name="Test Tag", slug="test-tag")
        self.post.tags.add(tag)
        admin_instance = TagAdmin(Tag, None)
        result = admin_instance.post_count(tag)
        self.assertEqual(result, 1)

    def test_comment_admin_preview(self):
        from core.admin import CommentAdmin

        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content="This is a long comment that should be truncated at some point to test the preview functionality",
        )
        admin_instance = CommentAdmin(Comment, None)
        preview = admin_instance.comment_preview(comment)
        self.assertTrue(preview.endswith("..."))
        self.assertTrue(len(preview) <= 53)


class TestFormValidation(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

    def test_comment_form_clean_content(self):
        # Test valid content
        form = CommentForm(
            data={"content": "This is a valid comment with enough characters."}
        )
        self.assertTrue(form.is_valid())

        # Test content cleaning
        cleaned_content = form.cleaned_data["content"]
        self.assertEqual(
            cleaned_content, "This is a valid comment with enough characters."
        )

    def test_profile_form_initialization(self):
        profile = Profile.objects.create(user=self.user)
        self.user.first_name = "John"
        self.user.last_name = "Doe"
        self.user.email = "john@example.com"
        self.user.save()

        form = ProfileForm(instance=profile)
        self.assertEqual(form.fields["first_name"].initial, "John")
        self.assertEqual(form.fields["last_name"].initial, "Doe")
        self.assertEqual(form.fields["email"].initial, "john@example.com")

    def test_profile_form_save(self):
        profile = Profile.objects.create(user=self.user)
        form_data = {
            "bio": "Updated bio",
            "location": "New York",
            "website": "https://example.com",
            "phone": "+1234567890",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
        }
        form = ProfileForm(data=form_data, instance=profile)
        self.assertTrue(form.is_valid())

        saved_profile = form.save()
        self.user.refresh_from_db()

        self.assertEqual(saved_profile.bio, "Updated bio")
        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(self.user.last_name, "Doe")
        self.assertEqual(self.user.email, "john@example.com")


class TestModelMethods(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )

    def test_profile_get_absolute_url(self):
        profile = Profile.objects.create(user=self.user)
        with self.assertRaises(Exception):  # noqa: B017
            # This will raise NoReverseMatch since profile_detail URL doesn't exist
            profile.get_absolute_url()

    def test_category_get_absolute_url(self):
        expected_url = reverse(
            "core:category_detail", kwargs={"slug": self.category.slug}
        )
        self.assertEqual(self.category.get_absolute_url(), expected_url)

    def test_post_get_absolute_url(self):
        post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            author=self.user,
            category=self.category,
            content="Test content",
            is_published=True,
        )
        expected_url = reverse("core:post_detail", kwargs={"slug": post.slug})
        self.assertEqual(post.get_absolute_url(), expected_url)

    def test_tag_get_absolute_url(self):
        tag = Tag.objects.create(name="Test Tag", slug="test-tag")
        with self.assertRaises(Exception):  # noqa: B017
            # This will raise NoReverseMatch since tag_detail URL doesn't exist
            tag.get_absolute_url()

    def test_comment_get_absolute_url(self):
        post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            author=self.user,
            category=self.category,
            content="Test content",
            is_published=True,
        )
        comment = Comment.objects.create(
            post=post, author=self.user, content="Test comment"
        )
        expected_url = f"{post.get_absolute_url()}#comment-{comment.pk}"
        self.assertEqual(comment.get_absolute_url(), expected_url)


class TestViewsErrorHandling(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

    def test_add_comment_ajax_invalid_form(self):
        category = Category.objects.create(name="Test", slug="test")
        Post.objects.create(
            title="Test Post",
            slug="test-post",
            author=self.user,
            category=category,
            content="Test content",
            is_published=True,
        )

        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(
            reverse("core:add_comment", kwargs={"post_slug": "test-post"}),
            {"content": "short"},  # Too short, should fail validation
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["success"])
        self.assertIn("errors", data)

    def test_edit_profile_get_or_create(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("core:edit_profile"))
        self.assertEqual(response.status_code, 200)

        # Verify profile was created
        self.assertTrue(Profile.objects.filter(user=self.user).exists())


class TestCustomUserCreationForm(TestCase):
    def test_custom_user_creation_form_save(self):
        from core.forms import CustomUserCreationForm

        form_data = {
            "username": "newuser",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password1": "complexpassword123",
            "password2": "complexpassword123",
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

        user = form.save()
        self.assertEqual(user.username, "newuser")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "john@example.com")


class TestPostForm(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )

    def test_post_form_initialization(self):
        from core.forms import PostForm

        form = PostForm()
        self.assertIn("slug", form.fields)
        self.assertIn("excerpt", form.fields)
        self.assertIn("tags", form.fields)

        # Check help texts
        self.assertIn("URL-friendly", form.fields["slug"].help_text)
        self.assertIn("Brief description", form.fields["excerpt"].help_text)
        self.assertIn("Select relevant", form.fields["tags"].help_text)


class TestViewsEdgeCases(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.category = Category.objects.create(name="Test", slug="test")
        self.post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            author=self.user,
            category=self.category,
            content="Test content",
            is_published=True,
        )

    def test_add_comment_ajax_success(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(
            reverse("core:add_comment", kwargs={"post_slug": "test-post"}),
            {"content": "This is a valid comment with enough characters."},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertIn("comment", data)

    def test_add_comment_non_ajax(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(
            reverse("core:add_comment", kwargs={"post_slug": "test-post"}),
            {"content": "This is a valid comment with enough characters."},
        )

        self.assertEqual(response.status_code, 302)  # Redirect after success

    def test_add_comment_invalid_non_ajax(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(
            reverse("core:add_comment", kwargs={"post_slug": "test-post"}),
            {"content": "short"},  # Too short
        )

        self.assertEqual(response.status_code, 302)  # Redirect after error

    def test_login_view_invalid_credentials(self):
        response = self.client.post(
            reverse("core:login"), {"username": "testuser", "password": "wrongpassword"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid username or password")

    def test_login_view_form_invalid(self):
        response = self.client.post(
            reverse("core:login"),
            {"username": "", "password": ""},  # Empty username  # Empty password
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid username or password")

    def test_profile_view_creates_profile(self):
        # Delete existing profile if any
        Profile.objects.filter(user=self.user).delete()

        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("core:profile"))

        self.assertEqual(response.status_code, 200)
        # Profile should be created automatically
        self.assertTrue(Profile.objects.filter(user=self.user).exists())

    def test_edit_profile_post_invalid(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(
            reverse("core:edit_profile"),
            {
                "email": "invalid-email",  # Invalid email format
                "bio": "Test bio",
                "first_name": "Test",
                "last_name": "User",
            },
        )

        self.assertEqual(response.status_code, 200)  # Stay on form page with errors

    def test_edit_profile_post_valid(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(
            reverse("core:edit_profile"),
            {
                "email": "updated@example.com",
                "bio": "Updated bio",
                "location": "New City",
                "first_name": "Updated",
                "last_name": "User",
                "website": "https://example.com",
                "phone": "+1234567890",
            },
        )

        self.assertEqual(response.status_code, 302)  # Redirect after success

        # Verify profile was updated
        self.user.refresh_from_db()
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.bio, "Updated bio")
        self.assertEqual(profile.location, "New City")
        self.assertEqual(self.user.first_name, "Updated")


class TestModelEdgeCases(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.category = Category.objects.create(name="Test", slug="test")

    def test_post_is_new_property_no_published_date(self):
        post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            author=self.user,
            category=self.category,
            content="Test content",
            is_published=False,  # Not published, no published_at
        )

        self.assertFalse(post.is_new)  # Should return False when no published_at

    def test_tag_str_method(self):
        tag = Tag.objects.create(name="Test Tag", slug="test-tag")
        self.assertEqual(str(tag), "Test Tag")


class TestAdminQuerysets(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.category = Category.objects.create(name="Test", slug="test")
        self.post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            author=self.user,
            category=self.category,
            content="Test content",
            is_published=True,
        )
        self.comment = Comment.objects.create(
            post=self.post, author=self.user, content="Test comment"
        )

    def test_post_admin_queryset(self):
        from core.admin import PostAdmin

        admin_instance = PostAdmin(Post, None)
        queryset = admin_instance.get_queryset(None)
        # Should use select_related and prefetch_related
        self.assertTrue(queryset.query.select_related)

    def test_comment_admin_queryset(self):
        from core.admin import CommentAdmin

        admin_instance = CommentAdmin(Comment, None)
        queryset = admin_instance.get_queryset(None)
        # Should use select_related
        self.assertTrue(queryset.query.select_related)
