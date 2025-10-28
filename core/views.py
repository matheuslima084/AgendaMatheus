from django.shortcuts import render, redirect, get_object_or_404
from core.models import Contato
from django.db.models.functions import Concat
from django.db.models import Q, Value
from django.core.paginator import Paginator
from django.contrib import messages

def add_contato(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        descricao = request.POST.get('descricao')
        telefone = request.POST.get('telefone')
        imagem = request.FILES.get('imagem')

        if not nome or not sobrenome:
            # Poderia passar uma mensagem de erro aqui, se quiser
            return render(request, 'core/add_contato.html')

        Contato.objects.create(
            nome=nome,
            sobrenome=sobrenome,
            descricao=descricao,
            telefone=telefone,
            imagem=imagem
        )
        # ✅ usa namespace 'core:'
        return redirect('core:listar_contato')

    return render(request, 'core/add_contato.html')


def listar_contato(request):
    contatos = Contato.objects.all()
    return render(request, 'core/listar_contato.html', {'contato': contatos})


def editarContato(request, id):
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
        # ✅ usa namespace 'core:'
        return redirect('core:listar_contato')

    return render(request, 'core/editar_contato.html', {'contato': contato})


def excluirContato(request, id):
    contato = get_object_or_404(Contato, id=id)
    contato.delete()
    # ✅ usa namespace 'core:'
    return redirect('core:listar_contato')

def buscarContato(request):
    termo = request.GET.get('termo')

    if not termo:
        messages.error(request, 'Campo não pode ser vazio!')
        # ✅ Corrigido: adiciona o namespace 'core:'
        return redirect('core:listar_contato')

    campos = Concat('nome', Value(' '), 'sobrenome')

    contatos = (
        Contato.objects
        .annotate(nome_contato=campos)
        .filter(Q(nome_contato__icontains=termo))
    )

    paginator = Paginator(contatos, 6)
    page = request.GET.get('p')
    contatos = paginator.get_page(page)

    if not contatos:
        messages.warning(request, 'Nenhum resultado encontrado.')

    context = {
        'contatos': contatos,
        'termo': termo,
    }

    return render(request, 'core/buscarContato.html', context)