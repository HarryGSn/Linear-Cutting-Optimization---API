from django.views.generic.edit import FormView
from .forms import RegistrationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError
class RegistrationView(FormView):
    form_class = RegistrationForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return HttpResponse(form.as_p())

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                # Create a new user object and save it
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                email = form.cleaned_data['email']
                user = User.objects.create_user(username, email, password)
                user.save()
                return JsonResponse( { 'message': 'Registration successful' }, status=200 )
            except IntegrityError:
                return JsonResponse( { 'error': 'failed to register, user already exists' }, status=400 )
            except Exception:
                return JsonResponse( { 'error': 'failed to register' }, status=422 )
            # Redirect to a success page
        else:
            return JsonResponse( { 'error': form.errors.as_text( ) }, status=403 )
