from django.shortcuts import render, reverse, redirect
from django.views import View
from django.core.mail import EmailMultiAlternatives  # импортируем класс для создание объекта письма с html
# from datetime import datetime
from .models import Appointment
from django.template.loader import render_to_string
from django.core import mail
from newsportal.models import Subscribe
from django.contrib.auth.models import User



class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'make_appointment.html', {})

    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            name=request.POST['name'],
            message=request.POST['message'],
        )
        appointment.save()

        # получаем наш html
        html_content = render_to_string(
            'appointment_created.html',
            {
                'appointment': appointment,
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'{appointment.name} ',
            body=appointment.message,  # это то же, что и message
            from_email='',
            to=['xapu3ma@gmail.com'],  # это то же, что и recipients_list
        )

        msg.attach_alternative(html_content, "text/html")  # добавляем html
        msg.send()  # отсылаем
        return redirect('appointments:make_appointment')
