from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth import login as auth_login

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Logado com sucesso!')
            return redirect('/listar_contato/')  # <-- use o caminho direto
        else:
            messages.error(request, 'E-mail ou senha incorreta!')

    return render(request, 'accounts/login.html')

