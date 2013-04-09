# -* - coding: utf-8 -*-
import logging

from django.template import Context, Template
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

from cs.settings import DOMAIN


def get_email_body(email_type, html=True, context_dict={}):

    template_src = "mail/%s_%s.txt" % (email_type, 'html' if html else 'plain')
    template = get_template(template_src)
    context = Context(context_dict)
    return template.render(context) 


def send_email(subject, from_email, to_emails, plain, html):
    try:
        msg = EmailMultiAlternatives(subject, plain, from_email, to_emails)
        msg.attach_alternative(html, "text/html")
        msg.send()
    except Exception:
        logging.exception(e)


def get_plain_and_html(email_type, context):
    plain = get_email_body(email_type, html=False, context_dict=context) 
    html = get_email_body(email_type, html=True, context_dict=context)
    return plain, html

def welcome_email(user):
    context = {
        'user': user,
        'domain': DOMAIN,
    }
    plain, html = get_plain_and_html('new_user', context)
    send_email(u'%s: witamy w systemie serwisowym Dziobak' % user.company, user.company.from_email, [user.email], plain, html)


def notify_email(comment):
    context = {
        'domain': DOMAIN,
        'editor': comment.user,
        'new_status': comment.status,
        'product': comment.product,
        'company': comment.user.company
    }
     
    from cs_user.models import User
    email = comment.user.company.user_set.filter(role__in=User.EMPLOYEE_KEYS).values_list('email', flat=True)
    email = list(emails)
    email.append(comment.user)
 
    plain, html = get_plain_and_html('notify', context)
    send_email(u'Dziobak - zgłoszenie %s zmieniło status' % comment.product, user.company.from_email, set(emails), plain, html)

