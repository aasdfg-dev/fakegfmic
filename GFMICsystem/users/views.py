from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponse
from .models import Membership, Event, register_event, Certificate
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from datetime import datetime, date
import random
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
import base64
from django.db.models import Q
import json
 
today = datetime.today()

def home(request):
    request.session['session_user_id'] = None
    request.session['session_user_sub'] = None
    request.session['session_user_status'] = None
    request.session['session_fname'] = None
    request.session['seesion_lname'] = None
    return render(request, 'home.html')

def login(request):
    request.session['session_user_id'] = None
    request.session['session_user_sub'] = None
    request.session['session_user_status'] = None
    request.session['session_fname'] = None
    request.session['seesion_lname'] = None
    return render(request, 'login.html')

def logout(request):
    request.session['session_user_id'] = None
    request.session['session_user_sub'] = None
    request.session['session_user_status'] = None
    request.session['session_fname'] = None
    request.session['seesion_lname'] = None
    return render(request, 'login.html')

def forgot_pass(request):
    return render(request, 'forgot_password.html')

def error_404(request):
    return render(request, '404.html')

def about(request):
    return render(request, 'about.html')

def home_event(request):
    return render(request, 'home_event.html')

def membership_conference(request):
    return render(request, 'membership-conference.html')

def national_convention(request):
    return render(request, 'national-convention.html')

def webinar(request):
    return render(request, 'webinar.html')

def faqs(request):
    return render(request, 'faqs.html')

def help_desk(request):
    return render(request, 'help-desk.html')

def ecert(request):
    return render(request, 'ecert.html')

def generator(request):
    return render(request, 'generator.html')

def process_login(request):
    email = request.POST.get('useremail')
    password = request.POST.get('password')
    try:
        m = Membership.objects.get(user_email=email, user_password=password)
        request.session['session_user_id'] = m.user_id
        request.session['session_user_sub'] = m.user_sub
        request.session['session_user_status'] = m.user_status
        request.session['session_fname'] = m.user_fname
        request.session['session_lname'] = m.user_lname
        request.session['session_user_file'] = json.dumps(str(m.user_file))
        return HttpResponseRedirect('/dashboard', {'member': m})
        # return render(request, 'dashboard.html', {
        #     'member': m
        # })
    except ObjectDoesNotExist:
        return render(request, 'login.html', {
            'error_message': 'Either email or password are incorrect :'
        })

def dashboard(request):
    try:
        if request.session['session_user_id']:
            m = Membership.objects.get(user_id=request.session['session_user_id'])
            request.session['session_user_sub'] = m.user_sub
            return render(request, 'dashboard.html')
    except:
        return render(request, '404.html')
    

def upload_profile(request):
    user_id = request.POST.get('userid')
    return render(request, 'dashboard.html')

def profile(request):
    user_id = request.POST.get('user_id')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    middle_name = request.POST.get('middle_name')
    contact = request.POST.get('contact')
    address = request.POST.get('address')
    agency = request.POST.get('agency')
    college = request.POST.get('college')
    post_grad = request.POST.get('post_grad')
    try:
        m = Membership.objects.get(user_id=user_id)
        m.user_fname = first_name
        m.user_mname = middle_name
        m.user_lname = last_name
        m.user_mobile = contact
        m.user_address = address
        m.user_agency = agency
        m.user_post = post_grad
        m.user_school = college
        m.save()
        request.session['session_fname'] = m.user_fname
        request.session['seesion_lname'] = m.user_lname
        data = {'success':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def register(request):
    return render(request, 'register.html')

def register_account(request):
    email = request.POST.get('useremail')
    password = request.POST.get('password')
    password1 = request.POST.get('password1')
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    randomstr =''.join((random.choice(chars)) for x in range(5))
    user_no = 'MN-' + randomstr
    if email != None or password != None or password1 != None:
        if password == password1:
            try:
                m = Membership.objects.get(user_email=email)
                return render(request, 'register.html', {
                    'error_message': 'Duplicated email :' + email
                })
            except ObjectDoesNotExist:
                m = Membership.objects.create(user_email=email, user_password=password, user_no=user_no)
                m.save()
                return HttpResponseRedirect('/login')
        else:
            return render(request, 'register.html', {
                'error_message': 'Password does not match.' 
            })
    else:
        return render(request, 'register.html', {
            'error_message': 'Please fill up the required fields.'
        })
        

def membership(request):
    try:
        if request.session['session_user_sub'] == 'ADMIN':
            member_list = Membership.objects.filter(~Q(user_sub='ADMIN')).order_by('-user_dateupdated')
            context = {'member_list': member_list}
            return render(request, 'membership.html', context)
        else:
            member_list = Membership.objects.filter(~Q(user_sub='ASSOCIATE')).order_by('-user_dateupdated')
            context = {'member_list': member_list}
            return render(request, 'membership.html', context)
    except ObjectDoesNotExist:
        return render(request, 'membership.html')

def add_membership(request):
    m_no = request.POST.get('m_no')
    m_name = request.POST.get('m_name')
    m_mobile = request.POST.get('m_mobile')
    m_satus = request.POST.get('m_satus')
    m_sub = request.POST.get('m_sub')
    email = request.POST.get('email')
    pass1 = request.POST.get('pass')
    try:
        c = Membership.objects.get(user_email=email)
        data = {'error': True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        member = Membership(
            user_no=m_no,
            user_email=email,
            user_password=pass1,
            user_sub=m_sub,
            user_status = m_satus,
            user_fname = m_name,
            user_mobile = m_mobile
        )
        member.save()
        data = {'success': True}
        return JsonResponse(data, safe=False)

# def edit_account(request):
#     acc_id = request.POST.get('acc_id') 
#     account_sub = request.POST.get('account_sub')
#     try:
#         c = Account.objects.get(account_id=acc_id)
#         c.account_subscription = account_sub
#         c.account_dateupdated = today
#         c.save()
#         data = {'success': True}
#         return JsonResponse(data, safe=False)
#     except ObjectDoesNotExist:
#         data = {'error': True}
#         return JsonResponse(data, safe=False)

def view_membership(request):
    user_id = request.POST.get('user_id')
    print(user_id)
    try:
        a = Membership.objects.get(user_id=user_id)
        data = {
            'member_proof': str(a.user_file),
            'membership_no':a.user_no,
            'payment_amount':a.user_amount,
            'mode_of_payment':a.user_pmode,
            'm_start':a.user_validity,
            'm_end':a.user_expire,
            'm_status':a.user_status,
        }
        print(a.user_file)
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

# def delete_account(request):
#     acc_id = request.POST.get('acc_id') 
#     try:
#         c = Account.objects.get(account_id=acc_id)
#         if c.account_status == 'ACTIVE':
#             c.account_status = 'INACTIVE'
#         else:
#             c.account_status = 'ACTIVE'
#             c.account_dateupdated = today
#         c.account_dateupdated = today
#         c.save()
#         data = {'success': True}
#         return JsonResponse(data, safe=False)
#     except ObjectDoesNotExist:
#         data = {'error': True}
#         return JsonResponse(data, safe=False)
   
def payment(request):
    userid = request.POST.get('payment_id')
    img = request.FILES.get("file")
    mode_of_payment = request.POST.get('mode_of_payment')
    m_start = request.POST.get('m_start')
    if m_start:
       
        # m_start = m_start + ' ' + '00:00:00'
        mstart = datetime.strptime(m_start, "%m/%d/%Y")
        # mstart = datetime.strptime(m_start, "%d/%m/%Y").strftime('%Y-%m-%d %H:%M:%S')
    
        # m_start = datetime.strftime(m_start, "%Y-%m-%d %H:%M:%S")
    
        # m_start = datetime.strptime(m_start, "YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]")
        
        m_end = request.POST.get('m_end')
        mend = datetime.strptime(m_start, "%m/%d/%Y")
        # mend = datetime.strptime(m_start, "%d/%m/%Y").strftime('%Y-%m-%d %H:%M:%S')
        # print(m_start, m_end)
    payment_amount = request.POST.get('payment_amount')
  
    try: 
        m = Membership.objects.get(user_id=userid)
        m.user_amount = payment_amount
        m.user_pmode = mode_of_payment
        m.user_validity = mstart
        m.user_expire = mend
        m.user_file = img
        m.save()
        request.session['session_user_sub'] = m.user_sub
        return HttpResponseRedirect('dashboard')
    except ObjectDoesNotExist:
        return HttpResponseRedirect('dashboard', {
            'error_message': 'failed'
        })

def approve_membership(request):
    userid = request.POST.get('user_id')
    approver_id = request.POST.get('approver_id')
    print(approver_id)
    try: 
        m = Membership.objects.get(user_id=userid)
        m.user_sub = 'PREMIUM'
        m.user_approver = str(approver_id),

        m.save()
        data = {'success': True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error': True}
        return JsonResponse(data, safe=False)

def disapprove_membership(request):
    userid = request.POST.get('user_id')
    try: 
        m = Membership.objects.get(user_id=userid)
        m.user_pmode = None
        print(m.user_pmode)
        m.user_amount = None
        m.user_validity = None
        m.user_expire = None
        m.user_file = None
        
        m.save()
        data = {'success': True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error': True}
        return JsonResponse(data, safe=False)


def info(request):
    try:
        account_list = Account.objects.order_by('account_id')
        context = {'account_list': account_list}
        return render(request, 'info.html', context)
    except ObjectDoesNotExist:
        return render(request, 'info.html')

def events(request):
    event_list = Event.objects.order_by('-event_datecreated')
    context = {'event_list': event_list}
    return render(request, 'events.html', context)

def event(request):
    try:
        event_list = Event.objects.order_by('-event_datecreated')
        context = {'event_list': event_list}
        return render(request, 'event.html', context)
    except ObjectDoesNotExist:
        return render(request, 'event.html')

def add_event(request):
    associate_id = request.POST.get('user_id')
    event_title = request.POST.get('event_title')
    sched_time_start = request.POST.get('sched_time_start')
    sched_time_end = request.POST.get('sched_time_end')
    sched_date = request.POST.get('sched_date')
    event_amount = request.POST.get('event_amount')
    event_link = request.POST.get('event_link')
    # print(sched_date)
    event_desc = request.POST.get('event_desc')
    event_speaker = request.POST.get('event_speaker')
    event_category = request.POST.get('event_category')
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    randomstr =''.join((random.choice(chars)) for x in range(5))
    event_no = 'EN-' + randomstr
    # sched_date = datetime.strptime(sched_date, '%m-%d-%Y' )
    try:
        # print(event_title, associate_id, event_title, sched_time, sched_date, event_desc, event_speaker, event_category)
        e = Event.objects.create(
            event_no = event_no,
            event_title = event_title,
            event_associate = Membership.objects.get(user_id = associate_id),
            event_date = sched_date,
            event_time_start = str(sched_time_start), 
            event_time_end = str(sched_time_end), 
            event_amount = event_amount,
            event_link = event_link,
            event_desc = event_desc,
            event_category = event_category,
            event_speaker = event_speaker
        )
        e.save()
        data = {'success': True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error': True}
        return JsonResponse(data, safe=False)

def add_event_picture(request):
    event_id = request.POST.get('event_id')
    event_img = request.FILES.get("event_file")
    try:
        e = Event.objects.get(event_id = event_id)
        e.event_image = event_img
        e.save()
        return HttpResponseRedirect('event/')
    except ObjectDoesNotExist:
        return HttpResponseRedirect('event/', {
            'error_message': 'failed'
        })

def view_event(request):
    e_id = request.POST.get('e_id')
    try:
        e = Event.objects.get(event_id = e_id)
        data = {
            'event_id': e.event_id,
            'event_title': e.event_title,
            'event_desc': e.event_desc,
            'event_time_start': e.event_time_start,
            'event_time_end': e.event_time_end,
            'event_date': e.event_date,
            'event_speaker': e.event_speaker,
            'event_amount': e.event_amount,
            'event_link': e.event_link,
        }
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def join_event_payment_proof(request):
    userid = request.POST.get('payment_id')
    img = request.FILES.get("file")
    mode_of_payment = request.POST.get('mode_of_payment')
    m_start = request.POST.get('m_start')
    if m_start:
       
        # m_start = m_start + ' ' + '00:00:00'
        mstart = datetime.strptime(m_start, "%m/%d/%Y")
        # mstart = datetime.strptime(m_start, "%d/%m/%Y").strftime('%Y-%m-%d %H:%M:%S')
    
        # m_start = datetime.strftime(m_start, "%Y-%m-%d %H:%M:%S")
    
        # m_start = datetime.strptime(m_start, "YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]")
        
        m_end = request.POST.get('m_end')
        mend = datetime.strptime(m_start, "%m/%d/%Y")
        # mend = datetime.strptime(m_start, "%d/%m/%Y").strftime('%Y-%m-%d %H:%M:%S')
        # print(m_start, m_end)
    payment_amount = request.POST.get('payment_amount')
  
    try: 
        m = Membership.objects.get(user_id=userid)
        m.user_amount = payment_amount
        m.user_pmode = mode_of_payment
        m.user_validity = mstart
        m.user_expire = mend
        m.user_file = img
        m.save()
        request.session['session_user_sub'] = m.user_sub
        return HttpResponseRedirect('dashboard')
    except ObjectDoesNotExist:
        return HttpResponseRedirect('dashboard', {
            'error_message': 'failed'
        })

def join_event_payment(request):
    ev_id = request.POST.get('ev_id')
    m_id = request.POST.get('member_id')
    img = request.FILES.get("file")
    mode_of_payment = request.POST.get('mode_of_payment')
    payment_amount = request.POST.get('payment_amount')
    try:
        e = register_event.objects.get(reg_event_id = Event.objects.get(event_id=ev_id), reg_member_id = Membership.objects.get(user_id = m_id))
        data = {'error':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        e.reg_event_id = ev_id,
        e.reg_member_id = m_id,
        e.reg_payment_amount = payment_amount,
        e.reg_pmode = mode_of_payment,
        e.reg_proof_payment = img,
        e.save()
        return JsonResponse(data, safe=False)

def add_event_picture(request):
    event_id = request.POST.get('event_id')
    event_img = request.FILES.get("event_file")
    try:
        e = Event.objects.get(event_id = event_id)
        e.event_image = event_img
        e.save()
        return HttpResponseRedirect('event/')
    except ObjectDoesNotExist:
        return HttpResponseRedirect('event/', {
            'error_message': 'failed'
        })
        
def event_remove(request):
    event_id = request.POST.get('event_id')
    event_choice =  request.POST.get('status')
    try:
        e = Event.objects.get(event_id = event_id)
        if event_choice == 'approve':
            e.event_status = 'ON GOING'
            e.save()
        elif event_choice == 'remove':
            e.delete()
        data = {'success':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error': True}
        return JsonResponse(data, safe=False)

def event_approve(request):
    event_id = request.POST.get('event_id')
    try:
        e = Event.objects.get(event_id = event_id)
        e.event_status = 'ON GOING'
        e.save()
        data = {'success':True}
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error': True}
        return JsonResponse(data, safe=False)

    # m_start = request.POST.get('m_start')
    # m_start = m_start + ' ' + '00:00:00'
    # mstart = datetime. strptime(m_start, '%m/%d/%Y %H:%M:%S')
    # m_end = request.POST.get('m_end')
    # m_end = m_end + ' ' + '00:00:00'
    # estart = datetime. strptime(m_end, '%m/%d/%Y %H:%M:%S')
    # payment_amount = request.POST.get('payment_amount')

def OR(request):
    member_list = Membership.objects.order_by('-user_dateupdated')
    context = {'member_list': member_list}
    return render(request, 'or.html', context)

def member_gen_receipt(request):
    user_id = request.POST.get('member_id')
    try:
        e = Membership.objects.get(user_id = user_id)
        data = {
            'user_id': e.user_id,
            'user_no': e.user_no,
            'user_sub': e.user_sub,
            'user_amount': e.user_amount,
            'user_validity': e.user_validity,
            'user_expire': e.user_expire,
            'user_lname': e.user_lname,
            'user_fname': e.user_fname,
            'user_mname': e.user_mname,
            'user_sname': e.user_sname,
            'user_approver': e.user_approver,
        }
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {'error':True}
        return JsonResponse(data, safe=False)

def add_ecert(request):
    cert_no = request.POST.get('cert_no')
    cert_status = request.POST.get('cert_status')
    cert_member_id = request.POST.get('cert_member_id')
    cert_event_id = request.POST.get('cert_event_id')
    try:
        e = Certificate.objects.create(
            event_no = cert_no,
            event_title = cert_status,
            event_member = Membership.objects.get(user_id = cert_member_id),
            event_event = Event.objects.get(event_id = cert_event_id)
        )
        e.save()
        data = {'success': True}
        return JsonResponse(data, safe=False)

    except ObjectDoesNotExist:
        data = {'error': True}
        return JsonResponse(data, safe=False)