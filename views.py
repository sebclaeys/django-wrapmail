__author__ = 'sebastienclaeys'


from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.template import Template, Context
from django.shortcuts import redirect, render
from common.decorators import staff_required
from common.shortcut import success_json_response, error_json_response
from django.contrib import messages
import mailator.forms as form
from django.conf import settings as conf
import mailator.models as model
import mailator.libs.helper as helper
import mailator.libs.api as api
import base64
from django.views.decorators.csrf import csrf_exempt
import mailator.tasks as task_queue

from datetime import datetime, timedelta


@login_required
@staff_required
def dashboard(request):
    connections = model.Connection.objects.all()
    layouts = model.Layout.objects.all()
    optout_categories = model.OptoutCategory.objects.all()
    listes = model.EmailList.objects.all()
    emails = model.Type.objects.all()
    return render(request, 'mailator/pages/dashboard.html', locals())

# @login_required
# @staff_required
# def lists(request):
#     layouts = model.Layout.objects.all()
#     listes = model.EmailList.objects.all()
#     return render(request, 'mailator/pages/lists.html', locals())
#
# @login_required
# @staff_required
# def emails(request):
#     emails = model.Type.objects.all()
#
#     return render(request, 'mailator/pages/emails.html', locals())
#
# @login_required
# @staff_required
# def subscriptions(request):
#     connections = model.Connection.objects.all()
#     return render(request, 'mailator/pages/subscribtions.html', locals())
#
#
# @login_required
# @staff_required
# def connection(request):
#     connections = model.Connection.objects.all()
#     return render(request, 'mailator/pages/connections.html', locals())


@login_required
@staff_required
def tasks(request):
    tasks = model.Task.objects.filter(completed=False)
    return render(request, 'mailator/pages/tasks.html', locals())


@login_required
@staff_required
def blacklist(request):
    if request.method == 'POST':
        emails = map(lambda x: x.strip(), request.POST['emails'].replace(';', ',').replace(' ', ',').split(','))
        added = model.Blacklist.objects.add_emails(emails)
        messages.success(request, '%d emails added to the blacklist' % added)

    emails = model.Blacklist.objects.all().order_by('-id')[:100]
    file_form = form.UploadListeForm()

    return render(request, 'mailator/pages/blacklist.html', locals())


@login_required
@staff_required
def send_email(request):
    return render(request, 'mailator/pages/send_email.html')


@login_required
@staff_required
def edit_email(request, eid):
    eid = int(eid)
    if eid > 0:
        email = model.Type.objects.get(pk=eid)
    else:
        email = model.Type()
        if request.method != 'POST':
            email.id = 0

    if request.method == 'POST':
        email_form = form.EmailTypeForm(data=request.POST, instance=email)
        if email_form.is_valid():
            email_form.save()
            messages.success(request, 'Email saved')
            return redirect(edit_email, email.id)
        else:
            messages.error(request, 'Unable to save email')
    else:
        email_form = form.EmailTypeForm(instance=email)

    return render(request, 'mailator/pages/edit_email.html', locals())


@login_required
@staff_required
def edit_template(request, eid):
    eid = int(eid)
    available_languages =  dict(conf.LANGUAGES).keys()
    email = model.Type.objects.get(pk=eid)
    templates = []
    for lang in available_languages:
        template = email.template_set.filter(lang=lang)
        if template:
            template = template[0]
            template.exists = True
        else:
            template = model.Template(lang=lang, id=0)
            template.exists = False
        template.form = form.TemplateForm(instance=template)
        if not len(templates):
            template.is_active = True
        templates.append(template)

    return render(request, 'mailator/includes/edit_template.html', {'templates': templates, 'email': email})


@login_required
@staff_required
def save_template(request, eid, lang):
    eid = int(eid)
    email = model.Type.objects.get(pk=eid)
    template = email.template_set.filter(lang=lang)
    if template:
        template = template[0]
    else:
        template = model.Template(lang=lang, email_type=email)

    if request.method == 'POST':
        template_form = form.TemplateForm(request.POST, request.FILES, instance=template)
        if template_form.is_valid():
            template_form.save()
            messages.success(request, 'Template saved')
        else:
            messages.error(request, 'Unable to save template')
    else:
        template_form = form.TemplateForm(instance=template)

    return redirect(edit_email, eid)


@login_required
@staff_required
def preview_layout(request, lid):
    layout = model.Layout.objects.get(pk=int(lid))
    ctx = Context({})
    html_content = Template(layout.content % {'content': '[content]', 'optout_link': '[optout_link]'}).render(ctx)

    return HttpResponse(html_content)


@login_required
@staff_required
def preview_template(request, eid, tid):
    tid = int(tid)
    eid = int(eid)
    email = model.Type.objects.get(pk=eid)
    layout = email.layout
    ctx = Context({})
    if tid:
        template = model.Template.objects.get(pk=int(tid))
        subject = Template(template.subject).render(ctx)
    else:
        template = None
    html_content = Template(layout.content % {'content': template.html_content.replace('{%', '[').replace('%}', ']') if template else '', 'optout_link': '[optout_link]'}).render(ctx)
    text_content = helper.html_to_text(html_content).replace('\n', '<br>')
    return render(request, 'mailator/includes/template_preview.html', locals())


@login_required
@staff_required
def edit_list(request, lid):
    lid = int(lid)
    if lid:
        liste = model.EmailList.objects.get(pk=lid)
        file_form = form.UploadListeForm()

    else:
        liste = model.EmailList()
        if request.method != 'POST':
            liste.id = 0

    if request.method == 'POST':
        liste_form = form.EmailListForm(data=request.POST, instance=liste)
        if liste_form.is_valid():
            liste_form.save()
            messages.success(request, 'Liste saved')
            return redirect(edit_list, liste.id)
        else:
            messages.error(request, 'Unable to save email')
    else:
        liste_form = form.EmailListForm(instance=liste)

    return render(request, 'mailator/pages/edit_list.html', locals())



@login_required
@staff_required
def compute_stats(request, lid):
    task_queue.compute_stats.delay(lid)
    return HttpResponse("Task queued")


@login_required
@staff_required
def edit_task(request, tid):
    tid = int(tid)
    if tid:
        task = model.Task.objects.get(pk=tid)
    else:
        task = model.Task()
        if request.method != 'POST':
            task.id = 0

    if request.method == 'POST':
        task_form = form.TaskForm(data=request.POST, instance=task)
        if task_form.is_valid():
            task_form.save()
            messages.success(request, 'Task saved')
            return redirect(edit_task, task.id)
        else:
            messages.error(request, 'Unable to save the task')
    else:
        task_form = form.TaskForm(instance=task)

    return render(request, 'mailator/pages/edit_task.html', locals())



@login_required
@staff_required
def play_task(request, tid):
    tid = int(tid)
    import mailator.tasks as task_queue
    task_queue.launch_task.delay(tid)
    import time
    time.sleep(1)
    return redirect(edit_task, tid)


@login_required
@staff_required
def task_logs(request, tid):
    tid = int(tid)
    task = model.Task.objects.get(pk=tid)
    return render(request, 'mailator/includes/task_logs.html', locals())


@login_required
@staff_required
def task_status(request, tid):
    tid = int(tid)
    task = model.Task.objects.get(pk=tid)
    return render(request, 'mailator/includes/task_status.html', locals())


@login_required
@staff_required
def upload_list(request, lid):
    lid = int(lid)
    liste = model.EmailList.objects.get(pk=lid)
    if request.method == 'POST':
        file_form = form.UploadListeForm(request.POST, request.FILES)
        if file_form.is_valid():
            import codecs
            f = codecs.EncodedFile(request.FILES['file'], "utf-8")
            liste.processItems(f.readlines())
            messages.success(request, 'File processed')
            return success_json_response({'msg': 'File processed'})
    return error_json_response({'msg': 'Unable to process input file'})


@login_required
@staff_required
def upload_blacklist(request):
    if request.method == 'POST':
        file_form = form.UploadListeForm(request.POST, request.FILES)
        if file_form.is_valid():
            import codecs
            f = codecs.EncodedFile(request.FILES['file'], "utf-8")
            added = model.Blacklist.objects.add_emails(f.readlines())
            messages.success(request, '%d emails added to the blacklist' % added)
            return success_json_response({'msg': '%d emails added to the blacklist' % added})
    return error_json_response({'msg': 'Unable to process input file'})


@csrf_exempt
def mandrill_events(request):
    if request.method == 'POST':
        import simplejson
        # data = simplejson.loads(request.POST)
        task_queue.process_mandrill_events.delay(simplejson.loads(request.POST['mandrill_events']))
        return HttpResponse("OK")
    return HttpResponse("Must be a POST request")


def unsubscribe(request, cid, email):
    cid = int(cid)
    email = base64.b64decode(email)
    api.optout(email, cid)
    messages.success(request, 'You have been unsubscribed successfully !')
    return render(request, 'mailator/pages/optout.html', {})
