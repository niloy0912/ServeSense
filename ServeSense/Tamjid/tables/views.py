from django.shortcuts import render, redirect, get_object_or_404
from .models import Table
from .forms import TableForm

def table_list(request):
    tables = Table.objects.all()

    # Handle add form submission
    if request.method == 'POST':
        form = TableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('table_list')
    else:
        form = TableForm()

    return render(request, 'tables/table_list.html', {'tables': tables, 'form': form})

def table_edit(request, pk):
    table = get_object_or_404(Table, pk=pk)
    if request.method == 'POST':
        form = TableForm(request.POST, instance=table)
        if form.is_valid():
            form.save()
            return redirect('table_list')
    else:
        form = TableForm(instance=table)
    return render(request, 'tables/table_edit.html', {'form': form})

def table_delete(request, pk):
    table = get_object_or_404(Table, pk=pk)
    table.delete()
    return redirect('table_list')
