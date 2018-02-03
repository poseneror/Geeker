import os
import string
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render
from django.template import RequestContext, loader
from .forms import UserCreationForm, AuthenticationForm, ReviewForm, RequestForm, UserChangeForm
from .models import User, Ticket, TicketRequest
from django.core.mail import send_mail


def index(request):
    latest_profiles = User.objects.filter(is_supplier=False).order_by('-id')[:4]
    form_response = ""
    if request.method == 'POST':
        request_form = RequestForm(data=request.POST)
        if request_form.is_valid():
            request = request_form.save()
            request_form = RequestForm()
            form_response = "Your request has been sent!"
            return HttpResponseRedirect('/geeker/thankyou/1')
    else:
        request_form = RequestForm()
    context = RequestContext(request, {
        'latest_profiles': latest_profiles,
        'request_form': request_form,
        'form_response': form_response,
        'scrollers': True
    })
    return render(request, 'Geeker/index.html', context)


def signup(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST, request.FILES)
        if user_form.is_valid():
            user = user_form.save()
            if 'image' in request.FILES:
                user.image = user_form.cleaned_data['image']
            user.save()
            user = authenticate(email=request.POST['email'], password=request.POST['password1'])
            django_login(request, user)
            return HttpResponseRedirect('/geeker/')
        else:
            return render(request, 'Geeker/signup.html', {'user_form': user_form})
    else:
        user_form = UserCreationForm()
        return render(request, 'Geeker/signup.html', {'user_form': user_form})


def login(request):
    if request.method == 'POST':
        user = authenticate(email=request.POST['email'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                django_login(request, user)
                return HttpResponseRedirect('/geeker/')
    return HttpResponseRedirect('/geeker/')


def logout(request):
    django_logout(request)
    return HttpResponseRedirect('/geeker/')


def profile(request, profile_id):
    try:
        profile = User.objects.get(pk=profile_id)
    except User.DoesNotExist:
        raise Http404("Profile does not exist")
    try:
        reviews = Ticket.objects.filter(assigned=profile, reviewed=True)
    except Ticket.DoesNotExist:
        reviews = []
    return render(request, 'Geeker/profile.html', {"profile": profile, "reviews": reviews})


def profileEdit(request, profile_id):
    if request.method == 'POST':
        user_form = UserChangeForm(request.POST, request.FILES)
        if user_form.is_valid():
            user = user_form.save()
            if 'image' in request.FILES:
                user.image = user_form.cleaned_data['image']
            user.save()
            return HttpResponseRedirect('/geeker/')
        else:
            return render(request, 'Geeker/signup.html', {'user_form': user_form})
    else:
        user_form = UserCreationForm()
        return render(request, 'Geeker/signup.html', {'user_form': user_form})

@login_required
def recruit(request, page):
    if int(page) < 1:
        page = 1
    limit = 6
    start = (int(page)-1) * limit
    end = start + limit
    current_user = request.user
    if not current_user.is_supplier:
        return HttpResponseRedirect('/geeker/')
    latest_profiles = User.objects.filter(is_supplier=False).exclude(freelancers=current_user).order_by('-id')[start:end]
    geek_count = User.objects.filter(is_supplier=False).exclude(freelancers=current_user).count()
    if geek_count % limit > 0:
        pages = round(geek_count/limit)+1
    else:
        pages = round(geek_count/limit)
    context = RequestContext(request, {
        'latest_profiles': latest_profiles, 'geek_count': geek_count, 'current': int(page), 'pages': range(1, pages)
    })
    return render(request, 'Geeker/recruit.html', context)

@login_required
def tickets(request):
    current_user = request.user
    if current_user.is_supplier:
        latest_tickets = Ticket.objects.filter(supplier=None, ticketrequest__isnull=True).order_by('-id')[:10]
        my_tickets = Ticket.objects.filter(supplier=current_user, solved=False).order_by('id')[:10]
        pending_tickets = []
    else:
        latest_tickets = Ticket.objects.filter(assigned=current_user, solved=False).order_by('id')[:10]
        my_tickets = Ticket.objects.filter(assigned=current_user, solved=True).order_by('id')[:10]
        pending_tickets = TicketRequest.objects.filter(assigned=current_user).order_by('id')[:10]
    context = RequestContext(request, {
            'latest_tickets': latest_tickets, 'my_tickets': my_tickets, 'pending_tickets': pending_tickets
        })
    return render(request, 'Geeker/tickets.html', context)

@login_required
def assign(request, ticket_id):
    try:
        ticket = Ticket.objects.get(pk=ticket_id)
    except Ticket.DoesNotExist:
        raise Http404("Request does not exist")
    current_user = request.user
    if current_user.is_supplier:
        if request.method == 'POST':
            if not hasattr(ticket, 'ticketrequest'):
                assigned = User.objects.get(pk=request.POST['fl'])
                ticket.supplier = current_user
                ticket.save()
                ticket_request = TicketRequest(ticket=ticket, assigned=assigned)
                ticket_request.save()
    elif ticket.assigned == current_user:
        if request.method == "POST":
            ticket.solved = True
            ticket.save()
            url = "http://localhost:8000/geeker/review/" + ticket_id + "/"
            html_message = "<h1>Thank you for using Geeker's service</h1>" + \
                           "<p>In order to keep our edge, we incorrage our customers to send reviews regarding " \
                           "the service they've received.</p>" + "<p>Please take a few seconds to visit the following " \
                                                                 "link and submit your review:</p>" + \
                           "<a href='" + url + "'>CLICK HERE</a>"

            send_mail("Thank you for using Geeker's service", message=html_message, html_message=html_message, from_email="geeker.it.service@gmail.com", recipient_list=[ticket.email])

    elif hasattr(ticket, 'ticketrequest'):
        if ticket.ticketrequest.assigned == current_user:
            if request.method == 'POST':
                ticket.assigned = current_user
                ticket.save()
                ticket.ticketrequest.delete()
        else:
            HttpResponseRedirect('/geeker/')
    else:
        return HttpResponseRedirect('/geeker/')
    try:
        ticket_request = TicketRequest.objects.get(ticket=ticket)
    except TicketRequest.DoesNotExist:
        ticket_request = False
    context = RequestContext(request, {
        'assigned': ticket_request, 'ticket': ticket, 'freelancers': current_user.freelancers.filter(available=True)
    })
    return render(request, 'Geeker/assign.html', context)


def review(request, ticket_id):
    try:
        ticket = Ticket.objects.get(pk=ticket_id)
    except Ticket.DoesNotExist:
        raise Http404("Request does not exist")
    if ticket.reviewed or not ticket.solved:
        return HttpResponseRedirect('/geeker/')
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            ticket.review_text = request.POST['review_text']
            ticket.review_rating = request.POST['review_rating']
            ticket.reviewed = True
            ticket.save()
            return HttpResponseRedirect('/geeker/thankyou/2')
    else:
        review_form = ReviewForm()

    context = RequestContext(request, {
        'ticket': ticket, 'review_form': review_form
    })

    return render(request, 'Geeker/review.html', context)

def thankyou(request, msg_code):
    if(int(msg_code) == 1):
        message = "Thank you for submiting your request!"
    else:
        message = "Thank you for reviewing our experts and making our service better!"
    context = RequestContext(request, {
        'message': message
    })
    return render(request, 'Geeker/thankyou.html', context)
@login_required
def tryRecruit(request):
    if request.method == 'POST':
        user_id = request.POST.get('profile')
        try:
            user = User.objects.get(pk=user_id)
            current_user = request.user
            if not current_user.freelancers.filter(pk=user.pk).exists():
                current_user.freelancers.add(user)
            else:
                return HttpResponse(status=400)
        except User.DoesNotExist:
            return HttpResponse(status=400)
        return HttpResponse(status=201)

@login_required
def fire(request):
    if request.method == 'POST':
        user_id = request.POST.get('profile')
        try:
            user = User.objects.get(pk=user_id)
            current_user = request.user
            if current_user.freelancers.filter(pk=user.pk).exists():
                current_user.freelancers.remove(user)
            else:
                return HttpResponse(status=400)
        except User.DoesNotExist:
            return HttpResponse(status=400)
        return HttpResponse(status=201)

@login_required
def toggleAvailability(request):
    if request.method == 'POST':
        current_user = request.user
        if current_user.available:
            current_user.available = False
        else:
            current_user.available = True
        current_user.save()
        return HttpResponse(status=201)
    return HttpResponse(status=400)