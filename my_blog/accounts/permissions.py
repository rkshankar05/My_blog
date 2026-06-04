def is_blog_owner(user, blog):
    # Returns True only when the logged-in user owns this blog post.
    return user.is_authenticated and blog.user == user
