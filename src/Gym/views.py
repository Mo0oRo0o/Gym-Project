from django.shortcuts import render 

from django.db.models import Count

from .models import GymClass , Specialization , Trainer , Member , Branch , Equipment , damaged_Equipment

# Create your views here.

def all_members(request) : # request is a parameter by default on views functions

    members = Member.objects.all()

    context = {
        "data" : members
    }

    return render(request , "Gym/Show_all_members.html" , context) # request , html page and context is the data is shown on html page

def Session_datail(request , GymClass_id) :

    Session = GymClass.objects.select_related("trainer").prefetch_related("members").get(id = GymClass_id)

    Session.discount()

    context = {
        "Session" : Session
    }

    return render(request , "Gym/Session_detail.html" , context)

def Trending_Sessions(request) :

    Sessions = GymClass.objects.select_related("trainer").prefetch_related("members").all().trending()

    context = {
        "Sessions" : Sessions
    }

    return render(request , "Gym/Trend_Session.html" , context)


def damaged(request) :

    damaged_equipments = damaged_Equipment.objects.select_related("branch").all().filter(is_damaged = True)

    context = {
        "damaged_equipments" : damaged_equipments
    }

    return render(request , "Gym/damage_equ.html" , context)
