from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from cs.settings import ROWS_PER_PAGE
from product.models import Product, Courier, Comment
from product.forms import ProductCreateForm, ProductUpdateForm, CommentCreateForm
from cs_user.models import User


class ProductDetail(DetailView):
    context_object_name = 'product'
    model = Product

product_detail = ProductDetail.as_view()


class ProductList(ListView):
    context_object_name = 'products'
    queryset = Product.objects.all()
    paginate_by = ROWS_PER_PAGE

    def get_context_data(self, **kwargs):
        context = super(ProductList, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        return context

    def get_queryset(self):
        q = self.request.GET.get('q', None)
        if q:
            return Product.objects.search(q)
        return self.queryset
 
product_list = ProductList.as_view()
    

class ProductCreate(CreateView):
    form_class = ProductCreateForm
    template_name = 'product/product_create_or_update.html'    

    def form_valid(self, form):
        form.instance.user = User.objects.get(pk=self.kwargs['user_pk'])
        form.instance.status = Comment.STATUS[10]
        product = form.save()
        comment = Comment(product=product, user=self.request.user, status=Comment.STATUS[10]).save()
        return super(ProductCreate, self).form_valid(form)

product_create = ProductCreate.as_view()


class ProductUpdate(UpdateView):
    form_class = ProductUpdateForm
    template_name = 'product/product_create_or_update.html'    
  
    def get_object(self):
        return get_object_or_404(Product, pk=self.kwargs['pk'])
 
product_update = ProductUpdate.as_view()


class CommentCreate(CreateView):
    form_class = CommentCreateForm
    template_name = 'product/comment_create_or_update.html'

    def get_context_data(self, **kwargs):
        context = super(CommentCreate, self).get_context_data(**kwargs)
        context['product'] = get_object_or_404(Product, pk=self.kwargs['product_pk'])
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.product = self.get_context_data()['product']
        return super(CommentCreate, self).form_valid(form)        

comment_create = CommentCreate.as_view()

