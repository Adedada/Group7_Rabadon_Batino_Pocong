from multiprocessing import context
from django.shortcuts import render
from collections import namedtuple
from django.db.models.fields import EmailField
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import SuperUserRequiredMixin


# Create your views here.
class userView(View):
    def get(self, request):
        return render(request, 'user.html',{})

class loginView(View):
    def get(self, request):
        return render(request, 'login.html',{})

# Register Page
class registerView(View):
    def get(self, request):
        form = AgentForm()
        return render(request, 'register.html', {'form':form})

    def post(self, request):
        form = AgentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ResSystem:login_view')
        return render(request, 'register.html', {'form':form})

class homeView(View):
    def get(self, request):
        return render(request, 'home.html',{})

class aboutView(View):
    def get(self, request):
        return render(request, 'about.html',{})

class contactView(View):
    def get(self, request):
        return render(request, 'contact.html',{})
    
class addroomView(SuperUserRequiredMixin, View):
    def get(self, request):
        context = {}
        return render(request, 'addroom.html',context)    
    def post(self, request):
        form = RoomForm(request.POST)
        reservationfee = request.POST.get("reservationfee")
        location = request.POST.get("location")
        starttime = request.POST.get("starttime")
        endtime = request.POST.get("endtime")
        status = request.POST.get("status")
        
        form = Room(
                reservationfee = reservationfee,
                location = location,
                starttime = starttime,
                endtime = endtime,
                status = status
        )
        form.save()
        return redirect('ResSystem:addroom_view')

class reservationView(LoginRequiredMixin, View):
    
    def get(self, request):
        user = Agent.objects.get(username=request.user.username)
        print(user)
        room = Room.objects.filter(status="VACANT") | Room.objects.filter(client=user)

        context ={
            'room' : room
        }
        return render(request, 'reservation.html', context)    
    def post(self, request):
        if request.method == 'POST':
            if 'roomBook' in request.POST: 
                roomID = request.POST.get("roomID")
                status = "RESERVED"
                reservationfee = request.POST.get("reservationfee") 
                starttime = request.POST.get("starttime")
                endtime = request.POST.get("endtime")
                client = request.POST.get("client")
                location = request.POST.get("location")
                roomUpdate = Room.objects.filter(roomID = roomID).update(status = status, reservationfee = reservationfee, starttime = starttime, endtime = endtime,client = client, location = location)
            elif 'roomCancel' in request.POST: 
                roomID = request.POST.get("roomID")
                status = request.POST.get("status")
                client = request.POST.get("client")

                roomUpdate = Room.objects.filter(roomID = roomID).update(status = status,client = client)
            elif 'agentUpdate' in request.POST: 
                agentID = request.POST.get("agentID")
                firstname = request.POST.get("firstname") 
                lastname = request.POST.get("lastname")
                phone_number = request.POST.get("phone_number")
                email = request.POST.get("email")
                agentUpdate = Agent.objects.filter(roomID = roomID).update(status = status, reservationfee = reservationfee, starttime = starttime, endtime = endtime,client = client, location = location)
            elif 'roomCancelAll' in request.POST: 
                status = request.POST.get("status")
                key = request.POST.get("client")
                client = "None"
                roomUpdate = Room.objects.filter(client = key).update(status = status,client = client)            
        return redirect('ResSystem:reservation_view')     


# Room Dashboard View
class roomView(SuperUserRequiredMixin, View):
    def get(self, request):
        room = Room.objects.all()
        agent = Agent.objects.all()
        context = {
            'room' : room,
            'agent' : agent
        }
        return render(request, 'room.html', context)

    def post(self, request):
        if request.method == 'POST':
            if 'roomDelete' in request.POST: 
                roomID = request.POST.get("roomID")
                roomDelete = Room.objects.filter(roomID = roomID).delete()
                print('recorded deleted')

            elif 'roomUpdate' in request.POST: 
                roomID = request.POST.get("roomID")
                status = request.POST.get("status")
                reservationfee = request.POST.get("reservationfee") 
                starttime = request.POST.get("starttime")
                endtime = request.POST.get("endtime")
                client = request.POST.get("client")
                location = request.POST.get("location")
                if client == 'None':
                    status = "VACANT"
                elif client == 'Maintenance':
                    status = "UNDER MAINTENANCE"
                else :
                    status = 'RESERVED'
                contactUpdate = Room.objects.filter(roomID = roomID).update(status = status, reservationfee = reservationfee, starttime = starttime, endtime = endtime,client = client, location = location)
            elif 'agentDelete' in request.POST: 
                agentID = request.POST.get("agentID")
                agentDelete = Agent.objects.filter(agentID = agentID).delete()
                print('recorded deleted')
            elif 'agentUpdate' in request.POST: 
                agentID = request.POST.get("agentID")
                firstname = request.POST.get("firstname")
                lastname = request.POST.get("lastname") 
                phone_number = request.POST.get("phone_number")
                email = request.POST.get("email")
                agentUpdate = Agent.objects.filter(agentID = agentID).update(firstname = firstname, lastname = lastname, phone_number = phone_number, email = email)
        return redirect('ResSystem:room_view')       
    #         elif 'errorDeleteBtn' in request.POST: # CABAHUG ERROR DELETE
    #             errorID = request.POST.get("errorDel")
    #             errorDelete = Error.objects.filter(errorID = errorID).delete()
    #             print('recorded deleted')

    #         elif 'errorUpdateBtn' in request.POST: # CABAHUG ERROR UPDATE
    #             errorID = request.POST.get("errorID")
    #             message = request.POST.get("message")
    #             code = request.POST.get("code") 
    #             explination = request.POST.get("explination")
    #             fix = request.POST.get("fix")
    #             errorUpdate = Error.objects.filter(errorID = errorID).update(message = message, code = code, explination = explination, fix = fix)

    #         elif 'userDeleteBtn' in request.POST: # POCONG USER DELETE
    #             userID = request.POST.get("userDel")
    #             errorDelete = User.objects.filter(userID = userID).delete()
    #             print('recorded deleted') 

    #         elif 'userUpdateBtn' in request.POST: # POCONG USER UPDATE 
    #             userID = request.POST.get("userID")
    #             firstname = request.POST.get("firstname")
    #             lastname = request.POST.get("lastname") 
    #             course = request.POST.get("course")
    #             year = request.POST.get("year")
    #             email = request.POST.get("email")
    #             userUpdate = User.objects.filter(userID = userID).update(firstname = firstname, lastname = lastname, course = course, year = year, email = email) 

    #         elif 'agentDeleteBtn' in request.POST: # RABADON USER DELETE
    #             agentID = request.POST.get("agentDel")
    #             errorDelete = Agent.objects.filter(agentID = agentID).delete()
    #             print('recorded deleted') 

    #         elif 'agentUpdateBtn' in request.POST: # RABADON USER UPDATE 
    #             agentID = request.POST.get("agentID")
    #             firstname = request.POST.get("firstname")
    #             lastname = request.POST.get("lastname") 
    #             phonenumber = request.POST.get("phone_number")
    #             email = request.POST.get("email")
    #             agentUpdate = Agent.objects.filter(agentID = agentID).update(firstname = firstname, lastname = lastname,  email = email, phone_number = phonenumber) 




    #     return redirect('codeApp:admindash_View')        