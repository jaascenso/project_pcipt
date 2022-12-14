from django.http import HttpResponseRedirect
from django.db import models
from django.shortcuts import render, redirect
from historia.forms import *
from historia.models import *
from historia.processo_migracao import *
from django.conf import settings

def home(request):
    return render(request, 'home.html')

def loading(request):
    return render(request, 'loading.html')

def migracao(request):
    if request.method == 'POST':
        form = MigracaoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            if form['apagar_dados'].value():
                apagar_geral()
            if not settings.DEBUG:
                try:
                    stats = migracao_geral()
                except Exception as e:
                    return render(request, 'failed.html', {'mensagem_erro': str(e)})
            else:
                stats = migracao_geral()
            return render(request, 'success.html', stats)
            # return HttpResponseRedirect("success.html", stats)
    else:
        form = MigracaoForm()
    return render(request, 'migracao.html', {'form':form})