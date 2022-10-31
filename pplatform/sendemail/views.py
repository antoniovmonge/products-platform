from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import ContactForm


def contactView(request):
    if request.method == "GET":
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            from_email = form.cleaned_data["from_email"]
            message = form.cleaned_data["message"]
            try:
                send_mail(
                    subject, message, from_email, ["admin@building-materials.com"]
                )
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            return redirect("sendemail:success")
    return render(request, "contact/email.html", {"form": form})


def successView(request):
    # return HttpResponse("Success! Thank you for your message.")
    return render(request, "contact/success.html")
