from django.shortcuts import render
from authapp.views import *
# Create your views here.
def she_main(request):
     return render(request, 'she.html', {
          'firstname' : request.user.first_name,
          'lastname' : request.user.last_name,
     })