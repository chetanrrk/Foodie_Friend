from django.shortcuts import render

def home(request):
    context = {
        'menus' : 'abc',
    }
    return render(request, 'foodie_friend_app/index.html', context)
