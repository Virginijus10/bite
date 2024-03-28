from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Avg, Count
from .forms import UserRegisterForm, InventoryItemForm
from .models import InventoryItem, Category
from inventory.settings import LOW_QUANTITY
import numpy as np
from collections import Counter
from decimal import Decimal


class Index(TemplateView):
	template_name = 'bee_inventory/index.html'


class About_us(TemplateView):
	template_name = 'bee_inventory/about_us.html'


class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        items = InventoryItem.objects.all().order_by('id')

        category_id = request.GET.get('category')
        search_query = request.GET.get('search')

        if category_id:
            items = items.filter(category_id=category_id)
        if search_query:
            items = items.filter(name__icontains=search_query)

        low_inventory = InventoryItem.objects.filter(
            quantity__lte=LOW_QUANTITY
        )

        if low_inventory.exists():
            messages.error(request, f'Yra prekių, kurių kiekis yra mažesnis nei nustatyta riba')

        low_inventory_ids = low_inventory.values_list('id', flat=True)

        return render(request, 'bee_inventory/dashboard.html', {'items': items, 'low_inventory_ids': low_inventory_ids})


class SignUpView(View):
	def get(self, request):
		form = UserRegisterForm()
		return render(request, 'bee_inventory/signup.html', {'form': form})

	def post(self, request):
		form = UserRegisterForm(request.POST)

		if form.is_valid():
			form.save()
			user = authenticate(
				username=form.cleaned_data['username'],
				password=form.cleaned_data['password1']
			)

			login(request, user)
			return redirect('index')

		return render(request, 'bee_inventory/signup.html', {'form': form})
	

def custom_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    else:
        return render(request, 'bee_inventory/logout.html')
	

class AddItem(LoginRequiredMixin, CreateView):
	model = InventoryItem
	form_class = InventoryItemForm
	template_name = 'bee_inventory/item_form.html'
	success_url = reverse_lazy('dashboard')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['categories'] = Category.objects.all()
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)
	

class EditItem(LoginRequiredMixin, UpdateView):
	model = InventoryItem
	form_class = InventoryItemForm
	template_name = 'bee_inventory/item_form.html'
	success_url = reverse_lazy('dashboard')


class DeleteItem(LoginRequiredMixin, DeleteView):
	model = InventoryItem
	template_name = 'bee_inventory/delete_item.html'
	success_url = reverse_lazy('dashboard')
	context_object_name = 'item'	


def filter_items(request):
    filter_by = request.GET.get('filter_by')
    search_query = request.GET.get('search')
    sort_toggle = request.GET.get('sort_toggle')

    items = InventoryItem.objects.all()

    if search_query:
        try:
            search_query = Decimal(search_query)
            items = items.filter(price=search_query)
        except:
            if filter_by == 'name':
                items = items.filter(name__icontains=search_query)
            elif filter_by == 'category':
                items = items.filter(category__name__icontains=search_query)

    if sort_toggle:
        if sort_toggle == 'on':
            items = items.order_by('price')
        else:
            items = items.order_by('-price')

    average_price = items.aggregate(avg_price=Avg('price'))['avg_price']
    if average_price is not None:
        average_price = Decimal(str(average_price)).quantize(Decimal('0.01'))
    median_price = np.median([item.price for item in items])
    price_counter = Counter([item.price for item in items])
    mode_price = None
    if price_counter:
        mode_price = price_counter.most_common(1)[0][0]

    context = {
        'items': items,
        'average_price': average_price,
        'median_price': median_price,
        'mode_price': mode_price
    }
    return render(request, 'bee_inventory/dashboard.html', context)
