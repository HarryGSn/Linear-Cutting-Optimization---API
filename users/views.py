from django.views.generic.edit import FormView
from .forms import RegistrationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse

class RegistrationView(FormView):
    form_class = RegistrationForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return HttpResponse(form.as_p())

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # Create a new user object and save it
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user = User.objects.create_user(username, email, password)
            user.save()

            # Redirect to a success page
            # return HttpResponse( 'Registration successful' )
        else:
            return JsonResponse( { 'error': form.errors.as_text( ) } )
