from django.shortcuts import render

from .forms import TestForm



def index(request):


    form = TestForm()



    return render(request, "lobby/lobby.html", {"form": form})
