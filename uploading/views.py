from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.shortcuts import render,  redirect
from .forms import UploadDocumentForm
import os
import json
from django.core.files.storage import default_storage
from django.conf import settings
from celery.result import AsyncResult
from .tasks import send_verification_email


def task_worker(**kwargs):
    data = json.loads(kwargs['data'])
    res = send_verification_email.delay(kwargs=data)
    return res.id


class TaskGetter(TemplateView):
    def get(self, request, *args, **kwargs):
        task_id = request.GET.get('task_id')
        context = {'title': 'Work\'s result'}
        if task_id:
            res = AsyncResult(task_id)
            context['message'] = f'Job progress status is  {res.status}'
        else:
            context['message'] = 'No ID'
        return render(request, 'uploading/result.html', context)


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'uploading/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context

    def get_success_url(self):
        return reverse_lazy('upload_data')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


class Upload(FormView):
    template_name = 'uploading/upload.html'
    form_class = UploadDocumentForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = dict()
        context['title'] = 'File upload'
        context['authorization_required'] = 'Authorization is required for further work.'
        context['form'] = UploadDocumentForm()
        return context

    def post(self, request, *args, **kwargs):
        form = UploadDocumentForm(request.POST, request.FILES)
        if not form.is_valid():
            form = UploadDocumentForm()
            error = 'Error! Valid file format is "xml" or "yml"'
            return render(request, "uploading/upload.html", {'errors': error, "form": form})
        else:
            save_path = os.path.join(settings.MEDIA_ROOT, str(request.FILES['file']))
            path = default_storage.save(save_path, request.FILES['file'])
            clean_data = {el: str(form.cleaned_data[el]) for el in form.cleaned_data}
            clean_data['path'] = path
            order_id = task_worker(data=json.dumps(clean_data))
            checkin_url = f'/check_order/?task_id={order_id}'
            return redirect(checkin_url)


