from django.shortcuts import render

# Create your views here.
def notice_board(request):
    return render(request, 'notice-board.html', {
          'firstname' : request.user.first_name,
          'lastname' : request.user.last_name,
     })