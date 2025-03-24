from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Blog
import json
from datetime import datetime


#   Login/Signup View
def login_signup_view(request):
    if request.method == "POST":
        action = request.POST.get('action')

        # Handle Signup
        if action == "signup":
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists. Try another!")
                return redirect('login')

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists. Try another!")
                return redirect('login')

            # Create new user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')

        # Handle Login
        elif action == "login":
            email = request.POST.get('email')
            password = request.POST.get('password')

            try:
                username = User.objects.get(email=email).username
                user = authenticate(request, username=username, password=password)

                if user is not None:
                    login(request, user)
                    messages.success(request, "Login successful!")
                    return redirect('index')
                else:
                    messages.error(request, "Invalid email or password.")
                    return redirect('login')

            except User.DoesNotExist:
                messages.error(request, "Invalid email or password.")
                return redirect('login')

    return render(request, 'myapp/login.html')


#   Logout View
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('index')


#   Home Page View
def index(request):
    return render(request, 'myapp/index.html')


#   Save Blog Data (Using Quill Data)
@csrf_exempt
@login_required
def save_blog(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # Create and save the blog
            blog = Blog.objects.create(
                author=request.user,
                title=data.get('title'),
                content=data.get('content'),
                labels=data.get('labels'),
                publish_date=datetime.strptime(data.get('publishDate'), '%Y-%m-%d').date(),
                publish_time=datetime.strptime(data.get('publishTime'), '%H:%M:%S').time(),
                permalink=data.get('permalink'),
                location=data.get('location')
            )
            blog.save()

            return JsonResponse({"status": "success", "message": "Blog published successfully!"})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid request method"})


#   Blog List View
def blogs(request):
    all_blogs = Blog.objects.all().order_by("-created_at")  # Order by newest first
    return render(request, "myapp/blogs.html", {"blogs": all_blogs})


#   Create Blog View (Optional - For Non-JS Based Creation)
@login_required
def blog_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        labels = request.POST.get("labels")
        publish_date = request.POST.get("publish_date")
        publish_time = request.POST.get("publish_time")
        permalink = request.POST.get("permalink")
        location = request.POST.get("location")

        if not title or not content:
            messages.error(request, "Title and content cannot be empty.")
            return redirect("blog_create")

        # Create and save blog
        Blog.objects.create(
            author=request.user,
            title=title,
            content=content,
            labels=labels,
            publish_date=publish_date,
            publish_time=publish_time,
            permalink=permalink,
            location=location,
        )
        messages.success(request, "Blog posted successfully!")
        return redirect("blogs")

    return render(request, "myapp/blog_create.html")
