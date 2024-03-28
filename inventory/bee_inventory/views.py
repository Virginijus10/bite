from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from .forms import UserRegisterForm, InventoryItemForm
from .models import InventoryItem, Category
from inventory.settings import LOW_QUANTITY
from django.contrib import messages
from django.contrib.auth import logout

# Create your views here.


class Index(TemplateView):
	template_name = 'bee_inventory/index.html'


class About_us(TemplateView):
	template_name = 'bee_inventory/about_us.html'


# class Dashboard(LoginRequiredMixin, View):
# 	def get(self, request):
# 		items = InventoryItem.objects.filter(user=self.request.user.id).order_by('id')

# 		low_inventory = InventoryItem.objects.filter(
# 			#user=self.request.user.id,
# 			quantity__lte=LOW_QUANTITY
# 		)

# 		if low_inventory.count() > 0:
# 			if low_inventory.count() > 1:
# 				messages.error(request, f'{low_inventory.count()} items have low inventory')
# 			else:
# 				messages.error(request, f'{low_inventory.count()} item has low inventory')

# 		low_inventory_ids = InventoryItem.objects.filter(
# 			user=self.request.user.id,
# 			quantity__lte=LOW_QUANTITY
# 		).values_list('id', flat=True)

# 		return render(request, 'bee_inventory/dashboard.html', {'items': items, 'low_inventory_ids': low_inventory_ids})

# class Dashboard(LoginRequiredMixin, View):
#     def get(self, request):
#         # Gauti visus inventoriaus elementus
#         items = InventoryItem.objects.all().order_by('id')

#         # Gauti inventoriaus elementus, kurių kiekis yra mažesnis arba lygus nustatytam mažiausiam kiekiui
#         low_inventory = InventoryItem.objects.filter(
#             quantity__lte=LOW_QUANTITY
#         )

#         if low_inventory.exists():
#             messages.error(request, f'Yra prekių, kurių kiekis yra mažesnis nei nustatyta riba')

#         low_inventory_ids = low_inventory.values_list('id', flat=True)

#         return render(request, 'bee_inventory/dashboard.html', {'items': items, 'low_inventory_ids': low_inventory_ids})




class Dashboard(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

    def get(self, request):
        items = InventoryItem.objects.all().order_by('id')

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
	

# def logout(request):
#     logout(request)
#     return redirect('bee_inventory/logout.html')
	

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