from django.http import HttpResponseRedirect
from django.db import models
from django.shortcuts import render, redirect
from historia.forms import *
from historia.models import *
from historia.processo_migracao import *
from django.conf import settings

# Imaginary function to handle an uploaded file.
#from somewhere import handle_uploaded_file

def home(request):
    return render(request, 'home.html')

def loading():
    return render('loading.html')

def migracao(request):
    if request.method == 'POST':
        form = MigracaoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            if form['apagar_dados'].value():
                apagar_geral()
            if not settings.DEBUG:
                try:
                    load_ling = loading()
                    stats = migracao_geral()
                except Exception as e:
                    return render(request, 'failed.html', {'mensagem_erro': str(e)})
            else:
                load_ling = loading()
                stats = migracao_geral()
            return render(request, 'success.html', stats)
            # return HttpResponseRedirect("success.html", stats)
    else:
        form = MigracaoForm()
    return render(request, 'migracao.html', {'form':form})

# def list_provocacao(request):
#     provocacao = Provocacao.objects.all()
#     return render(request, 'provocacao.html', {'provocacao': provocacao})

# def create_provocacao(request):
#     form = ProvocacaoForm(request.POST or None)

#     if form.is_valid():
#         form.save()
#         return redirect('list_provocacao')

#     return render(request,'provocacao-form.html',{'form':form})