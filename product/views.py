# -* - coding: utf-8 -*-
import logging
import mimetypes

from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.core.servers.basehttp import FileWrapper
from django.utils.encoding import smart_str

from cs.settings import ROWS_PER_PAGE
from product.models import Product, Courier, Comment
from product.forms import ProductForm, CommentForm, ClientCommentForm
from product.constants import get_status_flow, NEW, CLOSED
from cs_user.models import User
from base.views import UserCheckAccess


# pdf imports
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
import ho.pisa as pisa
import cStringIO as StringIO
import cgi
from cs.settings import STATIC_URL


class ProductDetail(UserCheckAccess, DetailView):
    context_object_name = 'product'
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context['closed'] = CLOSED
        return context

product_detail = ProductDetail.as_view()


class ProductPdf(ProductDetail, UserCheckAccess):
    template_name = 'product/product_pdf.html'

    def write_pdf(self, template_src, context_dict):
        template = get_template(template_src)
        context = Context(context_dict)
        context['product'] = self.get_object()
        context['client'] = self.get_object().user
        context['user'] = self.request.user
        context['company'] = self.request.user.company

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


class ProductList(ListView, UserCheckAccess):
    context_object_name = 'products'
    paginate_by = ROWS_PER_PAGE

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_client_with_access:
            return redirect(reverse('user_detail', args=[request.user.pk]))
        return super(ProductList, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProductList, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['status_filter'] = int(self.kwargs.get('status', 0))
        context['key'] = int(self.kwargs.get('key', 1))
        return context

    def get_queryset(self):
        status = self.kwargs.get('status', None)
        if status:
            queryset = Product.objects.filter(status=status)

        key = self.kwargs.get('key', 1)
        if key:
            queryset = Product.objects.who(user=self.request.user, key=int(key))

        q = self.request.GET.get('q', None)
        if q:
            return queryset.search(q, queryset=queryset)
        
        try:    
            return queryset 
        except UnboundLocalError:
            return Product.objects.all()

product_list = ProductList.as_view()
    

class ProductCreate(UserCheckAccess, CreateView):
    form_class = ProductForm
    template_name = 'product/product_create_or_update.html'    
    context_object_name = 'product'

    def form_valid(self, form):
        form.instance.user = User.objects.get(pk=self.kwargs['user_pk'])
        form.instance.company = self.request.user.company
        form.instance.status = form.instance.init_status
        product = form.save()
        comment = Comment(product=product, user=self.request.user, status=form.instance.init_status).save()
        messages.add_message(self.request, messages.SUCCESS, 'Zgłoszenie zostało dodane')
        return super(ProductCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProductCreate, self).get_context_data(**kwargs)
        context['client'] = get_object_or_404(User, pk=self.kwargs['user_pk'])
        return context

product_create = ProductCreate.as_view()


class ProductUpdate(UserCheckAccess, UpdateView):
    form_class = ProductForm
    template_name = 'product/product_create_or_update.html'    
    context_object_name = 'product'

    def get_object(self):
        return get_object_or_404(Product, pk=self.kwargs['pk'])
 
    def get_context_data(self, **kwargs):
        context = super(ProductUpdate, self).get_context_data(**kwargs)
        context['client'] = get_object_or_404(User, pk=self.kwargs['user_pk'])
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Zgłoszenie zostało zaktualizowane')
        return super(ProductUpdate, self).form_valid(form)

product_update = ProductUpdate.as_view()


class CommentCreate(UserCheckAccess, CreateView):
    form_class = CommentForm
    template_name = 'product/comment_create_or_update.html'

    def get_form_class(self):
        if self.request.user.is_client_with_access:
            return ClientCommentForm
        return CommentForm

    def get_product(self):
        return get_object_or_404(Product, pk=self.kwargs['product_pk'])

    def get_context_data(self, **kwargs):
        context = super(CommentCreate, self).get_context_data(**kwargs)
        context['product'] = self.get_product()
        context['closed'] = CLOSED
        return context

    def get_form(self, form_class):
        form = super(CommentCreate, self).get_form(form_class)
        submit = self.request.POST.get('submit', None)

        if self.get_product().status == CLOSED:  # you can still comment but no more costs after product has been closed
            del form.fields['cost_service']
            del form.fields['cost_hardware']
            del form.fields['cost_transport']

        if submit and int(submit) > 0:  # status bump
            form.fields['description'].required = False
            form.instance.status = int(submit)
        else:  # just a comment
            form.instance.status = self.get_product().status 
            
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        product = self.get_context_data()['product']
        form.instance.product = product

        result = super(CommentCreate, self).form_valid(form)        
        product.save()
        messages.add_message(self.request, messages.SUCCESS, 'Komentarz został dodany')
        return result

comment_create = CommentCreate.as_view()


class ServeAttachment(UserCheckAccess, View):

    def get_file(self):
        return Comment.objects.get(pk=self.kwargs['pk']).attachment

    def get(self, request, *args, **kwargs):
        file_obj = self.get_file()
        file_name = smart_str(file_obj.name)
        mime_type_guess = mimetypes.guess_type(file_name)
        response = HttpResponse(FileWrapper(file_obj.file), mimetype=mime_type_guess[0])
        response['Content-Disposition'] = 'attachment; filename=%s' % file_name
        return response

serve_attachment = ServeAttachment.as_view()


class ServeLogo(ServeAttachment):

    def get_file(self):
        return self.request.user.company.logo
        
serve_logo = ServeLogo.as_view()

