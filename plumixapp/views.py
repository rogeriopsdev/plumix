from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib import messages

from .models import (
    Granja, Galpao, Lote, Ambiente, Racao, Agua,
    Mortalidade, Pesagem, Tratamento, Vacinacao, Evento, Alerta
)
from .forms import (
    GranjaForm, GalpaoForm, LoteForm, AmbienteForm, RacaoForm, AguaForm,
    MortalidadeForm, PesagemForm, TratamentoForm, VacinacaoForm, EventoForm, AlertaForm
)


# ---------------------------
# Página inicial
# ---------------------------
from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum, Avg, Count
from django.shortcuts import render
from django.urls import reverse

from .models import (
    Granja, Galpao, Lote, Ambiente, Racao, Agua,
    Mortalidade, Pesagem, Tratamento, Vacinacao, Evento, Alerta
)

from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404

from .models import Lote, Racao, Agua, Mortalidade, Pesagem

from datetime import timedelta, datetime
from django.utils import timezone
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404

from .models import Granja, Galpao, Lote, Racao, Agua, Mortalidade, Pesagem


from django.contrib import messages  # opcional, caso queira avisos

def _get_or_session(request, key, default=None):
    """Se houver GET, usa; senão, cai no session; senão, default."""
    val = request.GET.get(key)
    if val is None:
        val = request.session.get(f"dash_{key}", default)
    return val
def _safe_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except Exception:
        return None

def index(request):
    # -------- Filtros: período (dias) OU intervalo custom (start/end) --------
    allowed_periods = [7, 14, 30, 60, 90]
    # lê de GET ou session
    dias_str = _get_or_session(request, "dias", "30")
    start_str = _get_or_session(request, "start", "")
    end_str = _get_or_session(request, "end", "")
    granja_str = _get_or_session(request, "granja", "")
    galpao_str = _get_or_session(request, "galpao", "")
    lote_str = _get_or_session(request, "lote", "")

    # normaliza período
    try:
        periodo_dias = int(dias_str)
    except (TypeError, ValueError):
        periodo_dias = 30
    if periodo_dias not in allowed_periods:
        periodo_dias = 30

    start_dt = _safe_date(start_str) if start_str else None
    end_dt = _safe_date(end_str) if end_str else None
    use_custom_range = bool(start_dt and end_dt and start_dt <= end_dt)

    # selecionados (se existirem)
    granja_selected = get_object_or_404(Granja, pk=int(granja_str)) if granja_str else None
    galpao_selected = get_object_or_404(Galpao, pk=int(galpao_str)) if galpao_str else None
    lote_selected = get_object_or_404(Lote, pk=int(lote_str)) if lote_str else None
    try:
        periodo_dias = int(request.GET.get('dias', 30))
    except (TypeError, ValueError):
        periodo_dias = 30
    if periodo_dias not in allowed_periods:
        periodo_dias = 30

    start_str = request.GET.get('start')
    end_str   = request.GET.get('end')
    start_dt  = _safe_date(start_str) if start_str else None
    end_dt    = _safe_date(end_str) if end_str else None
    use_custom_range = bool(start_dt and end_dt and start_dt <= end_dt)

    # -------- Filtros: granja / galpão / lote --------
    granja_param = request.GET.get('granja')
    galpao_param = request.GET.get('galpao')
    lote_param   = request.GET.get('lote')

    granja_selected = get_object_or_404(Granja, pk=int(granja_param)) if granja_param else None
    galpao_selected = get_object_or_404(Galpao, pk=int(galpao_param)) if galpao_param else None
    lote_selected   = get_object_or_404(Lote,   pk=int(lote_param))   if lote_param   else None

    # -------- Datas base --------
    today = timezone.now().date()
    if use_custom_range:
        date_from = start_dt
        date_to   = end_dt
        # Ajuste para queries que usam __gte apenas: manter today p/ idade
    else:
        date_to   = today
        date_from = today - timedelta(days=periodo_dias)

    # Período anterior (p/ tendências)
    prev_to   = date_from - timedelta(days=1)
    prev_from = prev_to - (date_to - date_from)

    # -------- Base de filtros por relacionamento --------
    # Restringe lotes por granja/galpão se informados
    lotes_base = Lote.objects.all()
    if granja_selected:
        galpoes_ids = Galpao.objects.filter(id_granja=granja_selected).values_list('pk', flat=True)
        lotes_base = lotes_base.filter(id_galpao__in=galpoes_ids)
    if galpao_selected:
        lotes_base = lotes_base.filter(id_galpao=galpao_selected)
    if lote_selected:
        lotes_base = lotes_base.filter(pk=lote_selected.pk)

    # -------- KPIs --------
    total_lotes = lotes_base.count()
    lotes_ativos = lotes_base.filter(d_entrada_lote__lte=today, d_saida_lote__gte=today).count()

    racao_qs = Racao.objects.filter(data_racao__gte=date_from, data_racao__lte=date_to)
    agua_qs  = Agua .objects.filter(data_agua__gte=date_from,  data_agua__lte=date_to)
    mortal_qs= Mortalidade.objects.filter(data_mortalidade__gte=date_from, data_mortalidade__lte=date_to)

    if granja_selected:
        racao_qs  = racao_qs .filter(id_lote__id_galpao__id_granja=granja_selected)
        agua_qs   = agua_qs  .filter(id_lote__id_galpao__id_granja=granja_selected)
        mortal_qs = mortal_qs.filter(id_lote__id_galpao__id_granja=granja_selected)
    if galpao_selected:
        racao_qs  = racao_qs .filter(id_lote__id_galpao=galpao_selected)
        agua_qs   = agua_qs  .filter(id_lote__id_galpao=galpao_selected)
        mortal_qs = mortal_qs.filter(id_lote__id_galpao=galpao_selected)
    if lote_selected:
        racao_qs  = racao_qs .filter(id_lote=lote_selected)
        agua_qs   = agua_qs  .filter(id_lote=lote_selected)
        mortal_qs = mortal_qs.filter(id_lote=lote_selected)

    racao_total  = racao_qs .aggregate(total=Sum('kg_racao'))['total'] or 0
    agua_total   = agua_qs  .aggregate(total=Sum('litro_agua'))['total'] or 0
    mortal_total = mortal_qs.aggregate(total=Sum('qtd_mortalidade'))['total'] or 0

    # Tendência vs período anterior (apenas Mortalidade, pra sinalizar cartão)
    racao_prev = Racao.objects.filter(data_racao__gte=prev_from, data_racao__lte=prev_to)
    agua_prev  = Agua .objects.filter(data_agua__gte=prev_from,  data_agua__lte=prev_to)
    mort_prev  = Mortalidade.objects.filter(data_mortalidade__gte=prev_from, data_mortalidade__lte=prev_to)

    if granja_selected:
        racao_prev = racao_prev.filter(id_lote__id_galpao__id_granja=granja_selected)
        agua_prev  = agua_prev .filter(id_lote__id_galpao__id_granja=granja_selected)
        mort_prev  = mort_prev .filter(id_lote__id_galpao__id_granja=granja_selected)
    if galpao_selected:
        racao_prev = racao_prev.filter(id_lote__id_galpao=galpao_selected)
        agua_prev  = agua_prev .filter(id_lote__id_galpao=galpao_selected)
        mort_prev  = mort_prev .filter(id_lote__id_galpao=galpao_selected)
    if lote_selected:
        racao_prev = racao_prev.filter(id_lote=lote_selected)
        agua_prev  = agua_prev .filter(id_lote=lote_selected)
        mort_prev  = mort_prev .filter(id_lote=lote_selected)

    racao_prev_total  = racao_prev.aggregate(total=Sum('kg_racao'))['total'] or 0
    agua_prev_total   = agua_prev .aggregate(total=Sum('litro_agua'))['total'] or 0
    mortal_prev_total = mort_prev.aggregate(total=Sum('qtd_mortalidade'))['total'] or 0

    def _delta(curr, prev):
        diff = curr - prev
        pct  = (diff / prev * 100) if prev else (100.0 if curr else 0.0)
        return diff, pct

    mortal_diff, mortal_pct = _delta(mortal_total, mortal_prev_total)
    mortal_card_class = 'border-left-danger' if mortal_diff > 0 else 'border-left-success'

    # -------- Série: Peso Médio x Idade --------
    if lote_selected:
        lote_ref = lote_selected
    else:
        lote_ref = (lotes_base.filter(d_entrada_lote__lte=today, d_saida_lote__gte=today)
                    .order_by('-d_entrada_lote').first()
                    or lotes_base.order_by('-d_entrada_lote').first())

    peso_idade_labels, peso_idade_values = [], []
    if lote_ref:
        pesagens = Pesagem.objects.filter(id_lote=lote_ref).order_by('data_pesagem')
        for p in pesagens:
            idade_dias = (p.data_pesagem - lote_ref.d_entrada_lote).days
            if idade_dias >= 0:
                peso_idade_labels.append(idade_dias)
                peso_idade_values.append(float(p.pmedio_pesagem))

    # -------- Pizza: Mortalidade por causa --------
    mort_por_causa_qs = (mortal_qs.values('causa_mortalidade')
                         .annotate(total=Sum('qtd_mortalidade'))
                         .order_by('-total'))
    mort_labels = [m['causa_mortalidade'] or 'N/D' for m in mort_por_causa_qs]
    mort_values = [m['total'] for m in mort_por_causa_qs]

    # -------- Séries diárias (Ração/Água) --------
    # Gera eixo de datas do intervalo selecionado
    num_days = (date_to - date_from).days
    date_list = [date_from + timedelta(days=i) for i in range(num_days + 1)]

    racao_by_date = {row['data_racao']: float(row['total'])
                     for row in racao_qs.values('data_racao').annotate(total=Sum('kg_racao'))}
    agua_by_date  = {row['data_agua']:  float(row['total'])
                     for row in agua_qs.values('data_agua').annotate(total=Sum('litro_agua'))}

    daily_labels       = [d.strftime('%d/%m') for d in date_list]
    racao_daily_values = [racao_by_date.get(d, 0.0) for d in date_list]
    agua_daily_values  = [agua_by_date.get(d, 0.0)  for d in date_list]

    # -------- Opções dos selects --------
    granjas  = Granja.objects.order_by('nome_granja').values('pk', 'nome_granja')
    galpoes  = Galpao.objects.order_by('nome_galpao')
    if granja_selected:
        galpoes = galpoes.filter(id_granja=granja_selected)
    galpoes = galpoes.values('pk', 'nome_galpao')

    lotes = lotes_base.order_by('-d_entrada_lote').values('pk', 'nome_lote')

    context = {
        'title': 'Dashboard',
        # filtros
        'periodos': allowed_periods,
        'periodo_dias': periodo_dias,
        'use_custom_range': use_custom_range,
        'start': start_dt.strftime("%Y-%m-%d") if start_dt else '',
        'end':   end_dt.strftime("%Y-%m-%d")   if end_dt   else '',
        'granjas': list(granjas),
        'galpoes': list(galpoes),
        'lotes':   list(lotes),
        'granja_selected': granja_selected,
        'galpao_selected': galpao_selected,
        'lote_selected':   lote_selected,

        # KPIs
        'total_lotes': total_lotes,
        'lotes_ativos': lotes_ativos,
        'mortal_30d': mortal_total,
        'racao_30d': float(racao_total),
        'agua_30d':  float(agua_total),
        'mortal_card_class': mortal_card_class,
        'mortal_diff': int(mortal_diff),
        'mortal_pct':  round(mortal_pct, 1),

        # referência do gráfico
        'lote_ref': lote_ref,

        # séries
        'peso_idade_labels': peso_idade_labels,
        'peso_idade_values': peso_idade_values,
        'mort_labels': mort_labels,
        'mort_values': mort_values,

        # séries diárias
        'daily_labels': daily_labels,
        'racao_daily_values': racao_daily_values,
        'agua_daily_values':  agua_daily_values,
    }
    request.session["dash_dias"] = str(periodo_dias)
    request.session["dash_start"] = context['start']
    request.session["dash_end"] = context['end']
    request.session["dash_granja"] = str(granja_selected.pk) if granja_selected else ""
    request.session["dash_galpao"] = str(galpao_selected.pk) if galpao_selected else ""
    request.session["dash_lote"] = str(lote_selected.pk) if lote_selected else ""
    return render(request, 'plumix/index.html', context)

from django.http import HttpResponse
import csv

def _safe_date(s):
    try:
        from datetime import datetime
        return datetime.strptime(s, "%Y-%m-%d").date()
    except Exception:
        return None

def dashboard_export_csv(request):
    """Exporta CSV do consumo diário (Ração/Água) respeitando os mesmos filtros do dashboard."""
    from django.utils import timezone
    from datetime import timedelta
    from django.db.models import Sum
    from django.shortcuts import get_object_or_404
    from .models import Granja, Galpao, Lote, Racao, Agua

    # -------- Período: rápido (dias) OU custom (start/end)
    allowed_periods = [7, 14, 30, 60, 90]
    try:
        periodo_dias = int(request.GET.get('dias', 30))
    except (TypeError, ValueError):
        periodo_dias = 30
    if periodo_dias not in allowed_periods:
        periodo_dias = 30

    start_dt = _safe_date(request.GET.get('start')) if request.GET.get('start') else None
    end_dt   = _safe_date(request.GET.get('end'))   if request.GET.get('end')   else None
    use_custom_range = bool(start_dt and end_dt and start_dt <= end_dt)

    # -------- Filtros: granja/galpão/lote
    granja_selected = None
    galpao_selected = None
    lote_selected   = None
    if request.GET.get('granja'):
        try: granja_selected = get_object_or_404(Granja, pk=int(request.GET['granja']))
        except Exception: pass
    if request.GET.get('galpao'):
        try: galpao_selected = get_object_or_404(Galpao, pk=int(request.GET['galpao']))
        except Exception: pass
    if request.GET.get('lote'):
        try: lote_selected   = get_object_or_404(Lote,   pk=int(request.GET['lote']))
        except Exception: pass

    # -------- Datas base
    today = timezone.now().date()
    if use_custom_range:
        date_from, date_to = start_dt, end_dt
    else:
        date_to = today
        date_from = today - timedelta(days=periodo_dias)

    # -------- Querysets
    racao_qs = Racao.objects.filter(data_racao__gte=date_from, data_racao__lte=date_to)
    agua_qs  = Agua .objects.filter(data_agua__gte=date_from,  data_agua__lte=date_to)

    if granja_selected:
        racao_qs = racao_qs.filter(id_lote__id_galpao__id_granja=granja_selected)
        agua_qs  = agua_qs .filter(id_lote__id_galpao__id_granja=granja_selected)
    if galpao_selected:
        racao_qs = racao_qs.filter(id_lote__id_galpao=galpao_selected)
        agua_qs  = agua_qs .filter(id_lote__id_galpao=galpao_selected)
    if lote_selected:
        racao_qs = racao_qs.filter(id_lote=lote_selected)
        agua_qs  = agua_qs .filter(id_lote=lote_selected)

    # ------- Séries diárias
    num_days = (date_to - date_from).days
    date_list = [date_from + timedelta(days=i) for i in range(num_days + 1)]

    racao_by_date = {row['data_racao']: float(row['total'])
                     for row in racao_qs.values('data_racao').annotate(total=Sum('kg_racao'))}
    agua_by_date  = {row['data_agua']:  float(row['total'])
                     for row in agua_qs.values('data_agua').annotate(total=Sum('litro_agua'))}

    # -------- Resposta CSV
    filename = "consumo"
    if use_custom_range:
        filename += f"_{date_from:%Y%m%d}-{date_to:%Y%m%d}"
    else:
        filename += f"_{periodo_dias}d"
    if lote_selected:   filename += f"_lote-{lote_selected.pk}"
    elif galpao_selected: filename += f"_galpao-{galpao_selected.pk}"
    elif granja_selected: filename += f"_granja-{granja_selected.pk}"

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'

    writer = csv.writer(response, delimiter=';')
    writer.writerow(['data', 'racao_kg', 'agua_litros'])
    for d in date_list:
        writer.writerow([d.strftime('%Y-%m-%d'),
                         racao_by_date.get(d, 0.0),
                         agua_by_date.get(d, 0.0)])
    return response



# ---------------------------
# Helpers genéricos FBV
# ---------------------------
def _list_view(request, *, model, title, create_url_name=None, update_url_name=None,
               delete_url_name=None, list_url_name=None, template='plumix/generic_list.html',
               order_by='-pk', per_page=20):
    qs = model.objects.all().order_by(order_by)

    # filtro simples opcional
    q = request.GET.get('q')
    if q:
        qs = qs.filter(pk__icontains=q)  # troque por filtro real se quiser

    from django.core.paginator import Paginator
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(request.GET.get('page'))

    # >>> CRIA A LISTA DE COLUNAS AQUI (sem usar no template nada com "_")
    columns = [f.name for f in model._meta.fields]

    context = {
        'title': title,
        'objects': page_obj.object_list,
        'columns': columns,                # <<< manda pro template
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'create_name': create_url_name,
        'update_name': update_url_name,
        'delete_name': delete_url_name,
        'list_name': list_url_name,
        'model': model,
        'query': q or '',
    }
    return render(request, template, context)



def _create_view(request, *, form_class, success_url_name, title, template='plumix/generic_form.html',
                 success_message='Registro criado com sucesso!'):
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            obj = form.save()
            messages.success(request, success_message)
            return redirect(reverse(success_url_name))
    else:
        form = form_class()

    context = {
        'title': title,
        'form': form,
        'action': 'create',
    }
    return render(request, template, context)


def _update_view(request, pk, *, model, form_class, success_url_name, title,
                 template='plumix/generic_form.html',
                 success_message='Registro atualizado com sucesso!'):
    obj = get_object_or_404(model, pk=pk)

    if request.method == 'POST':
        form = form_class(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, success_message)
            return redirect(reverse(success_url_name))
    else:
        form = form_class(instance=obj)

    context = {
        'title': title,
        'form': form,
        'object': obj,
        'action': 'update',
    }
    return render(request, template, context)


def _delete_view(request, pk, *, model, success_url_name, title,
                 template='plumix/generic_confirm_delete.html',
                 success_message='Registro excluído com sucesso!'):
    obj = get_object_or_404(model, pk=pk)

    if request.method == 'POST':
        obj.delete()
        messages.success(request, success_message)
        return redirect(reverse(success_url_name))

    context = {
        'title': title,
        'object': obj,
    }
    return render(request, template, context)


# ---------------------------
# GRANJA
# ---------------------------
def granja_list(request):
    return _list_view(request, model=Granja, title='Granjas', create_url_name='granja_create')

def granja_create(request):
    return _create_view(request, form_class=GranjaForm, success_url_name='granja_list', title='Nova Granja')

def granja_update(request, pk):
    return _update_view(request, pk, model=Granja, form_class=GranjaForm,
                        success_url_name='granja_list', title='Editar Granja')

def granja_delete(request, pk):
    return _delete_view(request, pk, model=Granja, success_url_name='granja_list', title='Excluir Granja')


# ---------------------------
# GALPÃO
# ---------------------------
def galpao_list(request):
    return _list_view(request, model=Galpao, title='Galpões', create_url_name='galpao_create')

def galpao_create(request):
    return _create_view(request, form_class=GalpaoForm, success_url_name='galpao_list', title='Novo Galpão')

def galpao_update(request, pk):
    return _update_view(request, pk, model=Galpao, form_class=GalpaoForm,
                        success_url_name='galpao_list', title='Editar Galpão')

def galpao_delete(request, pk):
    return _delete_view(request, pk, model=Galpao, success_url_name='galpao_list', title='Excluir Galpão')


# ---------------------------
# LOTE
# ---------------------------
def lote_list(request):
    return _list_view(request, model=Lote, title='Lotes', create_url_name='lote_create')

def lote_create(request):
    return _create_view(request, form_class=LoteForm, success_url_name='lote_list', title='Novo Lote')

def lote_update(request, pk):
    return _update_view(request, pk, model=Lote, form_class=LoteForm,
                        success_url_name='lote_list', title='Editar Lote')

def lote_delete(request, pk):
    return _delete_view(request, pk, model=Lote, success_url_name='lote_list', title='Excluir Lote')


# ---------------------------
# AMBIENTE
# ---------------------------
def ambiente_list(request):
    return _list_view(request, model=Ambiente, title='Leituras de Ambiente', create_url_name='ambiente_create')

def ambiente_create(request):
    return _create_view(request, form_class=AmbienteForm, success_url_name='ambiente_list', title='Nova Leitura de Ambiente')

def ambiente_update(request, pk):
    return _update_view(request, pk, model=Ambiente, form_class=AmbienteForm,
                        success_url_name='ambiente_list', title='Editar Leitura de Ambiente')

def ambiente_delete(request, pk):
    return _delete_view(request, pk, model=Ambiente, success_url_name='ambiente_list', title='Excluir Leitura de Ambiente')


# ---------------------------
# RAÇÃO
# ---------------------------
def racao_list(request):
    return _list_view(request, model=Racao, title='Ração', create_url_name='racao_create')

def racao_create(request):
    return _create_view(request, form_class=RacaoForm, success_url_name='racao_list', title='Novo Registro de Ração')

def racao_update(request, pk):
    return _update_view(request, pk, model=Racao, form_class=RacaoForm,
                        success_url_name='racao_list', title='Editar Registro de Ração')

def racao_delete(request, pk):
    return _delete_view(request, pk, model=Racao, success_url_name='racao_list', title='Excluir Registro de Ração')


# ---------------------------
# ÁGUA
# ---------------------------
def agua_list(request):
    return _list_view(request, model=Agua, title='Água', create_url_name='agua_create')

def agua_create(request):
    return _create_view(request, form_class=AguaForm, success_url_name='agua_list', title='Novo Registro de Água')

def agua_update(request, pk):
    return _update_view(request, pk, model=Agua, form_class=AguaForm,
                        success_url_name='agua_list', title='Editar Registro de Água')

def agua_delete(request, pk):
    return _delete_view(request, pk, model=Agua, success_url_name='agua_list', title='Excluir Registro de Água')


# ---------------------------
# MORTALIDADE
# ---------------------------
def mortalidade_list(request):
    return _list_view(request, model=Mortalidade, title='Mortalidade', create_url_name='mortalidade_create')

def mortalidade_create(request):
    return _create_view(request, form_class=MortalidadeForm, success_url_name='mortalidade_list', title='Nova Mortalidade')

def mortalidade_update(request, pk):
    return _update_view(request, pk, model=Mortalidade, form_class=MortalidadeForm,
                        success_url_name='mortalidade_list', title='Editar Mortalidade')

def mortalidade_delete(request, pk):
    return _delete_view(request, pk, model=Mortalidade, success_url_name='mortalidade_list', title='Excluir Mortalidade')


# ---------------------------
# PESAGEM
# ---------------------------
def pesagem_list(request):
    return _list_view(request, model=Pesagem, title='Pesagens', create_url_name='pesagem_create')

def pesagem_create(request):
    return _create_view(request, form_class=PesagemForm, success_url_name='pesagem_list', title='Nova Pesagem')

def pesagem_update(request, pk):
    return _update_view(request, pk, model=Pesagem, form_class=PesagemForm,
                        success_url_name='pesagem_list', title='Editar Pesagem')

def pesagem_delete(request, pk):
    return _delete_view(request, pk, model=Pesagem, success_url_name='pesagem_list', title='Excluir Pesagem')


# ---------------------------
# TRATAMENTO
# ---------------------------
def tratamento_list(request):
    return _list_view(request, model=Tratamento, title='Tratamentos', create_url_name='tratamento_create')

def tratamento_create(request):
    return _create_view(request, form_class=TratamentoForm, success_url_name='tratamento_list', title='Novo Tratamento')

def tratamento_update(request, pk):
    return _update_view(request, pk, model=Tratamento, form_class=TratamentoForm,
                        success_url_name='tratamento_list', title='Editar Tratamento')

def tratamento_delete(request, pk):
    return _delete_view(request, pk, model=Tratamento, success_url_name='tratamento_list', title='Excluir Tratamento')


# ---------------------------
# VACINAÇÃO
# ---------------------------
def vacinacao_list(request):
    return _list_view(request, model=Vacinacao, title='Vacinações', create_url_name='vacinacao_create')

def vacinacao_create(request):
    return _create_view(request, form_class=VacinacaoForm, success_url_name='vacinacao_list', title='Nova Vacinação')

def vacinacao_update(request, pk):
    return _update_view(request, pk, model=Vacinacao, form_class=VacinacaoForm,
                        success_url_name='vacinacao_list', title='Editar Vacinação')

def vacinacao_delete(request, pk):
    return _delete_view(request, pk, model=Vacinacao, success_url_name='vacinacao_list', title='Excluir Vacinação')


# ---------------------------
# EVENTO
# ---------------------------
def evento_list(request):
    return _list_view(request, model=Evento, title='Eventos', create_url_name='evento_create')

def evento_create(request):
    return _create_view(request, form_class=EventoForm, success_url_name='evento_list', title='Novo Evento')

def evento_update(request, pk):
    return _update_view(request, pk, model=Evento, form_class=EventoForm,
                        success_url_name='evento_list', title='Editar Evento')

def evento_delete(request, pk):
    return _delete_view(request, pk, model=Evento, success_url_name='evento_list', title='Excluir Evento')


# ---------------------------
# ALERTA
# ---------------------------
def alerta_list(request):
    return _list_view(request, model=Alerta, title='Alertas', create_url_name='alerta_create')

def alerta_create(request):
    return _create_view(request, form_class=AlertaForm, success_url_name='alerta_list', title='Novo Alerta')

def alerta_update(request, pk):
    return _update_view(request, pk, model=Alerta, form_class=AlertaForm,
                        success_url_name='alerta_list', title='Editar Alerta')

def alerta_delete(request, pk):
    return _delete_view(request, pk, model=Alerta, success_url_name='alerta_list', title='Excluir Alerta')
