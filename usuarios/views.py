from django.shortcuts import render, redirect
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth



def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not senha == confirmar_senha:
            messages.add_message(request, constants.ERROR, 'As senhas não são iguais!')
            return redirect('cadastro')
        
        if len(senha) < 6:
            print(2)
            messages.add_message(request, constants.ERROR, 'A senha deve possuir pelo menos 6 caracteres')
            return redirect('cadastro')
        
        users = User.objects.filter(username=username)

        if users.exists():
            messages.add_message(request, constants.ERROR, 'Usuarios já existe')
            return redirect('cadastro')


        user = User.objects.create_user(
            username=username,
            password=senha
        )
        messages.add_message(request, constants.SUCCESS, "Usuário cadastrado com suscesso!")
        return redirect('login',)


def login(request):
    if request.method == "GET":
        print("Método GET - Exibindo página de login")
        return render(request, 'login.html')
    elif request.method == "POST":
        print("Método POST - Tentativa de login")
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        print(f"Username: {username}")
        print(f"Senha: {senha}")

        user = auth.authenticate(request, username=username, password=senha)
        print(f"Authenticated user: {user}")

        if user:
            auth.login(request, user)
            print("Login successful")
            return redirect('/empresarios/cadastrar_empresa')
        else:
            print("Login failed")
            messages.add_message(request, constants.ERROR, "Usuario ou senha inválidos")
            return redirect('login')

def logout(request):
    return redirect('login')