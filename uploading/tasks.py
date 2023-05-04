import os
from decouple import config
from exist.celery import app
from .data_processing import *
from django.core.mail import send_mail


@app.task
def send_verification_email(execution_status=None, **kwargs):
    path_remove = kwargs['kwargs']['path']
    try:
        processing(**kwargs)
        os.remove(f'media/{path_remove}')
        execution_status = f'Data from file "{path_remove}" have been worked out successfully'
        print(execution_status)
    except Exception as ex:
        execution_status = f'Processing file {path_remove} has ended with an error.\nError is {ex}'
        print(execution_status)
    finally:
        send_mail(
             'Execution Status',
             f'{execution_status}',
             config('SENDER_EMAIL'),
             [config('RECIPIENT_EMAIL')],
             fail_silently=False,
          )





