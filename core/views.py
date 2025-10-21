from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.translation.template import context_re
from core.models import Contato

def add_contato(request):
    if request.method != 'POST':
        return render(request, 'core/add_contato.html')
    nome = request.POST['nome']
    sobrenome = request.POST['sobrenome']
    descricao = request.POST['descricao']
    telefone = request.POST['telefone']
    imagem = request.FILES['imagem']

    if not nome or not sobrenome:
        return render(request, 'core/add_contato.html')
    salvarContato = Contato.objects.create(nome=nome, sobrenome=sobrenome, descricao=descricao, telefone=telefone, imagem=imagem)

    salvarContato.save()
    return render(request, 'core/add_contato.html')


def listar_contato(request):
    contato = Contato.objects.all()
    return render(request, 'core/listar_contato.html',
                  {'contato': contato})

def editarContato(request,id):
    contato = get_object_or_404(Contato, id=id)
    if request.method == 'POST':
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        descricao = request.POST.get('descricao')
        telefone = request.POST.get('telefone')
        imagem = request.FILES('imagem')

        contato.nome = nome
        contato.sobrenome = sobrenome
        contato.descricao = descricao
        contato.telefone = telefone
        contato.imagem = imagem
        contato.save()
        return redirect('listar_contato')

    context = {
        'contato': contato
    }
    return render(request, 'core/editar_Contato.html', context)