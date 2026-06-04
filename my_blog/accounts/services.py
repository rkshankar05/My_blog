from django.db.models import Q

from .models import Blog


def get_all_posts():
    # Used on the home page to show all blog posts.
    return Blog.objects.all()


def get_user_posts(user):
    # Used on gallery/profile pages to show only the logged-in user's posts.
    return Blog.objects.filter(user=user).order_by("-id")


def search_posts(query):
    # Return no posts if the user searches with an empty box.
    query = (query or "").strip()
    if not query:
        return Blog.objects.none()

    # Search by blog title, blog content, or author's username.
    return Blog.objects.filter(
        Q(name__icontains=query)
        | Q(messeage__icontains=query)
        | Q(user__username__icontains=query)
    )
