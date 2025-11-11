from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Contato
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.core.paginator import Paginator

def add_contato(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        descricao = request.POST.get('descricao')
        telefone = request.POST.get('telefone')
        imagem = request.FILES.get('imagem')

        contato = Contato(
            nome=nome,
            sobrenome=sobrenome,
            descricao=descricao,
            telefone=telefone,
            imagem=imagem
        )
        contato.save()
        messages.success(request, "Contato adicionado com sucesso!")
        return redirect('listar_contato')  # sem namespace

    return render(request, 'core/add_contato.html')


def listar_contato(request):
    contatos = Contato.objects.all()
    paginator = Paginator(contatos, 6)
    page = request.GET.get('p')
    contatos = paginator.get_page(page)
    return render(request, 'core/listar_contato.html', {'contatos': contatos})


def editarContato(request):
    id = request.GET.get('id')
    if not id:
        messages.error(request, "Contato não especificado!")
        return redirect('listar_contato')  # sem namespace

    contato = get_object_or_404(Contato, id=id)

    if request.method == 'POST':
        contato.nome = request.POST.get('nome')
        contato.sobrenome = request.POST.get('sobrenome')
        contato.descricao = request.POST.get('descricao')
        contato.telefone = request.POST.get('telefone')

        imagem = request.FILES.get('imagem')
        if imagem:
            contato.imagem = imagem

        contato.save()
        messages.success(request, "Contato atualizado com sucesso!")
        return redirect('listar_contato')  # sem namespace

    return render(request, 'core/editar_contato.html', {'contato': contato})


def excluirContato(request):
    id = request.GET.get('id')
    if not id:
        messages.error(request, "Contato não especificado!")
        return redirect('listar_contato')  # sem namespace

    contato = get_object_or_404(Contato, id=id)
    contato.delete()
    messages.success(request, "Contato excluído com sucesso!")
    return redirect('listar_contato')  # sem namespace


def buscarContato(request):
    termo = request.GET.get('termo')

    if not termo:
        messages.error(request, 'Campo não pode ser vazio!')
        return redirect('listar_contato')  # sem namespace

    campos = Concat('nome', Value(' '), 'sobrenome')
    contatos_query = Contato.objects.annotate(nome_contato=campos).filter(Q(nome_contato__icontains=termo))

    paginator = Paginator(contatos_query, 6)
    page = request.GET.get('p')
    contatos = paginator.get_page(page)

    if contatos.paginator.count == 0:
        messages.warning(request, 'Nenhum resultado encontrado.')

    context = {
        'contatos': contatos,
        'termo': termo,
    }

    return render(request, 'core/buscarContato.html', context)
