from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Comment, Post, Profile


class CommentForm(forms.ModelForm):
    """
    Form for creating comments
    """

    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Write your comment here...",
                    "class": "form-control",
                }
            )
        }

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if content and len(content) < 10:
            raise forms.ValidationError("Comment must be at least 10 characters long.")
        return content


class ProfileForm(forms.ModelForm):
    """
    Form for updating user profile
    """

    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = ["bio", "location", "website", "phone", "avatar"]
        widgets = {
            "bio": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Tell us about yourself...",
                    "class": "form-control",
                }
            ),
            "location": forms.TextInput(
                attrs={"placeholder": "Your location", "class": "form-control"}
            ),
            "website": forms.URLInput(
                attrs={
                    "placeholder": "https://yourwebsite.com",
                    "class": "form-control",
                }
            ),
            "phone": forms.TextInput(
                attrs={"placeholder": "+1234567890", "class": "form-control"}
            ),
            "avatar": forms.FileInput(attrs={"class": "form-control-file"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields["first_name"].initial = self.instance.user.first_name
            self.fields["last_name"].initial = self.instance.user.last_name
            self.fields["email"].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            user = profile.user
            user.first_name = self.cleaned_data["first_name"]
            user.last_name = self.cleaned_data["last_name"]
            user.email = self.cleaned_data["email"]
            user.save()
            profile.save()
        return profile


class CustomUserCreationForm(UserCreationForm):
    """
    Custom user registration form with additional fields
    """

    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class PostForm(forms.ModelForm):
    """
    Form for creating/editing posts (for future use)
    """

    class Meta:
        model = Post
        fields = [
            "title",
            "slug",
            "category",
            "content",
            "excerpt",
            "featured_image",
            "tags",
            "is_published",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "slug": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"rows": 15, "class": "form-control"}),
            "excerpt": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "featured_image": forms.FileInput(attrs={"class": "form-control-file"}),
            "tags": forms.SelectMultiple(attrs={"class": "form-control"}),
            "is_published": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[
            "slug"
        ].help_text = "URL-friendly version of the title. Leave blank to auto-generate."
        self.fields["excerpt"].help_text = "Brief description of the post (optional)."
        self.fields["tags"].help_text = "Select relevant tags for this post."
