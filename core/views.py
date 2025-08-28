from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from django.views.generic import DetailView, ListView

from .forms import CommentForm, ProfileForm
from .models import Category, Post, Profile


def home(request):
    """
    Homepage view with featured posts
    """
    featured_posts = (
        Post.objects.filter(is_published=True)
        .select_related("author", "category")
        .prefetch_related("tags")[:6]
    )

    recent_posts = Post.objects.filter(is_published=True).select_related(
        "author", "category"
    )[:5]

    categories = Category.objects.filter(is_active=True).annotate(
        post_count=Count("posts")
    )

    context = {
        "featured_posts": featured_posts,
        "recent_posts": recent_posts,
        "categories": categories,
    }
    return render(request, "core/home.html", context)


class PostListView(ListView):
    """
    Class-based view for listing posts with pagination
    """

    model = Post
    template_name = "core/post_list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        return (
            Post.objects.filter(is_published=True)
            .select_related("author", "category")
            .prefetch_related("tags")
        )


class PostDetailView(DetailView):
    """
    Class-based view for displaying a single post
    """

    model = Post
    template_name = "core/post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        return Post.objects.filter(is_published=True).select_related(
            "author", "category"
        )

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        post.views_count += 1
        post.save(update_fields=["views_count"])
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = (
            self.object.comments.filter(is_approved=True, parent=None)
            .select_related("author")
            .prefetch_related("replies")
        )
        context["comment_form"] = CommentForm()
        context["related_posts"] = Post.objects.filter(
            category=self.object.category, is_published=True
        ).exclude(pk=self.object.pk)[:3]
        return context


class CategoryDetailView(DetailView):
    """
    View for displaying posts in a specific category
    """

    model = Category
    template_name = "core/category_detail.html"
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.filter(
            category=self.object, is_published=True
        ).select_related("author", "category")

        paginator = Paginator(posts, 10)
        page_number = self.request.GET.get("page")
        context["posts"] = paginator.get_page(page_number)
        return context


def search_posts(request):
    """
    Search functionality for posts
    """
    query = request.GET.get("q", "")
    posts = Post.objects.none()

    if query:
        posts = (
            Post.objects.filter(
                Q(title__icontains=query)
                | Q(content__icontains=query)
                | Q(excerpt__icontains=query),
                is_published=True,
            )
            .select_related("author", "category")
            .distinct()
        )

    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    posts_page = paginator.get_page(page_number)

    context = {
        "posts": posts_page,
        "query": query,
        "total_results": posts.count() if query else 0,
    }
    return render(request, "core/search_results.html", context)


@login_required
@require_http_methods(["POST"])
def add_comment(request, post_slug):
    """
    Add comment to a post (AJAX)
    """
    post = get_object_or_404(Post, slug=post_slug, is_published=True)
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse(
                {
                    "success": True,
                    "comment": {
                        "author": comment.author.username,
                        "content": comment.content,
                        "created_at": comment.created_at.strftime(
                            "%B %d, %Y at %I:%M %p"
                        ),
                    },
                }
            )
        messages.success(request, "Your comment has been added!")
    else:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": False, "errors": form.errors})
        messages.error(request, "There was an error with your comment.")

    return redirect("core:post_detail", slug=post_slug)


def register_view(request):
    """
    User registration view
    """
    if request.method == "POST":
        form: UserCreationForm = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}!")
            return redirect("core:login")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})


def login_view(request):
    """
    User login view
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("core:home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})


def logout_view(request):
    """
    User logout view
    """
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("core:home")


@login_required
def profile_view(request):
    """
    User profile view
    """
    profile, created = Profile.objects.get_or_create(user=request.user)
    user_posts = Post.objects.filter(author=request.user).select_related("category")

    context = {
        "profile": profile,
        "user_posts": user_posts,
    }
    return render(request, "core/profile.html", context)


@login_required
def edit_profile(request):
    """
    Edit user profile view
    """
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect("core:profile")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "core/edit_profile.html", {"form": form})
