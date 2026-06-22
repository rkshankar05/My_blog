from datetime import timedelta

from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.contrib import messages
from . models import Blog,Profile
from django.utils import timezone
import secrets
from .permissions import is_blog_owner
from .services import delete_replaced_file, get_all_posts, get_user_posts, search_posts
from .validators import validate_image

OTP_EXPIRY_MINUTES = 10
OTP_MAX_ATTEMPTS = 5

# Create your views here.
def home(request):
    blogs = get_all_posts()
    return render(request,'home.html',{"blogs":blogs})

def sigin(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, "Login successfully!")
            return redirect('home')
        else:
            messages.info(request, "Invalid username or password!")
            return redirect('login')
    return render(request, 'login.html')

def sign_up(request):
    if request.method == "POST":
        first_name = request.POST['firstname'].strip()
        last_name = request.POST['lastname'].strip()
        username = request.POST['username'].strip()
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email'].strip()

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already used")
            return redirect("signup")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("signup")

        otp = secrets.randbelow(900000) + 100000

        user = User.objects.create_user(
            username=username,
            password=password1,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_active=False,
        )
        request.session['pending_user_id'] = user.id
        request.session['otp'] = otp
        request.session['otp_created_at'] = timezone.now().isoformat()
        request.session['otp_attempts'] = 0

        send_mail(
            subject="Your OTP for Registration",
            message=f"Your OTP is {otp}",
            from_email=None,
            recipient_list=[email],
        )

        messages.success(request, "OTP sent to your email")
        return redirect("verify_otp")

    return render(request, "signup.html")


@login_required
def add_blog(request):
    if request.method =="POST":
        name = request.POST["name"].strip()
        messeage = request.POST["messeage"].strip()
        image = request.FILES.get('image')
        valid_image, image_error = validate_image(image)

        if not valid_image:
            messages.error(request, image_error)
            return redirect('add_blog')

        blog = Blog(
            user = request.user,
            name =name,
            image = image,
            messeage =messeage
        )
        blog.save()
        return redirect('gallery')

    return render(request,'blog.html')

@login_required
def gallery(request):
    blogs = get_user_posts(request.user)
    return render(request,"gallery.html",{'blogs':blogs})

@login_required
def user_logout(request):
    logout(request)

    return redirect("home")

@login_required
def edit(request,id):
    blog = Blog.objects.filter(id=id).first()
    if not blog or not is_blog_owner(request.user, blog):
        messages.error(request, "This blog was not found or you do not have permission to edit it.")
        return redirect('gallery')

    if request.method =="POST":
        name = request.POST["name"].strip()
        messeage = request.POST["messeage"].strip()
        image = request.FILES.get('image')
        old_image_name = blog.image.name
        old_image_storage = blog.image.storage

        if image:
            valid_image, image_error = validate_image(image)
            if not valid_image:
                messages.error(request, image_error)
                return redirect('edit', id=blog.id)
            blog.image = image
        blog.name = name
        blog.messeage = messeage
        blog.save()
        if image:
            delete_replaced_file(old_image_name, old_image_storage, blog.image)
        return redirect('gallery')
    
    return render(request,'edit.html',{"blog":blog})

@login_required
def delete(request,id):
    blog = Blog.objects.filter(id=id).first()
    if not blog or not is_blog_owner(request.user, blog):
        messages.error(request, "This blog was already deleted or you do not have permission to delete it.")
        return redirect('gallery')

    if request.method == "POST":
        blog.delete()
        messages.success(request, "Blog deleted successfully.")
        return redirect('gallery')

    return render(request, "delete_confirm.html", {"blog": blog})

@login_required
def profile(request):
    user = request.user
    # Get only the logged-in user's blogs
    user_blogs = get_user_posts(request.user)
    total_blogs = user_blogs.count()
    data = {
        "total": total_blogs,
        "blogs": user_blogs
    }
    return render(request, "profile.html", {"data": data})

def forget(request):
    if request.method == "POST":
        email = request.POST["email"]
        if User.objects.filter(email = email).exists():
            print("user exists")
    return render(request,"forget.html")

def search(request):
    query = request.GET.get("q", "").strip()
    results = search_posts(query)

    if query and results.exists():
        messages.info(request,"Searched Blog")
    elif query:
        messages.info(request,"No result found")
    else:
        messages.info(request,"Enter a keyword to search")
    return render(request,"search.html",{"results":results, "query":query})

@login_required
def edit_profile(request,id):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == "POST":
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            username = request.POST.get('username', '').strip()
            email = request.POST.get('email', '').strip()
            dob = request.POST.get('birthday')
            image = request.FILES.get('profile_image')
            old_profile_image_name = profile.profile_image.name
            old_profile_image_storage = profile.profile_image.storage

            if User.objects.exclude(id=user.id).filter(username=username).exists():
                messages.error(request, "Username already exists")
                return redirect('edit_profile', id=user.id)

            if User.objects.exclude(id=user.id).filter(email=email).exists():
                messages.error(request, "Email already used")
                return redirect('edit_profile', id=user.id)

            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email

            profile.dob = dob
            if image:
                valid_image, image_error = validate_image(image)
                if not valid_image:
                    messages.error(request, image_error)
                    return redirect('edit_profile', id=user.id)
                profile.profile_image = image

            user.save()
            profile.save()
            if image:
                delete_replaced_file(
                    old_profile_image_name,
                    old_profile_image_storage,
                    profile.profile_image,
                )

            return redirect('profile')
    return render(request,"edit_profile.html",{"user":user})

def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST['otp']
        session_otp = request.session.get('otp')
        pending_user_id = request.session.get('pending_user_id')
        created_at = request.session.get('otp_created_at')
        attempts = request.session.get('otp_attempts', 0)

        if not pending_user_id or not session_otp or not created_at:
            messages.error(request, "OTP session expired. Please sign up again.")
            return redirect("signup")

        if attempts >= OTP_MAX_ATTEMPTS:
            User.objects.filter(id=pending_user_id, is_active=False).delete()
            request.session.flush()
            messages.error(request, "Too many invalid OTP attempts. Please sign up again.")
            return redirect("signup")

        otp_created_at = timezone.datetime.fromisoformat(created_at)
        if timezone.now() > otp_created_at + timedelta(minutes=OTP_EXPIRY_MINUTES):
            User.objects.filter(id=pending_user_id, is_active=False).delete()
            request.session.flush()
            messages.error(request, "OTP expired. Please sign up again.")
            return redirect("signup")

        if session_otp and entered_otp == str(session_otp):
            user = get_object_or_404(User, id=pending_user_id, is_active=False)
            user.is_active = True
            user.save(update_fields=["is_active"])
            request.session.flush()

            messages.success(request, "Signup successful! Please login.")
            return redirect("login")

        else:
            request.session['otp_attempts'] = attempts + 1
            messages.error(request, "Invalid OTP")
            return redirect("verify_otp")

    if not request.session.get('pending_user_id'):
        messages.error(request, "Please sign up first.")
        return redirect("signup")

    return render(request, "verify_otp.html")

def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    back_url = request.META.get("HTTP_REFERER") or reverse("home")
    if request.get_host() not in back_url:
        back_url = reverse("home")

    context = {
        'blog': blog,
        'back_url': back_url,
    }
    return render(request, 'blog_detail.html', context)
