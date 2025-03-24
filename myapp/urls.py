from django.urls import path
from .views import index, blogs, blog_create, login_signup_view, logout_view, save_blog



   

urlpatterns = [
    path('', index, name='index'),
    path('blogs/', blogs, name='blogs'),
    path('blog_create/', blog_create, name='blog_create'),
    path('login/', login_signup_view, name='login'),  # Handle both login & signup
    path('logout/', logout_view, name='logout'),
    path('save-blog/', save_blog, name='save_blog'),

]
