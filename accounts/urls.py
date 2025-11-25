from django.urls import path
from accounts.views import *

urlpatterns = [
    path('admin/users/user-list', usersList, name="userList"),
    path('admin/user/create', createUser, name="createUser"),
    path('admin/edit-profile/<int:id>', editUserProfile, name='editUserProfile'),
    path('admin/user/change-password/<int:id>', changePassword, name='changePassword'),
    path('admin/user/delete/<int:id>', deleteUser, name='deleteUser'),

    path('forgot-password/', initiate_password_reset, name='initiate_password_reset'),
    path('reset_password/<uuid:token>/', reset_password, name='reset_password'),

    path('login/', logIn, name='logIn'),
    path('logout/', LogOut, name='LogOut'),
]
