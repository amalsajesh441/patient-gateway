from celery import shared_task

@shared_task
def send_welcome_email(name):
    print(f"Welcome email sent to {name}")
