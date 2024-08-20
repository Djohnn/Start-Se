from django.shortcuts import render,redirect
from .models import Empresas, Documento, Metricas
from django.contrib import messages
from django.contrib.messages import constants
from investidores.models import PropostaInvestimento
from django.utils import timezone
from datetime import timedelta

def dashboard(request, id):
    empresa = Empresas.objects.get(id=id)
    today = timezone.now().date()

    seven_days_ago = today - timedelta(days=6)

    propostas_por_dia = {}

    for i in range(7):
        day = seven_days_ago + timedelta(days=1)

        propostas = PropostaInvestimento.objects.filter(
            empresa=empresa,
            status='PA',
            data=day
        )

        total_dia = 0
        for proposta in propostas:
            total_dia += proposta.valor

        propostas_por_dia[day.strftime('%d/%m/%Y')] = int(total_dia)

    for dia, total in propostas_por_dia.items():
        print(f'Data: {dia}, total de proposta: {total}')

    return render(request, 'dashboard.html', {'labels': list(propostas_por_dia.keys()), 'values': list(propostas_por_dia.values())})

def cadastrar_empresa(request):
    if not request.user.is_authenticated:
        return redirect('/usuarios/login')

    if request.method == "GET":
        return render(request, 'cadastrar_empresa.html', {'tempo_existencia': Empresas.tempo_existencia_choices, 'areas': Empresas.area_choices })
    elif request.method == "POST":
        nome = request.POST.get('nome')
        cnpj = request.POST.get('cnpj')
        site = request.POST.get('site')
        tempo_existencia = request.POST.get('tempo_existencia')
        descricao = request.POST.get('descricao')
        data_final = request.POST.get('data_final')
        percentual_equity = request.POST.get('percentual_equity')
        estagio = request.POST.get('estagio')
        area = request.POST.get('area')
        publico_alvo = request.POST.get('publico_alvo')
        valor = request.POST.get('valor')
        pitch = request.FILES.get('pitch')
        logo = request.FILES.get('logo')

        # TODO validaçoes do dados recebido do form
        try:
            empresa = Empresas(
                user=request.user,
                nome=nome,
                cnpj=cnpj,
                site=site,
                tempo_existencia=tempo_existencia,
                descricao=descricao,
                data_final_captacao=data_final,
                percentual_equity=percentual_equity,
                estagio=estagio,
                area=area,
                publico_alvo=publico_alvo,
                valor=valor,
                pitch=pitch,
                logo=logo
            )
            empresa.save()
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return redirect('/empresarios/cadastrar_empresa')
        
        messages.add_message(request, constants.SUCCESS, 'Empresa criada com sucesso')
        return redirect('/empresarios/cadastrar_empresa')
    
def listar_empresas(request):
    if not request.user.is_authenticated:
        return redirect('/usuarios/login')
    if request.method == "GET":
        nome_empresa = request.GET.get(empresa)
        empresas = Empresas.objects.filter(user=request.user)

        if nome_empresa:
            empresas = empresas.filter(nome__icontains=nome_empresa)

        return render(request, 'listar_empresas.html', {'empresas': empresas, 'nome_empresa': nome_empresa})
    elif request.method == "POST":
        pass

def empresa(request, id):
    empresa = Empresas.objects.get(id=id)
  
    if empresa.user != request.user:
        messages.add_message(request, constants.ERROR, "Essa empresa não e sua!")
        return redirect('/empresarios/empresas', {'documentos': documentos})
    
    if request.method == "GET":
        documentos = Documento.objects.filter(empresa=empresa)
        proposta_investimentos = PropostaInvestimento.objects.filter(empresa=empresa)

        percentual_vendido = 0
        for pi in proposta_investimentos:
            if pi.status == 'PA':
                percentual_vendido = percentual_vendido + pi.percentual

        total_captado = sum(proposta_investimentos.filter(status='PA').values_list('valor', flat=True))
        valuation_atual = (100 * float(total_captado)) / float(percentual_vendido) if percentual_vendido != 0 else 0
        proposta_investimentos_enviada = proposta_investimentos.filter(status='PE')

        context = {'empresa': empresa,
                   'documentos': documentos,
                   'proposta_investimentos_enviada': proposta_investimentos_enviada,
                   'percentual_vendido': int(percentual_vendido),
                   'total_captado': total_captado,
                   'valuation_atual': valuation_atual}
        
        return render(request, 'empresa.html', context) 

def gerenciar_proposta(request, id):
    acao = request.GET.get('acao')
    pi = PropostaInvestimento.objects.get(id=id)

    if acao == 'aceitar':
        messages.add_message(request, constants.SUCCESS, 'Proposta aceita')
        pi.status = 'PA'
    elif acao == 'recusar':
        messages.add_message(request, constants.SUCCESS, 'Proposta recusada')
        pi.status = 'PR'


    pi.save()
    return redirect(f'/empresarios/empresa/{pi.empresa.id}')

def add_doc(request, id):
    empresa = Empresas.objects.get(id=id)
    titulo = request.POST.get('titulo')
    arquivo = request.FILES.get('arquivo')
    extensao = arquivo.name.split('.')

    if empresa.user != request.user:
        messages.add_message(request, constants.ERROR, "Essa empresa não e sua!")
        return redirect('/empresarios/empresas')

    if extensao[1] != 'pdf':
        messages.add_message(request, constants.ERROR, "Envie apenas PDF's")
        return redirect(f'/empresarios/empresa/{empresa.id}')
    
    if not arquivo:
        messages.add_message(request, constants.ERROR, "Envie um arquivo")
        return redirect(f'/empresarios/empresa/{empresa.id}')
        
    documento = Documento(
        empresa=empresa,
        titulo=titulo,
        arquivo=arquivo
    )
    documento.save()
    messages.add_message(request, constants.SUCCESS, "Arquivo cadastrado com sucesso")
    return redirect(f'/empresarios/empresa/{empresa.id}')

def excluir_doc(request, id):
    documento = Documento.objects.get(id=id)

    if documento.empresa.user != request.user:
        messages.add_message(request, constants.ERROR, "Esse documento não e seu")
        return redirect(f'/empresarios/empresas/{empresa.id}')
    
    documento.delete()
    messages.add_message(request, constants.SUCCESS, "Arquivo excluido com sucesso")
    return redirect(f'/empresarios/empresa/{documento.empresa.id}')

def add_metricas(request, id):
    empresa = Empresas.objects.get(id=id)
    titulo = request.POST.get('titulo')
    valor = request.POST.get('valor')

    metrica = Metricas(
        empresa=empresa,
        titulo=titulo,
        valor=valor
        )
    metrica.save()
    messages.add_message(request, constants.SUCCESS, "Metrica cadastrada com sucesso")
    return redirect(f'/empresarios/empresa/{empresa.id}')