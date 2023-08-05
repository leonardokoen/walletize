from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.http import HttpResponse
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        print("Trying....")
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, f'Account created for {email}!')
            return redirect('login')
        else:
            print("Errors:")
            print(form.errors.as_data())
            return redirect('/register')

    else:
        form = RegisterForm()
    return render(request, 'core/templates/register.html', {'form': form})


# Create your views here.
# def register(request):
#     if request.method == 'GET':
#         form = RegisterForm()
#         return render(request, 'core/templates/register.html', { 'form': form})
#     if request.method == 'POST':
#         # form = RegisterForm(request.POST)
#         # print(form.data) 
#         data = request.POST
#         first_name = data["firstName"]    
#         # if form.is_valid():
#         #     user = form.save()
#         #     messages.success(request, 'You have singed up successfully.') 
#         return HttpResponse(status=200)