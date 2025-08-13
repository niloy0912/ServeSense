from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuItem
from .forms import MenuItemForm

def menu_list(request):
    menu_items = MenuItem.objects.all()

    # Handle add form submission
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu_list')
    else:
        form = MenuItemForm()

    return render(request, 'menu/menu_list.html', {'menu_items': menu_items, 'form': form})

def menu_edit(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('menu_list')
    else:
        form = MenuItemForm(instance=item)
    return render(request, 'menu/menu_edit.html', {'form': form})

def menu_delete(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    item.delete()
    return redirect('menu_list')
