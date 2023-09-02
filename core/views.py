from django.contrib.auth import login
from django.shortcuts import render, redirect

from .forms import SignUpForm


# Home page view
def frontpage(request):
    return render(request, 'core/frontpage.html')


# Sign up view
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect('frontpage')
    else:
        form = SignUpForm()

    return render(request, 'core/signup.html', {'form': form})


# Custom error handling view , redirecting any error to custom page
def custom_404(request, exception, template_name='core/404.html'):
    return render(request, template_name)
