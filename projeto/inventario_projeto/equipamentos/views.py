from django.shortcuts import render, redirect
from .models import Equipamento
from .forms import EquipamentoForm

def lista_equipamentos(request):
    equipamentos = Equipamento.objects.all()
    query = request.GET.get('q')
    if query:
        equipamentos = equipamentos.filter(equipamento__icontains=query)
    return render(request, 'equipamentos/lista_equipamentos.html', {'equipamentos': equipamentos})

def adicionar_equipamento(request):
    if request.method == 'POST':
        form = EquipamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_equipamentos')
    else:
        form = EquipamentoForm()
    return render(request, 'equipamentos/adicionar_equipamento.html', {'form': form})

