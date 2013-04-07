from django.template import Context, Template
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives


def get_email_body(email_type, html=True, context_dict={}):

    template_src = "mail/%s_%s.txt" % (email_type, 'html' if html else 'plain')
    template = get_template(template_src)
    context = Context(context_dict)
    return template.render(context) 


def send_email(subject, from_email, to_email, text_content, html_content):
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def welcome_email(user):
    context = {'user': user}
    text_content = get_email_body('new_user', html=False, context_dict=context) 
    html_content = get_email_body('new_user', html=True, context_dict=context)
    send_email('Witamy w systemie', 'llechowicz@gmail.com', 'llechowicz@gmail.com', text_content, html_content)

