from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Produto, Venda

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'login.html')

def registro_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Este nome de usuário já existe.')
        elif username and password:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('home')
    return render(request, 'registro.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        categoria = request.POST.get('categoria')
        quantidade = request.POST.get('quantidade')
        preco = request.POST.get('preco')
        if nome and categoria and quantidade and preco:
            Produto.objects.create(
                nome=nome,
                categoria=categoria,
                quantidade=int(quantidade),
                preco=float(preco.replace(',', '.'))
            )
        return redirect('home')

    busca = request.GET.get('busca', '')
    if busca:
        produtos = Produto.objects.filter(nome__icontains=busca).order_by('-id')
    else:
        produtos = Produto.objects.all().order_by('-id')

    vendas = Venda.objects.all().order_by('-id')[:5]
    total_itens = sum(p.quantidade for p in produtos)
    faturamento = sum(v.valor_total for v in Venda.objects.all())

    return render(request, 'index.html', {
        'produtos': produtos,
        'vendas': vendas,
        'total_produtos': produtos.count(),
        'total_itens': total_itens,
        'faturamento': faturamento,
        'busca': busca
    })

@login_required(login_url='login')
def vender_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    if produto.quantidade > 0:
        produto.quantidade -= 1
        produto.save()
        Venda.objects.create(produto=produto, quantidade=1, valor_total=produto.preco)
    return redirect('home')

@login_required(login_url='login')
def repor_estoque(request, id):
    produto = get_object_or_404(Produto, id=id)
    produto.quantidade += 1
    produto.save()
    return redirect('home')

@login_required(login_url='login')
def deletar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    produto.delete()
    return redirect('home')