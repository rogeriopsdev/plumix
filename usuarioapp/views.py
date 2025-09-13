from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def criar_usuario(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuário criado com sucesso. Faça login para continuar.")
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "usuarios/usuario.html", {"form": form})
