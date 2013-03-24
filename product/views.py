from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from cs.settings import ROWS_PER_PAGE
from product.models import Product, Courier, Comment
from product.forms import ProductCreateForm, ProductUpdateForm, CommentCreateForm
from cs_user.models import User

# pdf imports
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
import ho.pisa as pisa
import cStringIO as StringIO
import cgi
from cs.settings import STATIC_URL


class ProductDetail(DetailView):
    context_object_name = 'product'
    model = Product

product_detail = ProductDetail.as_view()


class ProductPdf(ProductDetail):
    template_name = 'product/product_pdf.html'

    def write_pdf(self, template_src, context_dict):
        template = get_template(template_src)
        context = Context(context_dict)
        context['product'] = self.get_object()
        context['client'] = self.get_object().user
        context['user'] = self.request.user

        html  = template.render(context)
        result = StringIO.StringIO()
        pdf = pisa.pisaDocument(StringIO.StringIO(
            html.encode("UTF-8")), result)
        if not pdf.err:
            return HttpResponse(result.getvalue(), mimetype='application/pdf')
        return HttpResponse('Gremlins ate your pdf! %s' % cgi.escape(html))
    
    def get(self, request, *args, **kwargs):
        return self.write_pdf(self.template_name, {'pagesize' : 'A4'})

product_pdf = ProductPdf.as_view()


class ProductList(ListView):
    context_object_name = 'products'
    paginate_by = ROWS_PER_PAGE

    def get_context_data(self, **kwargs):
        context = super(ProductList, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        return context

    def get_queryset(self):
        Product.objects.company = self.request.user.company
        q = self.request.GET.get('q', None)
        if q:
            return Product.objects.search(q)
        return Product.objects.all()
 
product_list = ProductList.as_view()
    

class ProductCreate(CreateView):
    form_class = ProductCreateForm
    template_name = 'product/product_create_or_update.html'    
    context_object_name = 'product'

    def form_valid(self, form):
        form.instance.user = User.objects.get(pk=self.kwargs['user_pk'])
        form.instance.company = self.request.user.company
        form.instance.status = Comment.S10
        product = form.save()
        comment = Comment(product=product, user=self.request.user, status=Comment.S10).save()
        return super(ProductCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProductCreate, self).get_context_data(**kwargs)
        context['client'] = get_object_or_404(User, pk=self.kwargs['user_pk'])
        return context

product_create = ProductCreate.as_view()


class ProductUpdate(UpdateView):
    form_class = ProductUpdateForm
    template_name = 'product/product_create_or_update.html'    
    context_object_name = 'product'
  
    def get_object(self):
        return get_object_or_404(Product, pk=self.kwargs['pk'])
 
    def get_context_data(self, **kwargs):
        context = super(ProductUpdate, self).get_context_data(**kwargs)
        context['client'] = get_object_or_404(User, pk=self.kwargs['user_pk'])
        return context

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

