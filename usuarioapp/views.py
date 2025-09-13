from django.shortcuts import render, redirect
from .forms import UsuarioForm
from django.contrib.auth.views import LoginView


from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def criar_usuario(request):
    form = UsuarioForm(request.POST)
    if request.method=="POST":
        form = UsuarioForm(request.POST, request.FILES)
        if  form.is_valid():
            obj=form.save()
            obj.save()
            return redirect('login')
    return render(request, 'usuarios/usuario.html',{'form':form})



