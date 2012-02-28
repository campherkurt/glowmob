from django.template import RequestContext
from django.shortcuts import render_to_response
from apps.contact.forms import ContactForm
from apps.contact.models import Contact
from django.contrib import messages

def index(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            contact = Contact(
                name = request.POST["name"],
                contact = request.POST["contact"],
                message = request.POST["message"]
            )

            contact.save()

            messages.add_message(request, messages.SUCCESS, "Your post was successfull.")

            form = ContactForm()
    else:
        form = ContactForm()
        
    return render_to_response("contact/index.html", {
        "form": form
    }, context_instance=RequestContext(request))