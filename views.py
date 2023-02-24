from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect, reverse
from django.contrib.auth.models import User
from django.contrib import auth
from .models import extendedusers, extendedNgoRequest, extendedNgoAcceptedRequest
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.cache import never_cache


# Create your views here.
def index(request):
    return render(request, 'index.html')

def Register(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['confirmPassword']:
            try:
                user = User.objects.get(email=request.POST['email'])
                return render(request, 'Registration\Register.html', {'error':"Email has already been taken"})
            except User.DoesNotExist:
                user = User.objects.create_user(
                    username=request.POST['email'],
                    first_name=request.POST['firstName'],
                    last_name=request.POST['lastName'],
                    email=request.POST['email'],
                    password=request.POST['password']
                )
                userType = request.POST['userType']
                city = request.POST['city']
                newextendedusers = extendedusers(userType=userType, city=city, user=user)
                newextendedusers.save()
                auth.login(request, user)
                return render(request, 'Registration\Register.html', {'success': "You are successfully registered"})
        else:
            return render(request, 'Registration\Register.html', {'error': "Password and Confirm Password are not same"})
    else:
        return render(request, 'Registration\Register.html')

def Login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            if user.extendedusers.userType == 'ngo':
                return redirect('MainNGO')
            else:
                return redirect('MainPeople')
        else:
            return render(request, 'Registration\login.html', {'error':"Invalid Login Credentials"})
    else:
        return render(request, 'Registration\login.html')
    # return render(request, 'Registration\Login.html')

def Logout(request):
    auth.logout(request)
    return render(request, 'Registration\login.html')

def MainNGO(request):
    current_user = request.user
    username = current_user.first_name.capitalize()  + " " +current_user.last_name.capitalize()
    current_user_id = current_user.id
    donation_requests = extendedNgoRequest.objects.filter(ngo_id=current_user_id)

    current_user_id = request.user.id
    AcceptedRequest = extendedNgoAcceptedRequest.objects.filter(ngo_id=current_user_id)
    # print(AcceptedRequest)
    return render(request, 'MainNGO.html', {'username' : username, 'donation_requests': donation_requests, 'AcceptedRequest': AcceptedRequest})

def MainPeople(request):
    User = get_user_model()
    ngo_list = User.objects.filter(extendedusers__userType='ngo')
    # for i in ngo_list:
    #     ngo_list.append(i.first_name + " " + i.last_name)

    current_user = request.user
    username = current_user.first_name.capitalize()  + " " +current_user.last_name.capitalize()
    return render(request, 'MainPeople.html', {'username' : username, 'ngo_list': ngo_list})

def NgoDetail(request):
    # current user
    current_user = request.user
    username = current_user.first_name.capitalize() + " " + current_user.last_name.capitalize()

    # ngo details
    user_id = request.GET.get("id")
    User = get_user_model()
    ngo_detail = User.objects.get(id=user_id)
    ngo_city = ngo_detail.extendedusers.city

    return render(request, 'NGODetails.html', {'username': username, 'ngo_detail': ngo_detail, 'ngo_city': ngo_city})

def RequestNgo(request):
    print("request")
    if request.is_ajax():
        firstName = request.POST.get('firstName', None)
        lastName = request.POST.get('lastName', None)
        locality = request.POST.get('locality', None)
        contactNumber = request.POST.get('contactNumber', None)
        city = request.POST.get('city', None)
        pincode = request.POST.get('pincode', None)
        ngoId = request.POST.get('ngoId', None)
        print(firstName, lastName, locality, city, pincode, contactNumber, ngoId, "I am request details")

        requestNgo = extendedNgoRequest()
        requestNgo.firstName = firstName
        requestNgo.lastName = lastName
        requestNgo.locality = locality
        requestNgo.contactNumber = contactNumber
        requestNgo.city = city
        requestNgo.pinCode = pincode
        requestNgo.ngo_id = ngoId
        requestNgo.save()
        response = {
            'msg':'Successfully Requested'
        }
        print(requestNgo.firstName)
        return JsonResponse(response)
    # return render(request, 'NGODetails.html', {'success': "Successfully Requested"})

def AcceptedRequest(request):
    if request.is_ajax():
        request_id = request.POST.get('button_id', None)
        request_data = extendedNgoRequest.objects.get(id=request_id)

        acceptedRequest = extendedNgoAcceptedRequest()
        acceptedRequest.firstName = request_data.firstName
        acceptedRequest.lastName = request_data.lastName
        acceptedRequest.locality = request_data.locality
        acceptedRequest.contactNumber = request_data.contactNumber
        acceptedRequest.city = request_data.city
        acceptedRequest.pinCode = request_data.pinCode
        acceptedRequest.ngo_id = request_data.ngo_id
        acceptedRequest.request_id = request_id
        acceptedRequest.save()

        request_data.delete()

        current_user_id = request.user.id

        AcceptedRequest = extendedNgoAcceptedRequest.objects.filter(ngo_id=current_user_id)

    return render(request, 'MainPeople.html', {'AcceptedRequest': AcceptedRequest})

def DoneRequest(request):
    if request.is_ajax():
        request_id = request.POST.get('button_id', None)
        request_data = extendedNgoAcceptedRequest.objects.get(id=request_id)
        print(request_data.firstName)
        request_data.delete()

    return render(request, 'MainPeople.html')