from django.shortcuts import render, redirect, get_object_or_404
from core.models import Contato

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
        return redirect('listar_contato')  # Redireciona após criar para a lista

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
        return redirect('listar_contato')

    return render(request, 'core/editar_contato.html', {'contato': contato})


def excluirContato(request, id):
    contato = get_object_or_404(Contato, id=id)
    contato.delete()
    return redirect('listar_contato')
