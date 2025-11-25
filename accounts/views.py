from django.shortcuts import render, redirect
from accounts.models import *
from django.http import Http404
from accounts.forms import *
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from accounts.utils import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from core.decorators import *
from django.conf import settings

# # # # # # # # # # # # # # # # # #
      # Admin User List #
# # # # # # # # # # # # # # # # # #
@login_required(login_url='logIn')
@admin_role_required
def usersList(request):
        users = UserProfile.objects.all()
        context = {
            'title': 'Users',
            'users': users,
        }
        return render(request, 'authenticate/user/users.html', context)

# # # # # # # # # # # # # # # # # #
    # Admin User Edit #
# # # # # # # # # # # # # # # # # #
@login_required(login_url='logIn')
@admin_role_required
def editUserProfile(request, id):
    try:
        profile = UserProfile.objects.get(id=id)
        user = profile.user
    except UserProfile.DoesNotExist:
        raise Http404("User profile does not exist")

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('editUserProfile', user.id)
    else:
        form = UserProfileForm(instance=profile)

    context = {
        'title': 'Edit User Profile',
        'form': form,
        'profile': profile,
        'user': user,
    }
    return render(request, 'authenticate/user/edit.html', context)

# # # # # # # # # # # # # # # # # #
    # Admin User Create #
# # # # # # # # # # # # # # # # # #
@login_required(login_url='logIn')
@admin_role_required
def createUser(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Prevent immediate save
            user.role = form.cleaned_data['role']  # Set role from form
            user.save()  # Save User instance to DB

            # Update or Create a profile for the user
            UserProfile.objects.update_or_create(
                user=user, 
                defaults={
                    'name': form.cleaned_data['name'], 
                    'email': form.cleaned_data['email']
                }
            )

            return redirect('userList')
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()

    context = {
        'title': 'Create User',
        'form': form,
    }
    return render(request, 'authenticate/user/create.html', context)

# # # # # # # # # # # # # # # # # #
    # Admin User Password #
# # # # # # # # # # # # # # # # # #
@login_required(login_url='logIn')
@admin_role_required
def changePassword(request, id):

    user = User.objects.get(id=id)
    profile = UserProfile.objects.get(user=user)

    if request.method == 'POST':
        form = UserPasswordChangeForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully.')
            return redirect('changePassword', user.id)
    else:
        form = UserPasswordChangeForm(user)

    context = {
        'title': 'Change Password',
        'form': form,
        'profile': profile,
        'user': user,
    }
    return render(request, 'authenticate/user/password.html', context)

# # # # # # # # # # # # # # # # # #
    # Admin Delete User #
# # # # # # # # # # # # # # # # # #
@login_required(login_url='logIn')
@admin_role_required
def deleteUser(request, id):
    try:
        user = User.objects.get(id=id)
        profile = UserProfile.objects.get(user=user)
        user.delete()
        profile.delete()
    except User.DoesNotExist:
        raise Http404("User does not exist")

    return redirect('userList')

# # # # # # # # # # # # # # # # # #
       # Reset Password #
# # # # # # # # # # # # # # # # # #
def initiate_password_reset(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username) 
            generate_reset_token_and_send_email(user, request)
            messages.success(request, 'An email has sent!')
            return redirect('initiate_password_reset') 
        except User.DoesNotExist:
            messages.warning(request, 'Invalid username!')
            return redirect('initiate_password_reset')
    context = {
        'title' : 'Forgot Password'
    }
    return render(request, 'authenticate/auth/forgotpassword.html', context)

def reset_password(request, token):
    try:
        password_reset_token = PasswordResetToken.objects.get(token=token)
        if password_reset_token.is_expired():
            messages.warning(request, 'The password reset token has expired. Please initiate the password reset process again.')
            return redirect('password_reset') 

        if request.method == 'POST':
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')
            if new_password1 == new_password2:

                user = password_reset_token.user
                user.set_password(new_password1)
                user.save()
                
                update_session_auth_hash(request, user)
                
                password_reset_token.delete()
                messages.success(request, 'Password reset successfully!')
                return redirect('/') 
            else:
                messages.warning(request, 'Passwords did not match. Please try again.')
                return redirect('reset_password', token=token)
        context = {
            'title' : 'Reset Password'
        }
        return render(request, 'authenticate/auth/reset.html', context)
    except PasswordResetToken.DoesNotExist:
        messages.warning(request, 'Invalid token. Please ensure you have the correct link.')
        return redirect('initiate_password_reset')
    except Exception as e:
        messages.warning(request, f'An error occurred: {str(e)}')
        return redirect('/')

# # # # # # # # # # # # # # # # # #
          # Login #
# # # # # # # # # # # # # # # # # #
def logIn(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('login[password]')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('adminHome')
            else:
                messages.warning(request, 'Invalid username or password!')
                return redirect('logIn')
        
        else:
            demo_mode = True if 'core.middleware.middleware.DemoModeMiddleware' in settings.MIDDLEWARE else False
            context = {
                'title' : 'Log In',
                'demo_mode' : demo_mode
            }
            return render(request, 'authenticate/auth/login.html', context)
    else:
        return redirect('adminHome')

# # # # # # # # # # # # # # # # # #
          # LogOut #
# # # # # # # # # # # # # # # # # #
@login_required(login_url='signIn')
def LogOut(request):
    logout(request)
    messages.success(request, 'Logout successfully!')
    return redirect('logIn')
    
def error_404(request, exception):
    return render(request, 'error/404.html', status=404)