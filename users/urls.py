from django.urls import path
from .views import home_view, signup_view , login_view , dashboard, logout_view,profile_view, profile_edit, delete_account,member_list, member_detail

urlpatterns = [
    path('', home_view, name='home'),   
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('profile/delete/', delete_account, name='delete_account'),
    path('members/', member_list, name='member_list'),
    path('members/<int:member_id>/', member_detail, name='member_detail'),
]

