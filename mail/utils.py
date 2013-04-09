# -* - coding: utf-8 -*-
from django.template import Context, Template
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives


def get_email_body(email_type, html=True, context_dict={}):

    template_src = "mail/%s_%s.txt" % (email_type, 'html' if html else 'plain')
    template = get_template(template_src)
    context = Context(context_dict)
    return template.render(context) 


def send_email(subject, from_email, to_email, plain, html):
    msg = EmailMultiAlternatives(subject, plain, from_email, [to_email])
    msg.attach_alternative(html, "text/html")
    msg.send()


def get_plain_and_html(email_type, context):
    plain = get_email_body(email_type, html=False, context_dict=context) 
    html = get_email_body(email_type, html=True, context_dict=context)
    return plain, html

def welcome_email(user):
    context = {'user': user}
    plain, html = get_plain_and_html('new_user', context)
    send_email(u'%s: witamy w systemie serwisowym Dziobak' % user.company, user.company.from_email, user.email, plain, html)


def notify_email(comment):
    context = {
        'editor': comment.user,
        'new_status': comment.status,
        'product': comment.product,
        'company': comment.user.company
    }
  
    plain, html = get_plain_and_html('notify', context)
    send_email(u'Dziobak - zgłoszenie %s zmieniło status' % comment.product, 'llechowicz@gmail.com', 'llechowicz@gmail.com', plain, html)

