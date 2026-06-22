import logging

from django.db.models import Q

from .models import Blog

logger = logging.getLogger(__name__)


def delete_replaced_file(old_name, storage, new_file):
    if not old_name or not storage or not new_file:
        return

    if old_name != new_file.name:
        try:
            storage.delete(old_name)
        except Exception:
            logger.exception("Failed to delete replaced file: %s", old_name)


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
