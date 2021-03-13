from django.db.models import Q
from django.shortcuts import render, redirect, reverse
from . import forms, models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from django.contrib import messages
from django.utils import timezone
from django.db.models import Avg, F
from django.db.models import DateTimeField
from ReferalSystem.utils import render_to_pdf
from datetime import datetime
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
import datetime
from datetime import timedelta


def home_view(request):
    # paginate_by = 10
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'Referal/index.html')


def regionaladminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('regionaladminlogin')


def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


def liaizon_signup_view(request):
    userForm = forms.LiaizonUserForm()
    liaizonForm = forms.LiaizonForm()
    mydict = {'userForm': userForm, 'liaizonForm': liaizonForm}
    if request.method == 'POST':
        userForm = forms.LiaizonUserForm(request.POST)
        liaizonForm = forms.LiaizonForm(request.POST, request.FILES)
        if userForm.is_valid() and liaizonForm.is_valid():
            user = userForm.save()
            user.set_password(user.password) 
            user.save()
             liaizon = liaizonForm.save(commit=False)
            liaizon.user = user
            liaizon.assignedHospitalID = request.POST.get('assignedHospitalID')
            liaizon.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('customerlogin')
    return render(request, 'vehicle/customersignup.html', context=mydict)

# for checking user , m or admin


def is_liaizon(user):
    return user.groups.filter(name='LIAIZON').exists()


def is_regionaladmin(user):
    return user.groups.filter(name='REGIONALADMIN').exists()


def is_CEO(user):
    return user.groups.filter(name='CEO').exists()


def afterlogin_view(request):
    if is_liaizon(request.user):
        return redirect('liaizon-dashboard')
    elif is_regionaladmin(request.user):
        return redirect('regionaladmin-dashboard')
    elif is_CEO(request.user):
        return redirect('ceo-dashboard')
    else:
        return redirect('admin-dashboard')


@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    # paginated_by = 10

    enquiry = models.referalrequest.objects.all().order_by('-id')
    paginator = Paginator(enquiry, 10)
    page = request.GET.get('page')
    enquiry = paginator.get_page(page)

    liaizons = []
    for enq in enquiry:
        liaizon = models.Liaizon.objects.get(id=enq.liaizon_id)
        liaizons.append(liaizon)
    dict = {
        'total_customer': models.Liaizon.objects.all().count(),
        'total_facility': models.Facility.objects.all().count(),
        'total_request': models.referalrequest.objects.all().count(),
        'enquiry': enquiry,
        'data': zip(liaizons, enquiry),

        'nam': request.user.first_name + " " + request.user.last_name

    }

    return render(request, 'Referal/admin_dashboard.html', context=dict)


@login_required(login_url='adminlogin')
def admin_add_Liaizon_view(request):
    liaizonForm = forms.LiaizonUserForm()
    liaizonForm = forms.LiaizonForm()
    mydict = {'userForm': userForm, 'customerForm': customerForm}
    if request.method == 'POST':
        userForm = forms.CustomerUserForm(request.POST)
        liaizonForm = forms.LiaizonForm(request.POST, request.FILES)
        if userForm.is_valid() and LiaizonForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            laiazion = liaizonForm.save(commit=False)
            liaizon.user = user
            laiazion.save()
            my_customer_group = Group.objects.get_or_create(name='laizion')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('/admin-view-customer')
    return render(request, 'vehicle/admin_add_customer.html', context=mydict)


@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def liaizon_approve_request_view(request):
    # customer = models.Customer.objects.get(user_id=request.user.id)
    liaizon = models.Liaizon.objects.get(user_id=request.user.id)
    facility = models.Facility.objects.get(id=liaizon.facility.id)

    enquiry = models.referalrequest.objects.filter(
        referal_to=facility, status__in=('Pending', 'Approved')).order_by('-id')

    hos = facility.facility_name
    nam = liaizon.get_name
    # enquiry =  models.referalrequest.objects.all().filter(status='Pending')
    return render(request, 'Referal/customer_approve_request.html', {'enquiry': enquiry, "hos": hos, "nam": nam})


@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def liaizon_view_all_request(request):
    # customer = models.Customer.objects.get(user_id=request.user.id)
    liaizon = models.Liaizon.objects.get(user_id=request.user.id)
    facility = models.Facility.objects.get(id=liaizon.facility.id)
    liaizons = models.Liaizon.objects.filter(facility=facility.id)

    enquiry = models.referalrequest.objects.filter(referal_to=facility, status__in=(
        'Pending', 'Approved', 'Feedback', 'Re-direct')).order_by('-id')
    # enquiry = models.referalrequest.objects.all().exclude(status='Pending',customer__in=customers).order_by('-id')

    # enquiry = models.referalrequest.objects.filter(referal_to=facility)
    paginator = Paginator(enquiry, 3)
    page = request.GET.get('page')
    enquiry = paginator.get_page(page)
    nam = liaizon.get_name
    hos = facility.facility_name
    # enquiry =  models.referalrequest.objects.all().filter(status='Pending')
    return render(request, 'Referal/liaizon_view_approve_all_request.html', {'enquiry': enquiry, "nam": nam, "hos": hos})


@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def liaizon_view_all_feedback(request):
    # customer = models.Customer.objects.get(user_id=request.user.id)
    liaizon = models.Liaizon.objects.get(user_id=request.user.id)
    facility = models.Facility.objects.get(id=liaizon.facility.id)
    liaizons = models.Liaizon.objects.filter(facility=facility.id)

    enquiry = models.referalrequest.objects.filter(
        status='Feedback', liaizon__in=liaizons).order_by('-id')

    # enquiry = models.referalrequest.objects.filter(referal_to=facility)
    paginator = Paginator(enquiry, 3)
    page = request.GET.get('page')
    enquiry = paginator.get_page(page)
    nam = liaizon.get_name
    hos = facility.facility_name
    # enquiry =  models.referalrequest.objects.all().filter(status='Pending')
    return render(request, 'Referal/liaizon_view_approve_all_feedback.html', {'enquiry': enquiry, "nam": nam, "hos": hos})


@login_required(login_url='adminlogin')
def update_approve_status(request, pk):
    liaizon = models.Liaizon.objects.get(user_id=request.user.id)
    referal_request = models.referalrequest.objects.get(id=pk)
    referal_request.status = 'Approved'
    referal_request.approved_date = timezone.now()
    referal_request.approved_by = liaizon
    referal_request.save()
    return HttpResponseRedirect(reverse('liaizon_approve_request'))


def liaizon_feedback_referal_view(request):
    liaizon = models.Liaizon.objects.get(user_id=request.user.id)
    facility = models.Facility.objects.get(id=liaizon.facility.id)

    enquiry = models.referalrequest.objects.filter(
        referal_to=facility, status='Approved')

    return render(request, 'Referal/liaizon__fedbackt.html', {'enquiry': enquiry})


@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def Capprove_request_view(request, pk):
    adminenquirys = forms.liaizonApproveRequestForm()
    if request.method == 'POST':
        adminenquirys = forms.liaizonApproveRequestForm(request.POST)
        if adminenquirys.is_valid():
            enquiry_x = models.referalrequest.objects.get(id=pk)
            enquiry_x.status = adminenquirys['status']
            enquiry_x.status = 'Approved'
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect(reverse('liaizon_approve_request'))
    return render(request, 'Referal/customer_approve_request_details.html', {'adminenquirys': adminenquirys})


@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def Liaizon_request_view(request, pk):
    liaizon = models.Liaizon.objects.get(user_id=request.user.id)
    facility = models.Facility.objects.get(id=liaizon.facility.id)
    nam = liaizon.get_name
    hos = facility.facility_name
    adminenquirys = forms.LiaizonApproveRequestForm()
    if request.method == 'POST':
        adminenquirys = forms.LiaizonApproveRequestForm(request.POST)
        if adminenquirys.is_valid():
            enquiry_x = models.referalrequest.objects.get(id=pk)
            # enquiry_x.mechanic=adminenquiry.cleaned_data['mechanic']
            enquiry_x.patient_diagnosis = adminenquirys.cleaned_data['patient_diagnosis']
            enquiry_x.comments_of_referal = adminenquirys.cleaned_data['comments_of_referal']
            enquiry_x.with_respect_to_medical_care = adminenquirys.cleaned_data[
                'with_respect_to_medical_care']
            enquiry_x.with_respect_patient_transportation = adminenquirys.cleaned_data[
                'with_respect_patient_transportation']
            enquiry_x.feedback_status = 'YES'
            enquiry_x.status = 'Feedback'
            enquiry_x.feedback_date = timezone.now()
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/liaizon_approve_request')
    return render(request, 'vehicle/liaizon_approve_request_details.html', {'adminenquirys': adminenquirys, 'nam': nam, 'hos': hos})


@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def patient_detail_view(request, pk):
    pad = models.referalrequest.objects.get(id=pk)
    liaizon = models.Liaizon.objects.get(user_id=request.user.id)
    facility = models.Facility.objects.get(id=customer.facility.id)
    nam = liaizon.get_name
    hos = facility.facility_name

    context = {
        'pad': pad,
        'nam': nam,
        'hos': hos,
    }
    return render(request, 'Referal/patient_detail.html', context)


@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def Liaizon_dashboard_view(request):

    liaizon = models.Liaizon.objects.get(user_id=request.user.id)
    facility = models.Facility.objects.get(id=liaizon.facility.id)

    liaizons = models.Liaizon.objects.filter(facility=facility.id)

    enquiries = models.referalrequest.objects.all().filter(
        liaizon__in=liaizons).order_by('-id')
    # enquiries = Post.objects.all()
    paginator = Paginator(enquiries, 5)
    page = request.GET.get('page')
    enquiries = paginator.get_page(page)

    liaizon = models.Liaizon.objects.get(user_id=request.user.id)
    facility = models.Facility.objects.get(id=liaizon.facility.id)

    liaizons = models.Liaizon.objects.filter(facility=facility.id)

    refere_out = models.referalrequest.objects.all().filter(
        liaizon__in=liaizons).count()
    refere_out_feedback = models.referalrequest.objects.all().filter(
        liaizon__in=liaizons, status='Feedback').count()
    refer_in = models.referalrequest.objects.all().filter(
        referal_to=facility.id, status='Pending').count()

    dict = {

        'refer_in': refer_in,
        'hos': facility.facility_name,
        'refere_out_feedback': refere_out_feedback,
        'refere_out': refere_out,
        'nam': liaizon.get_name,
        'enquiries': enquiries,

    }
    return render(request, 'Referal/liaizon_dashboard.html', context=dict)


@login_required(login_url='ceologin')
@user_passes_test(is_CEO)
def Ceo_dashboard_view(request):

    liaizon = models.Liaizon.objects.get(user_id=request.user.id)
    facility = models.Facility.objects.get(id=liaizon.facility.id)

    liaizons = models.Liaizon.objects.filter(facility=facility.id)

    enquiries = models.referalrequest.objects.all().filter(
        liaizon__in=liaizons).order_by('-id')
    # enquiries = Post.objects.all()
    paginator = Paginator(enquiries, 5)
    page = request.GET.get('page')
    enquiries = paginator.get_page(page)

    liaizon = models.Liaizon.objects.get(user_id=request.user.id)
    facility = models.Facility.objects.get(id=liaizon.facility.id)

    liaizons = models.Liaizon.objects.filter(facility=facility.id)

    # refere_out=models.referalrequest.objects.all().filter(customer__in=customers).filter(Q(status="Pending") | Q(status="Approved")).count()
    refere_out = models.referalrequest.objects.all().filter(
        liaizon__in=liaizons).count()
    refere_out_feedback = models.referalrequest.objects.all().filter(
        liaizon__in=liaizons, status='Feedback').count()
    refer_in = models.referalrequest.objects.all().filter(
        referal_to=facility.id, status='Pending').count()

    dict = {

        'refer_in': refer_in,
        'hos': facility.facility_name,
        'refere_out_feedback': refere_out_feedback,
        'refere_out': refere_out,
        'nam': customer.get_name,
        'enquiries': enquiries,


    }
    return render(request, 'Referal/ceo_dashboard.html', context=dict)


@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def Facility_dashboard(request):

    liaizon = models.Facility_User.objects.get(user_id=request.user.id)
    facility = models.Facility.objects.get(id=liaizon.facility.id)
    startdate = datetime.date.today()
    enddate = startdate + timedelta(days=6)
    apps = models.Appoint.objects.filter(
        facility=facility.id, date__range=[startdate, enddate]).order_by('app_date')
    ward = models.Ward.objects.filter(facility_id=facility)
    rooms = models.Room.objects.filter(facility=facility)
    if rooms.count() != 0:
        no_beds = models.Room.objects.filter(facility=facility).aggregate(
            Sum('no_beds')).get('no_beds__sum')
        occ_beds = models.Room.objects.filter(facility=facility).aggregate(
            Sum('occ_beds')).get('occ_beds__sum')
        free_beds = no_beds - occ_beds
        male_beds = models.Room.objects.filter(
            facility=facility, room_type='Male').aggregate(Sum('no_beds')).get('no_beds__sum')
        male_occ = models.Room.objects.filter(
            facility=facility, room_type='Male').aggregate(Sum('occ_beds')).get('occ_beds__sum')
        if male_beds != None:
            male_free = male_beds - male_occ
        else:
            male_free = 0
        female_beds = models.Room.objects.filter(
            facility=facility, room_type='Female').aggregate(Sum('no_beds')).get('no_beds__sum')
        female_occ = models.Room.objects.filter(
            facility=facility, room_type='Female').aggregate(Sum('occ_beds')).get('occ_beds__sum')
        if female_beds != None:
            female_free = female_beds - female_occ
        else:
            female_free = 0
    else:
        no_beds = 0
        occ_beds = 0
        free_beds = 0
        male_free = 0
        female_free = 0

    context = {
        'hos': facility.facility_name,
        'nam': liaizon.get_name,
        'no_beds': no_beds,
        'free_beds': free_beds,
        'male_free': male_free,
        'female_free': female_free,
        'apps': apps
    }
    return render(request, 'Referal/facility_dashboard.html', context)


@login_required(login_url='ceologin')
@user_passes_test(is_liaizon)
def ceo_view_all_request(request):
    # customer = models.Customer.objects.get(user_id=request.user.id)
    liaizon = models.Liaizon.objects.get(user_id=request.user.id)
    facility = models.Facility.objects.get(id=liaizon.facility.id)
    liaizons = models.Liaizon.objects.filter(facility=facility.id)

    enquiry = models.referalrequest.objects.filter(referal_to=facility, status__in=(
        'Pending', 'Approved', 'Feedback', 'Re-direct')).order_by('-id')
    # enquiry = models.referalrequest.objects.all().exclude(status='Pending',customer__in=customers).order_by('-id')

    # enquiry = models.referalrequest.objects.filter(referal_to=facility)
    paginator = Paginator(enquiry, 3)
    page = request.GET.get('page')
    enquiry = paginator.get_page(page)
    nam = customer.get_name
    hos = facility.facility_name
    # enquiry =  models.referalrequest.objects.all().filter(status='Pending')
    return render(request, 'Referal/ceo_view_approve_all_request.html', {'enquiry': enquiry, "nam": nam, "hos": hos})


@login_required(login_url='ceologin')
@user_passes_test(is_liaizon)
def ceo_view_all_feedback(request):
    # customer = models.Customer.objects.get(user_id=request.user.id)
    liaizon = models.Liaizon.objects.get(user_id=request.user.id)
    facility = models.Facility.objects.get(id=liaizon.facility.id)
    liaizons = models.Liaizon.objects.filter(facility=facility.id)

    enquiry = models.referalrequest.objects.filter(
        status='Feedback', liaizon__in=liaizons).order_by('-id')

    # enquiry = models.referalrequest.objects.filter(referal_to=facility)
    paginator = Paginator(enquiry, 3)
    page = request.GET.get('page')
    enquiry = paginator.get_page(page)
    nam = customer.get_name
    hos = facility.facility_name
    # enquiry =  models.referalrequest.objects.all().filter(status='Pending')
    return render(request, 'Referal/ceo_view_approve_all_feedback.html', {'enquiry': enquiry, "nam": nam, "hos": hos})


def patient_detail2_view(request, pk):
    pad = models.referalrequest.objects.get(id=pk)
    liaizon = models.Liaizon.objects.get(user_id=request.user.id)
    facility = models.Facility.objects.get(id=liaizon.facility.id)
    nam = liaizon.get_name
    hos = facility.facility_name

    context = {
        'pad': pad,
        'nam': nam,
        'hos': hos,
    }
    return render(request, 'Referal/patient_detail2.html', context)

# @login_required(login_url='liaizonlogin')
# @user_passes_test(is_liaizon)
# def liaizon_request_view(request):
#     customer=models.Customer.objects.get(user_id=request.user.id)
#     return render(request,'vehicle/customer_request.html',{'customer':customer})


# @login_required(login_url='liaizonlogin')
# @user_passes_test(is_liaizon)
# def liaizon_view_request_view(request):

#     liaizon = models.Liaizon.objects.get(user_id=request.user.id)
#     facility = models.Facility.objects.get(id=customer.facility.id)

#     liaizons = models.Liaizon.objects.filter(facility=facility.id)

#     enquiries=models.referalrequest.objects.all().filter(liaizon__in=liaizons)
#     return render(request,'Refera/customer_view_request.html',{'customer':customer,'enquiries':enquiries})

@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def liaizon_profile_view(request):
    liaizon = models.Liaizon.objects.get(user_id=request.user.id)
    facility = models.Facility.objects.get(id=liaizon.facility.id)
    nam = liaizon.get_name
    hos = facility.facility_name
    return render(request, 'Referal/liaizon_profile.html', {'customer': customer, 'hos': hos, 'nam': nam})


@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def edit_liaizon_profile_view(request):
    liaizon = models.Liaizon.objects.get(user_id=request.user.id)
    facility = models.Facility.objects.get(id=liaizon.facility.id)
    hos = facility.facility_name
    nam = liaizon.get_name
    user = models.User.objects.get(id=liaizon.user_id)
    # userForm=forms.CustomerUserForm(instance=user)
    # customerForm=forms.CustomerForm(instance=customer)

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your Password Was Succefuy Edited")
            return redirect("edit-liaizon-profile")
        else:
            messages.error(request, "please Correct the eroor")

    else:
        form = PasswordChangeForm(request.user)
    mydict = {'customer': customer, 'hos': hos, 'nam': nam, 'form': form}
    return render(request, 'Referal/edit_liaizon_profile.html', context=mydict)
# Reg


@login_required(login_url='regionaladminlogin')
@user_passes_test(is_regionaladmin)
def regional_admin_dashboard_view(request):
    print(request.user.id)
    regionaladmin = models.RegionalAdmin.objects.get(user=request.user.id)
    reg_facility = models.Facility.objects.all().filter(region=regionaladmin.region)
    no_of_facility_count = models.Facility.objects.all().filter(
        region=regionaladmin.region).count()
    no_of_users_count = models.Liaizon.objects.all().filter(
        facility__in=reg_facility).count()
    dict = {
        'regionaladmin': regionaladmin,
        'no_of_facility_count': no_of_facility_count,
        'no_of_users_count': no_of_users_count,
        # 'nam':request.user
        'fac': regionaladmin.region,
        'nam': regionaladmin.get_name,
        'segment': 'regionaladmin',
    }
    return render(request, 'Referal/regionaladmin_dash.html', dict)


@login_required(login_url='regionaladminlogin')
@user_passes_test(is_regionaladmin)
def regionaladmin_profile_view(request):
    # mechanic=models.RegionalAdmin.objects.get(user_id=request.user.id)
    regionaladmin = models.RegionalAdmin.objects.get(user=request.user.id)
    fac = regionaladmin.region
    return render(request, 'Referal/regionaladmin_profile.html', {'regionaladmin': regionaladmin, "fac": fac})


@login_required(login_url='regionaladminlogin')
@user_passes_test(is_regionaladmin)
def edit_regionaladmin_profile_view(request):
    regionaladmin = models.RegionalAdmin.objects.get(user_id=request.user.id)
    user = models.User.objects.get(id=regionaladmin.user_id)

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your Password Was Succefuy Edited")
            return redirect("edit_mechanic_profile.html")
        else:
            messages.error(request, "please Correct the eroor")

    else:
        form = PasswordChangeForm(request.user)
        mydict = {
            'regionaladmin': regionaladmin,
            'fac': regionaladmin.region,
            'nam': regionaladmin.get_name,
            'form': form
        }
    return render(request, 'Referal/edit_regionaladmin_profile.html', context=mydict)


@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def refere_request_view(request):

    liaizon = models.Liaizon.objects.get(user_id=request.user.id)
    facility = models.Facility.objects.get(id=liaizon.facility.id)
    reference_to = models.ReferTo.objects.filter(facility__id=facility.id)
    refer_in = models.referalrequest.objects.all().filter(
        referal_to=facility.id, status='Pending').count()
    facility_ref_list = []

    for reference in reference_to:
        facility_ref_list.append(reference.refer_to)

    facilitys = models.Facility.objects.filter(id__in=facility_ref_list)
    regions = ['ADDIS ABBABA', 'OROMIA', 'AMHARA', 'TIGRAY', 'SOUTH',
               'GAMBELLA', 'BENSHANGUL', 'HARRARI', 'DIREDAWA', 'SIDAMA', 'SOUTH WEST']
    pd = ['THE SAME TO REFERING FACILITY', 'NOT THE SAME TO REFERING FACILITY']
    services = models.Service.objects.all()
    dict = {
        "facilitys": facilitys, "regions": regions,
        "services": services,
        "facility": facility,
        "liaizon": liaizon,
        "hos": facility.facility_name,
        "nam": liaizon.get_name,
        "refer_in": refer_in
    }
    return render(request, "Referal/refere_request.html", dict)


def refere_request_save_view(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        type_of_referal = request.POST.get("type_of_referal")
        name_of_patient = request.POST.get("name_of_patient")
        paient_age = request.POST.get("paient_age")
        gender = request.POST.get("gender")
        patient_region = request.POST.get("patient_region")
        patient_subcity = request.POST.get("patient_subcity")
        patient_woreda = request.POST.get("patient_woreda")
        patient_phone = request.POST.get("patient_phone")
        chief_compliants = request.POST.get("chief_compliants")
        diagnosis = request.POST.get("diagnosis")

        reason_for_referal = request.POST.get("reason_for_referal")
        refering_dr = request.POST.get("refering_dr")
        ambulance_driver_name = request.POST.get("ambulance_driver_name")
        ambulance_driver_phone = request.POST.get("ambulance_driver_phone")
        ahp_name = request.POST.get("ahp_name")
        ahp_phone = request.POST.get("ahp_name")
        refered_date = request.POST.get("refered_date")
        # patient_diagnosis = request.POST.get("patient_diagnosis")
        # comments_of_referal = request.POST.get("comments_of_referal")
        # with_respect_to_medical_care = request.POST.get("with_respect_to_medical_care")
        # with_respect_patient_transportation = request.POST.get("with_respect_patient_transportation")
        # status = request.POST.get("status")
        # service =request.POST.get("required_service")
        # required_service = models.Service.objects.get(id=required_service)

        facility = request.POST.get("referal_to")
        referal_to = models.Facility.objects.get(id=facility)
        liaizon = models.Liaizon.objects.get(user=request.user.id)

        required_srv = request.POST.get("required_service")
        required_service = models.Service.objects.get(id=required_srv)

        try:
            refer = models.referalrequest(
                type_of_referal=type_of_referal,
                name_of_patient=name_of_patient,
                paient_age=paient_age,
                gender=gender,
                patient_region=patient_region,
                patient_subcity=patient_subcity,
                patient_woreda=patient_woreda,
                patient_phone=patient_phone,
                chief_compliants=chief_compliants,
                diagnosis=diagnosis,
                required_service=required_service,
                reason_for_referal=reason_for_referal,
                refering_dr=refering_dr,
                ambulance_driver_name=ambulance_driver_name,
                ambulance_driver_phone=ambulance_driver_phone,
                ahp_name=ahp_name,
                ahp_phone=ahp_phone,
                #    refered_date=refered_date,
                #    patient_diagnosis=patient_diagnosis,
                #    comments_of_referal=comments_of_referal,
                #    with_respect_to_medical_care=with_respect_to_medical_care,
                #    with_respect_patient_transportation=with_respect_patient_transportation,
                # status="Pending",
                referal_to=referal_to,
                liaizon=liaizon,
            )
            refer.save()
            messages.success(request, "Successfully Added Reference")
            return HttpResponseRedirect(reverse("refere-request"))
        except:
            messages.error(request, "Failed to Add Reference")
            return HttpResponseRedirect(reverse("refere-request"))


@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def refere_in(request):
    liaizon = models.Liaizon.objects.get(user_id=request.user.id)
    facility = models.Facility.objects.get(id=liaizon.facility.id)

    refere_reqs = models.referalrequest.objects.filter(referal_to=facility)

    return render(request, "Referal/refere_in.html", {"refere_reqs": refere_reqs})


@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def edit_refer_request(request, ref_req_id):
    pass


@login_required(login_url='regionaladminlogin')
@user_passes_test(is_regionaladmin)
def manage_facility(request):
    regionaladmin = models.RegionalAdmin.objects.get(user=request.user.id)
    nam = request.user.first_name + " " + request.user.last_name
    facilitys = models.Facility.objects.all().filter(region=regionaladmin.region)
    paginator = Paginator(facilitys, 10)
    page = request.GET.get('page')
    facilitys = paginator.get_page(page)
    # customer = models.Customer.objects.get(user=request.user.id)

    return render(request, "Referal/manage_facility_template.html", {"facilitys": facilitys, "nam": nam, 'fac': regionaladmin.region})


@login_required(login_url='regionaladminlogin')
@user_passes_test(is_regionaladmin)
def edit_facility(request, facility_id):
    facility = models.Facility.objects.get(id=facility_id)
    reference_to = models.ReferTo.objects.filter(facility__id=facility.id)
    facility_ref_list = []

    for reference in reference_to:
        facility_ref_list.append(reference.refer_to)

    facilitys_can = models.Facility.objects.filter(id__in=facility_ref_list)

    regionaladmin = models.RegionalAdmin.objects.get(user=request.user.id)
    # facilitys=models.Facility.objects.all().filter(region=regionaladmin.region).exclude(id=facility_id)
    facilitys = models.Facility.objects.all().exclude(id=facility_id)
    # facilitys =models.Facility.objects.all()

    return render(request, "Referal/edit_facility_template.html", {"facility": facility, "facilitys": facilitys, "facilitys_can": facilitys_can})


@login_required(login_url='regionaladminlogin')
@user_passes_test(is_regionaladmin)
def delete_facility(request, pk):
    delfac = models.Facility.objects.get(id=pk)
    delfac.delete()
    return render(request, "Referal/delete_facility_template.html", {'delfac': delfac})


@login_required(login_url='regionaladminlogin')
@user_passes_test(is_regionaladmin)
def edit_facility_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        facility_id = request.POST.get("facility_id")
        facility_ob = models.Facility.objects.get(id=facility_id)
        facility_ref = request.POST.get("facility")
        try:
            reference_to = models.ReferTo(
                facility=facility_ob, refer_to=facility_ref)
            reference_to.save()

            messages.success(request, "Successfully  Edited Facility")
            return HttpResponseRedirect(reverse("edit_facility", kwargs={"facility_id": facility_id}))
        except:
            messages.error(request, "Failed to Edit Facility")
            return HttpResponseRedirect(reverse("edit_facility", kwargs={"facility_id": facility_id}))


def manage_facilities(request):
    regionaladmin = models.RegionalAdmin.objects.get(user=request.user.id)
    reg_facility = models.Facility.objects.all().filter(region=regionaladmin.region)
    return render(request, 'Referal/manage_facilities.html', {"facilities": reg_facility, 'fac': regionaladmin.region, 'segment': 'manage-facilities'})


@login_required(login_url='regionaladminlogin')
@user_passes_test(is_regionaladmin)
def add_facility(request):
    regionaladmin = models.RegionalAdmin.objects.get(user=request.user.id)
    nam = request.user.first_name + " " + request.user.last_name
    facility_type = {'Specialized', 'General', 'Primary', 'Health Center'}
    return render(request, "Referal/add_facility.html", {'fac': regionaladmin.region, "nam": nam, 'fa_ty': facility_type})


@login_required(login_url='regionaladminlogin')
@user_passes_test(is_regionaladmin)
def add_facility_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        facility_type = request.POST.get("facility_type")
        facility_name = request.POST.get("facility_name")
        regionaladmin = models.RegionalAdmin.objects.get(user=request.user.id)
        region = regionaladmin.region
        subcity = request.POST.get("subcity")
        woreda = request.POST.get("woreda")
        try:
            facility = models.Facility(
                facility_type=facility_type, facility_name=facility_name,
                region=region, subcity=subcity, woreda=woreda)
            facility.save()

            messages.success(request, "Successfully  Added Facility")
            return HttpResponseRedirect(reverse("manage_facilities"))
        except:
            messages.error(request, "Failed to Add Facility")
            return HttpResponseRedirect(reverse("add_facility"))


@login_required(login_url='regionaladminlogin')
@user_passes_test(is_regionaladmin)
def edit_fac(request, pk):
    facs = models.Facility.objects.get(id=pk)
    regionaladmin = models.RegionalAdmin.objects.get(user=request.user.id)
    nam = request.user.first_name + " " + request.user.last_name
    facility_type = {'Specialized', 'General', 'Primary', 'Health Center'}
    return render(request, "Referal/edit_facility.html", {'fac': regionaladmin.region, "nam": nam, 'fa_ty': facility_type, 'facs': facs})


@login_required(login_url='regionaladminlogin')
@user_passes_test(is_regionaladmin)
def edit_fac_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        pk = request.POST.get("id")
        facility_type = request.POST.get("facility_type")
        facility_name = request.POST.get("facility_name")
        subcity = request.POST.get("subcity")
        woreda = request.POST.get("woreda")
        try:
            fa = models.Facility.objects.get(id=pk)
            fa.facility_type = facility_type
            fa.facility_name = facility_name
            fa.subcity = subcity
            fa.woreda = woreda
            fa.save()
            messages.success(request, "Successfully  Added Facility")
            return HttpResponseRedirect(reverse("manage_facilities"))
        except:
            messages.error(request, "Failed to Add Facility")
            return HttpResponseRedirect(reverse("add_facility"))


@login_required(login_url='regionaladminlogin')
@user_passes_test(is_regionaladmin)
def manage_facility_user(request, pk):
    facility = models.Facility.objects.get(id=pk)
    fa_users = models.Facility_User.objects.all().filter(facility=facility)
    regionaladmin = models.RegionalAdmin.objects.get(user=request.user.id)
    return render(request, "Referal/manage_facility_users.html", {'fac': regionaladmin.region, "facility": facility, "fa_users": fa_users})


@login_required(login_url='regionaladminlogin')
@user_passes_test(is_regionaladmin)
def manage_facility_user_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        facility_id = request.POST.get("facility")
        mobile = request.POST.get("mobile")
        facility = models.Facility.objects.get(id=facility_id)
        try:
            user = User(
                first_name=first_name, last_name=last_name,
                username=username)
            user.set_password(password)
            user.save()
            liaizon = models.Facility_User(
                user=user, mobile=mobile, facility=facility)
            liaizon.save()
            my_customer_group = Group.objects.get_or_create(name='LIAIZON')
            my_customer_group[0].user_set.add(user)

            messages.success(request, "Successfully Added Facility User")
            return HttpResponseRedirect(reverse("manage_facility_user", kwargs={"facility": facility_id}))
        except:
            messages.error(request, "Failed to Add Facsility user")
            return HttpResponseRedirect(reverse("manage_facilities"))


def regionaladmin_add_Liaizonusers_view(request):
    regionaladmin = models.RegionalAdmin.objects.get(user=request.user.id)
    facilitys = models.Facility.objects.filter(region=regionaladmin.region)
    nam = request.user.first_name + " " + request.user.last_name
    return render(request, 'Referal/admin_add_liaizon.html', {"facilitys": facilitys, "nam": nam, 'fac': regionaladmin.region})


def regional_admin_view_users(request):

    # customer=models.Customer.objects.get(user_id=request.user.id)
    regionaladmin = models.RegionalAdmin.objects.get(user=request.user.id)
    reg_facility = models.Facility.objects.all().filter(region=regionaladmin.region)
    regionuser = models.Liaizon.objects.all().filter(facility__in=reg_facility)
    nam = request.user.first_name + " " + request.user.last_name
    return render(request, 'Referal/regionaladmin_view_liaizon_users.html', {"nam": nam, 'fac': regionaladmin.region, 'regionuser': regionuser})


@login_required(login_url='regionaladminlogin')
@user_passes_test(is_regionaladmin)
def regionaladmin_add_Liaizonusers_view_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        mobile = request.POST.get("mobile")
        address = request.POST.get("address")
        facility_id = request.POST.get("facility")
        facility = models.Facility.objects.get(id=facility_id)
        # profile_pic = request.POST.get("profile_pic")

        try:
            user = User(
                first_name=first_name, last_name=last_name,
                username=username)
            user.set_password(password)
            user.save()
            liaizon = models.Liaizon(user=user, mobile=mobile,
                                     address=address, facility=facility)
            liaizon.save()
            my_customer_group = Group.objects.get_or_create(name='LIAIZON')
            my_customer_group[0].user_set.add(user)

            messages.success(request, "Successfully  Added User")
            return HttpResponseRedirect(reverse("regionaladmin-add-Liaizonusers"))
        except:
            messages.error(request, "Failed to Add User")
            return HttpResponseRedirect(reverse("regionaladmin-add-Liaizonusers"))


@login_required(login_url='regionaladminlogin')
@user_passes_test(is_regionaladmin)
def regionaladmin_add_ceo_view(request):
    regionaladmin = models.RegionalAdmin.objects.get(user=request.user.id)
    facilitys = models.Facility.objects.filter(region=regionaladmin.region)
    nam = request.user.first_name + " " + request.user.last_name
    return render(request, 'Referal/admin_add_ceo.html', {"facilitys": facilitys, "nam": nam, 'fac': regionaladmin.region})


@login_required(login_url='regionaladminlogin')
@user_passes_test(is_regionaladmin)
def regionaladmin_add_ceo_view_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        mobile = request.POST.get("mobile")
        address = request.POST.get("address")
        facility_id = request.POST.get("facility")
        facility = models.Facility.objects.get(id=facility_id)
        # profile_pic = request.POST.get("profile_pic")

        try:
            user = User(first_name=first_name,
                        last_name=last_name, username=username)
            user.set_password(password)
            user.save()
            liaizon = models.Liaizon(user=user, mobile=mobile,
                                     address=address, facility=facility)
            liaizon.save()
            my_customer_group = Group.objects.get_or_create(name='CEO')
            my_customer_group[0].user_set.add(user)

            messages.success(request, "Successfully  Added User")
            return HttpResponseRedirect(reverse("regionaladmin-add-ceousers"))
        except:
            messages.error(request, "Failed to Add User")
            return HttpResponseRedirect(reverse("regionaladmin-add-ceousers"))


@login_required(login_url='adminlogin')
def add_regional_admin_admin(request):
    nam = request.user.first_name + " " + request.user.last_name
    regions = ['ADDISS ABABA', 'OROMIA', 'AMHARA', 'TIGRAY', 'SOUTH',
               'GAMBELLA', 'BENSHANGUL', 'HARRARI', 'DIREDAWA', 'SIDAMA', 'SOUTH WEST']
    return render(request, 'Referal/add_regional_admin.html', {"regions": regions, "nam": nam, 'segment': 'view_regional_add'})


@login_required(login_url='adminlogin')
def add_regional_admin_admin_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        region = request.POST.get("region")

        try:
            user = User(first_name=first_name,
                        last_name=last_name, username=username)
            user.set_password(password)
            user.save()
            regionaladmin = models.RegionalAdmin(user=user, region=region)
            regionaladmin.save()
            my_customer_group = Group.objects.get_or_create(
                name='REGIONALADMIN')
            my_customer_group[0].user_set.add(user)

            messages.success(
                request, "Successfully   Added   Regional   Admin")
            return HttpResponseRedirect(reverse("view_regional_admins"))
        except:
            messages.error(request, "Failed to Add Regional Admin")
            return HttpResponseRedirect(reverse("view_regional_admins"))


@login_required(login_url='adminlogin')
def edit_regional_admin(request, pk):
    regionaladmin = models.RegionalAdmin.objects.get(id=pk)
    regions = ['ADDIS-ABABA', 'OROMIA', 'AMHARA', 'TIGRAY', 'SOUTH',
               'GAMBELLA', 'BENSHANGUL', 'HARRARI', 'DIREDAWA', 'SIDAMA', 'SOUTH WEST']
    context = {
        "regionaladmin": regionaladmin,
        "regions": regions,
        "id": pk,
    }
    return render(request, 'Referal/edit_regional_admin.html', context)


@login_required(login_url='adminlogin')
def edit_regional_admin_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        pk = request.POST.get('id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        region = request.POST.get('region')

        try:
            regionaladmin = models.RegionalAdmin.objects.get(id=pk)
            user = models.User.objects.get(id=regionaladmin.user.id)
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.password = password
            user.save()
            regionaladmin.region = region
            regionaladmin.save()

            messages.success(
                request, "Regional Admin info Updated Successfully.")
            return redirect("view_regional_admins")

        except:
            messages.error(request, "Failed to Update Course.")
            return redirect('/edit_regional_admin/'+id)


@login_required(login_url='adminlogin')
def delete_regional_admin(request, pk):
    regionaladmin = models.RegionalAdmin.objects.get(id=pk)
    regionaladmin.delete()
    messages.success(request, "Regional Admin Deleted Successfully.")
    return redirect('view_regional_admins')


@login_required(login_url='adminlogin')
def view_regional_admins(request):
    regionadmin = models.RegionalAdmin.objects.all()
    return render(request, 'Referal/manage_regional_admins.html', {"regionadmin": regionadmin, 'segment': 'view_regional_admins'})


def is_valid_queryparam(param):
    return param != '' and param is not None


def admin_report_one(request):
    region = request.GET.get("region")
    facility = request.GET.get("facility")
    facilitys_in_reg = models.Facility.objects.all()
    liaizons = models.Liaizon.objects.all()
    if is_valid_queryparam(region):
        # facilitys_in_reg = models.Facility.objects.filter(region=region)
        facilitys_in_reg = facilitys_in_reg.filter(region=region)
        liaizons = liaizons.filter(facility__in=facilitys_in_reg)

        refer_out = models.referalrequest.objects.all().filter(liaizon__in=liaizons).count()
        refer_in = models.referalrequest.objects.all().filter(
            referal_to__in=facilitys_in_reg, status='Approved').count()
        emrg_refer_in = models.referalrequest.objects.all().filter(
            referal_to__in=facilitys_in_reg, type_of_referal='EMERGENCY').count()
        feedback_sent = models.referalrequest.objects.all().filter(
            referal_to__in=facilitys_in_reg, status='Feedback').count()
        pending = models.referalrequest.objects.all().filter(
            referal_to__in=facilitys_in_reg, status='Pending').count()
        feedback_not_sent = models.referalrequest.objects.all().filter(
            referal_to__in=facilitys_in_reg, status='Approved').count()
        inapp_with_md = models.referalrequest.objects.all().filter(
            referal_to__in=facilitys_in_reg, with_respect_to_medical_care='NO').count()
        inapp_with_trans = models.referalrequest.objects.all().filter(
            referal_to__in=facilitys_in_reg, with_respect_patient_transportation='NO').count()
        # avg_weigh_feedback_time=models.referalrequest.objects.filter(referal_to__in=facilitys_in_reg,feedback_date__isnull=False).aggregate(avg_time=Avg(F('feedback_date') - F('refered_date'),output_field=models.DateTimeField()))
        avg_weigh_feedback_time = 0
        re_direct_ref = models.referalrequest.objects.all().filter(
            referal_to__in=facilitys_in_reg, status='Re-direct').count()
    elif is_valid_queryparam(facility):
        liaizons = liaizons.filter(facility__facility_name=facility)
        print(liaizons)
        refer_out = models.referalrequest.objects.all().filter(liaizon__in=liaizons).count()
        refer_in = models.referalrequest.objects.all().filter(
            referal_to__facility_name=facility, status='Approved').count()
        emrg_refer_in = models.referalrequest.objects.all().filter(
            referal_to__facility_name=facility, type_of_referal='EMERGENCY').count()
        feedback_sent = models.referalrequest.objects.all().filter(
            referal_to__facility_name=facility, status='Feedback').count()
        pending = models.referalrequest.objects.all().filter(
            referal_to__facility_name=facility, status='Pending').count()
        feedback_not_sent = models.referalrequest.objects.all().filter(
            referal_to__facility_name=facility, status='Approved').count()
        inapp_with_md = models.referalrequest.objects.all().filter(
            referal_to__facility_name=facility, with_respect_to_medical_care='NO').count()
        inapp_with_trans = models.referalrequest.objects.all().filter(
            referal_to__facility_name=facility, with_respect_patient_transportation='NO').count()
        # avg_weigh_feedback_time=models.referalrequest.objects.filter(referal_to__facility_name=facility,feedback_date__isnull=False).aggregate(avg_time=Avg(F('feedback_date') - F('refered_date'),output_field=models.DateTimeField()))
        avg_weigh_feedback_time = 0
        re_direct_ref = models.referalrequest.objects.all().filter(
            referal_to__facility_name=facility, status='Re-direct').count()
    else:
        refer_out = models.referalrequest.objects.all().count()
        refer_in = models.referalrequest.objects.all().count()
        emrg_refer_in = models.referalrequest.objects.all().filter(
            type_of_referal='EMERGENCY', status='Approved').count()
        feedback_sent = models.referalrequest.objects.all().filter(status='Feedback').count()
        pending = models.referalrequest.objects.all().filter(status='Pending').count()
        feedback_not_sent = models.referalrequest.objects.all().filter(
            status='Approved').count()
        inapp_with_md = models.referalrequest.objects.all().filter(
            with_respect_to_medical_care='NO').count()
        inapp_with_trans = models.referalrequest.objects.all().filter(
            with_respect_patient_transportation='NO').count()
        # avg_weigh_feedback_time=models.referalrequest.objects.filter(feedback_date__isnull=False).aggregate(avg_time=Avg(F('feedback_date') - F('refered_date')))
        avg_weigh_feedback_time = 0
        re_direct_ref = models.referalrequest.objects.all().filter(status='Re-direct').count()
    regions = ['ADDIS ABBABA', 'OROMIA', 'AMHARA', 'TIGRAY', 'SOUTH',
               'GAMBELLA', 'BENSHANGUL', 'HARRARI', 'DIREDAWA', 'SIDAMA', 'SOUTH WEST']

    mydict = {
        # 'fac':regionaladmin.region,
        'refer_out': refer_out,
        'refer_in': refer_in,
        'emrg_refer_in': emrg_refer_in,
        'pending': pending,
        'feedback_sent': feedback_sent,
        'feedback_not_sent': feedback_not_sent,
        'inapp_with_md': inapp_with_md,
        'inapp_with_trans': inapp_with_trans,
        'avg_weigh_feedback_time': avg_weigh_feedback_time,
        're_direct_ref': re_direct_ref,
        'regions': regions,
        "region": region,
        "facility": facility,
        "nam": request.user.first_name + " "+request.user.last_name,
    }
    return render(request, 'Referal/admin_report_one_template.html', context=mydict)


def regional_admin_report_one(request):
    regionaladmin = models.RegionalAdmin.objects.get(user=request.user.id)
    facilitys = models.Facility.objects.filter(region=regionaladmin.region)

    facilitys_in_reg = models.Facility.objects.filter(
        region=regionaladmin.region)
    liaizons = models.Liaizon.objects.filter(facility__in=facilitys_in_reg)

    facility = request.GET.get("facility")
    facility_in_reg = facilitys_in_reg.filter(facility_name=facility).count()
    if is_valid_queryparam(facility) and facility_in_reg > 0:
        liaizons = liaizons.filter(facility__facility_name=facility)

        print(liaizons)
        refer_out = models.referalrequest.objects.all().filter(liaizon__in=liaizons).count()
        refer_in = models.referalrequest.objects.all().filter(
            referal_to__facility_name=facility, status='Approved').count()
        emrg_refer_in = models.referalrequest.objects.all().filter(
            referal_to__facility_name=facility, type_of_referal='EMERGENCY').count()
        feedback_sent = models.referalrequest.objects.all().filter(
            referal_to__facility_name=facility, status='Feedback').count()
        pending = models.referalrequest.objects.all().filter(
            referal_to__facility_name=facility, status='Pending').count()
        feedback_not_sent = models.referalrequest.objects.all().filter(
            referal_to__facility_name=facility, status='Approved').count()
        inapp_with_md = models.referalrequest.objects.all().filter(
            referal_to__facility_name=facility, with_respect_to_medical_care='NO').count()
        inapp_with_trans = models.referalrequest.objects.all().filter(
            referal_to__facility_name=facility, with_respect_patient_transportation='NO').count()
        # avg_weigh_feedback_time=models.referalrequest.objects.filter(referal_to__facility_name=facility,feedback_date__isnull=False).aggregate(avg_time=Avg(F('feedback_date') - F('refered_date'),output_field=models.DateTimeField()))
        avg_weigh_feedback_time = 0
        re_direct_ref = models.referalrequest.objects.all().filter(
            referal_to__facility_name=facility, status='Re-direct').count()
    else:
        refer_out = models.referalrequest.objects.all().filter(liaizon__in=liaizons).count()
        refer_in = models.referalrequest.objects.all().filter(
            referal_to__in=facilitys_in_reg, status='Approved').count()
        emrg_refer_in = models.referalrequest.objects.all().filter(
            referal_to__in=facilitys_in_reg, type_of_referal='EMERGENCY').count()
        feedback_sent = models.referalrequest.objects.all().filter(
            referal_to__in=facilitys_in_reg, status='Feedback').count()
        pending = models.referalrequest.objects.all().filter(
            referal_to__in=facilitys_in_reg, status='Pending').count()
        feedback_not_sent = models.referalrequest.objects.all().filter(
            referal_to__in=facilitys_in_reg, status='Approved').count()
        inapp_with_md = models.referalrequest.objects.all().filter(
            referal_to__in=facilitys_in_reg, with_respect_to_medical_care='NO').count()
        inapp_with_trans = models.referalrequest.objects.all().filter(
            referal_to__in=facilitys_in_reg, with_respect_patient_transportation='NO').count()
        # avg_weigh_feedback_time=models.referalrequest.objects.filter(feedback_date__isnull=False).aggregate(avg_time=Avg(F('feedback_date') - F('refered_date')))
        avg_weigh_feedback_time = 0
        re_direct_ref = models.referalrequest.objects.all().filter(
            referal_to__in=facilitys_in_reg, status='Re-direct').count()
    # regions = ['ADDIS ABBABA','OROMIA','AMHARA','TIGRAY','SOUTH','GAMBELLA','BENSHANGUL','HARRARI','DIREDAWA','SIDAMA','SOUTH WEST']
        nam = request.user.first_name + " " + request.user.last_name
        fac = regionaladmin.region
    mydict = {
        'refer_out': refer_out,
        'refer_in': refer_in,
        'emrg_refer_in': emrg_refer_in,
        'pending': pending,
        'feedback_sent': feedback_sent,
        'feedback_not_sent': feedback_not_sent,
        'inapp_with_md': inapp_with_md,
        'inapp_with_trans': inapp_with_trans,
        'avg_weigh_feedback_time': avg_weigh_feedback_time,
        're_direct_ref': re_direct_ref,
        "nam": request.user.first_name + " "+request.user.last_name,
        # 'fac':fac,
        "region": regionaladmin.region,
        "facility": facility
    }
    return render(request, 'Referal/region_admin_report_one_template.html', context=mydict)


@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def manage_service(request):
    liaizon = models.Facility_User.objects.get(user_id=request.user.id)
    facility = models.Facility.objects.get(id=liaizon.facility.id)
    hos = facility.facility_name
    nam = liaizon.get_name
    services = models.Facility_Service.objects.filter(facility=facility)

    return render(request, 'Referal/manage_service.html', {'services': services, 'hos': hos, 'nam': nam})


@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def add_service(request):
    liaizon = models.Facility_User.objects.get(user_id=request.user.id)
    facility = models.Facility.objects.get(id=liaizon.facility.id)
    hos = facility.facility_name
    nam = liaizon.get_name

    return render(request, 'Referal/add_service.html', {'hos': hos, 'nam': nam})


@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def add_service_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        name = request.POST.get("name")
        desc = request.POST.get("desc")
        liaizon = models.Facility_User.objects.get(user_id=request.user.id)
        facility = models.Facility.objects.get(id=liaizon.facility.id)

        try:
            service = models.Facility_Service(
                service_name=name, service_desc=desc, created_by=liaizon, facility=facility)
            service.save()
            messages.success(request, "Ward created Successfully")
            return HttpResponseRedirect(reverse("manage_service"))
        except:
            messages.error(request, "Failed to Add Ward")
            return HttpResponseRedirect(reverse("manage_service"))


def edit_service(request, pk):
    service = models.Facility_Service.objects.get(id=pk)
    return render(request, "Referal/edit_service.html", {'service': service})


@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def edit_service_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        name = request.POST.get("name")
        desc = request.POST.get("desc")
        liaizon = models.Facility_User.objects.get(user_id=request.user.id)
        facility = models.Facility.objects.get(id=liaizon.facility.id)

        try:
            ser = models.Facility_Service.objects.get(id=id)
            ser.service_name = name,
            ser.service_desc = desc,
            ser.save()
            messages.success(request, "Ward Updated Successfully")
            return HttpResponseRedirect(reverse("manage_ward"))
        except:
            messages.error(request, "Failed to Update Ward")
            return HttpResponseRedirect(reverse("manage_ward"))


@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def delete_service(request, pk):
    service = models.Facility_Service.objects.get(id=pk)
    try:
        ward.delete()
        messages.success(request, "Service Deleted Successfully.")
        return redirect('manage_ward')
    except:
        messages.error(request, "Failed to Delete Service.")
        return redirect('manage_ward')


@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def manage_ward(request):
    liaizon = models.Facility_User.objects.get(user_id=request.user.id)
    facility = models.Facility.objects.get(id=liaizon.facility.id)
    hos = facility.facility_name
    nam = liaizon.get_name
    wards = models.Ward.objects.filter(facility_id=facility)

    return render(request, 'Referal/manage_ward.html', {'wards': wards, 'hos': hos, 'nam': nam})


@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def view_ward(request, pk):
    ward = models.Ward.objects.get(id=pk)
    liaizon = models.Facility_User.objects.get(user_id=request.user.id)
    facility = models.Facility.objects.get(id=liaizon.facility.id)
    hos = facility.facility_name
    nam = liaizon.get_name
    wards = models.Ward.objects.filter(facility_id=facility)
    rooms = models.Room.objects.filter(ward=ward)
    gen = {'Male': 'Male', 'Female': 'Female', 'Both': 'Both'}
    if rooms.count() != 0:
        no_beds = models.Room.objects.filter(ward=ward).aggregate(
            Sum('no_beds')).get('no_beds__sum')
        occ_beds = models.Room.objects.filter(ward=ward).aggregate(
            Sum('occ_beds')).get('occ_beds__sum')
        free_beds = no_beds - occ_beds
        male_beds = models.Room.objects.filter(
            ward=ward, room_type='Male').aggregate(Sum('no_beds')).get('no_beds__sum')
        male_occ = models.Room.objects.filter(
            ward=ward, room_type='Male').aggregate(Sum('occ_beds')).get('occ_beds__sum')
        if male_beds != None:
            male_free = male_beds - male_occ
        else:
            male_free = 0
        female_beds = models.Room.objects.filter(
            ward=ward, room_type='Female').aggregate(Sum('no_beds')).get('no_beds__sum')
        female_occ = models.Room.objects.filter(
            ward=ward, room_type='Female').aggregate(Sum('occ_beds')).get('occ_beds__sum')
        if female_beds != None:
            female_free = female_beds - female_occ
        else:
            female_free = 0

    else:
        no_beds = 0
        occ_beds = 0
        free_beds = 0
        male_free = 0
        female_free = 0
    context = {'rooms': rooms,
               'hos': hos,
               'nam': nam,
               'ward': ward,
               'gen': gen,
               'total': no_beds,
               'occupied': occ_beds,
               'free': free_beds,
               'male_free': male_free,
               'female_free': female_free,
               }
    return render(request, 'Referal/view_ward.html', context)


@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def add_ward(request):
    liaizon = models.Facility_User.objects.get(user_id=request.user.id)
    facility = models.Facility.objects.get(id=liaizon.facility.id)
    hos = facility.facility_name
    nam = liaizon.get_name
    enquiry = models.Ward.objects.filter(facility_id=facility)

    return render(request, 'Referal/add_ward.html', {'enquiry': enquiry, 'hos': hos, 'nam': nam})


@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def add_ward_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        ward_type = request.POST.get("ward_type")
        ward_name = request.POST.get("ward_name")
        liaizon = models.Facility_User.objects.get(user_id=request.user.id)
        facility = models.Facility.objects.get(id=liaizon.facility.id)

        try:
            ward = models.Ward(
                ward_type=ward_type,
                ward_name=ward_name,
                created_by=liaizon,
                facility_id=facility
            )
            ward.save()
            messages.success(request, "Ward created Successfully")
            return HttpResponseRedirect(reverse("manage_ward"))
        except:
            messages.error(request, "Failed to Add Ward")
            return HttpResponseRedirect(reverse("manage_ward"))


def edit_ward(request, pk):
    ward = models.Ward.objects.get(id=pk)
    return render(request, "Referal/edit_ward.html", {'ward': ward})


@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def edit_ward_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        ward_id = request.POST.get("ward_id")
        ward_type = request.POST.get("ward_type")
        ward_name = request.POST.get("ward_name")
        liaizon = models.Facility_User.objects.get(user_id=request.user.id)
        facility = models.Facility.objects.get(id=liaizon.facility.id)

        try:
            w = models.Ward.objects.get(id=ward_id)
            w.ward_type = ward_type
            w.ward_name = ward_name
            w.created_by = liaizon
            w.facility_id = facility

            w.save()
            messages.success(request, "Ward Updated Successfully")
            return HttpResponseRedirect(reverse("manage_ward"))
        except:
            messages.error(request, "Failed to Update Ward")
            return HttpResponseRedirect(reverse("manage_ward"))


@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def delete_ward(request, pk):
    ward = models.Ward.objects.get(id=pk)
    try:
        ward.delete()
        messages.success(request, "Ward Deleted Successfully.")
        return redirect('manage_ward')
    except:
        messages.error(request, "Failed to Delete Ward.")
        return redirect('manage_ward')


@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def add_room_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        ward_id = request.POST.get("ward_id")
        room_no = request.POST.get("room_no")
        room_type = request.POST.get("room_type")
        no_beds = request.POST.get("no_beds")
        occ_beds = request.POST.get("occ_beds")
        free_beds = int(no_beds) - int(occ_beds)

        ward = models.Ward.objects.get(id=ward_id)
        liaizon = models.Facility_User.objects.get(user_id=request.user.id)
        facility = models.Facility.objects.get(id=liaizon.facility.id)

        try:
            room = models.Room(ward=ward,
                               room_no=room_no,
                               room_type=room_type,
                               no_beds=no_beds,
                               occ_beds=occ_beds,
                               free_beds=free_beds,
                               created_by=liaizon,
                               )
            room.save()
            messages.success(request, "New room info created successfully")
            return HttpResponseRedirect(reverse("view_ward", kwargs={"pk": ward_id}))
        except:
            messages.error(request, "Failed to Add New Room")
            return HttpResponseRedirect(reverse("view_ward", kwargs={"pk": ward_id}))


@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def edit_room_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        room_id = request.POST.get("room_id")
        ward_id = request.POST.get("ward_id")
        room_no = request.POST.get("room_no")
        room_type = request.POST.get("room_type")
        no_beds = request.POST.get("no_beds")
        occ_beds = request.POST.get("occ_beds")
        free_beds = int(no_beds) - int(occ_beds)

        ward = models.Ward.objects.get(id=ward_id)
        liaizon = models.Facility_User.objects.get(user_id=request.user.id)
        facility = models.Facility.objects.get(id=liaizon.facility.id)

        try:
            r = models.Room.objects.get(id=room_id)
            r.ward = ward
            r.room_no = room_no
            r.room_type = room_type
            r.no_beds = no_beds
            r.occ_beds = occ_beds
            r.free_beds = free_beds
            r.created_by = liaizon
            r.save()
            messages.success(request, "Room info updated successfully")
            return HttpResponseRedirect(reverse("view_ward", kwargs={"pk": ward_id}))
        except:
            messages.error(request, "Failed to update")
            return HttpResponseRedirect(reverse("view_ward", kwargs={"pk": ward_id}))


@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def delete_room(request, pk):
    room = models.Room.objects.get(id=pk)
    try:
        room.delete()
        messages.success(request, "Room Deleted Successfully!")
        return HttpResponseRedirect(reverse("view_ward", kwargs={"pk": room.ward.id}))
    except:
        messages.error(request, "Failed to Delete Room.")
        return HttpResponseRedirect(reverse("view_ward", kwargs={"pk": room.ward.id}))


@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def manage_appointment(request):
    liaizon = models.Facility_User.objects.get(user_id=request.user.id)
    facility = models.Facility.objects.get(id=liaizon.facility.id)
    hos = facility.facility_name
    apps = models.Appoint.objects.filter(
        facility=facility.id).order_by('app_date')
    nam = liaizon.get_name
    context = {'hos': hos, 'nam': nam, 'apps': apps}
    return render(request, 'Referal/manage_appointment.html', context)


@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def add_appointment(request):
    liaizon = models.Facility_User.objects.get(user_id=request.user.id)
    facility = models.Facility.objects.get(id=liaizon.facility.id)
    hos = facility.facility_name
    nam = liaizon.get_name
    gen = {'Male': 'Male', 'Female': 'Female'}
    stat = {'Pending': 'Pending', 'Admitted': 'Admitted',
            'Not Available': 'Not Available'}
    context = {'hos': hos, 'nam': nam, 'gen': gen, 'status': stat}
    return render(request, 'Referal/add_appointment.html', context)


@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def add_appointment_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        patient_mrn = request.POST.get("mrn")
        patient_name = request.POST.get("fname")
        patient_age = request.POST.get("patient_age")
        gen = request.POST.get("gen")
        diagnosis = request.POST.get("diagnosis")
        mob = request.POST.get("mob")
        department = request.POST.get("department")
        app_date = request.POST.get("app_date")
        # app_round = request.POST.get("app_round")
        reason = request.POST.get("reason")

        liaizon = models.Facility_User.objects.get(user_id=request.user.id)
        facility = models.Facility.objects.get(id=liaizon.facility.id)

        try:
            app = models.Appoint(
                patient_mrn=patient_mrn,
                patient_name=patient_name,
                gender=gen,
                patient_age=patient_age,
                mob=mob,
                diagnosis=diagnosis,
                department=department,
                app_date=app_date,
                reason=reason,
                facility=facility,
                created_by=liaizon)
            app.save()
            messages.success(request, "New Appointment created successfully")
            return HttpResponseRedirect(reverse("manage_appointment"))
        except:
            messages.error(request, "Failed to Add New Appointment")
            return HttpResponseRedirect(reverse("manage_appointment"))


@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def edit_appointment(request, pk):
    app = models.Appoint.objects.get(id=pk)
    liaizon = models.Facility_User.objects.get(user_id=request.user.id)
    facility = models.Facility.objects.get(id=liaizon.facility.id)
    hos = facility.facility_name
    nam = liaizon.get_name
    gen = {'Male': 'Male', 'Female': 'Female'}
    stat = {'Pending': 'Pending', 'Admitted': 'Admitted',
            'Not Available': 'Not Available', 'Re-Appoint': 'Re-Appoint'}
    context = {'hos': hos, 'nam': nam, 'gen': gen, 'status': stat, 'app': app}
    return render(request, "Referal/edit_appointment.html", context)


@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def edit_appointment_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        app_id = request.POST.get("app_id")
        patient_mrn = request.POST.get("mrn")
        patient_name = request.POST.get("fname")
        patient_age = request.POST.get("patient_age")
        gen = request.POST.get("gen")
        diagnosis = request.POST.get("diagnosis")
        mob = request.POST.get("mob")
        department = request.POST.get("department")
        app_date = request.POST.get("app_date")
        # app_round = request.POST.get("app_round")
        reason = request.POST.get("reason")

        liaizon = models.Facility_User.objects.get(user_id=request.user.id)
        facility = models.Facility.objects.get(id=liaizon.facility.id)

        try:
            app = models.Appoint.objects.get(id=app_id)
            app.patient_mrn = patient_mrn
            app.patient_name = patient_name
            app.gender = gen
            app.patient_age = patient_age
            app.mob = mob
            app.diagnosis = diagnosis
            app.department = department
            app.app_date = app_date
            app.reason = reason
            app.app_round = app.app_round + 1
            app.facility = facility
            app.created_by = liaizon
            app.save()
            messages.success(request, "New Appointment Updated successfully")
            return HttpResponseRedirect(reverse("manage_appointment"))
        except:
            messages.error(request, "Failed to Update Appointment")
            return HttpResponseRedirect(reverse("manage_appointment"))


@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def delete_appointment(request, pk):
    app = models.Appoint.objects.get(id=pk)
    try:
        app.delete()
        messages.success(request, "Appointment Deleted Successfully!")
        return redirect('manage_appointment')
    except:
        messages.error(request, "Failed to Delete Appointment.")
        return redirect('manage_appointment')


@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def manage_patient(request):
    liaizon = models.Facility_User.objects.get(user_id=request.user.id)
    facility = models.Facility.objects.get(id=liaizon.facility.id)
    hos = facility.facility_name
    nam = liaizon.get_name
    patients = models.Patient.objects.filter(facility_id=facility)
    return render(request, 'Referal/manage_patient.html', {'patients': patients, 'hos': hos, 'nam': nam})


@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def add_patient(request):
    liaizon = models.Facility_User.objects.get(user_id=request.user.id)
    facility = models.Facility.objects.get(id=liaizon.facility.id)
    hos = facility.facility_name
    nam = liaizon.get_name
    context = {'hos': hos, 'nam': nam, }

    return render(request, 'Referal/add_patient.html', context)


@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def add_patient_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        mrn = request.POST.get("mrn")
        fname = request.POST.get("fname")
        mob = request.POST.get("mob")
        address = request.POST.get("address")
        liaizon = models.Facility_User.objects.get(user_id=request.user.id)
        facility = models.Facility.objects.get(id=liaizon.facility.id)
        try:
            patient = models.Patient(mrn=mrn,
                                     fname=fname,
                                     mob=mob,
                                     address=address,
                                     facility_id=facility,
                                     created_by=liaizon)
            patient.save()
            messages.success(request, "Patient created Successfully")
            return HttpResponseRedirect(reverse("manage_patient"))
        except:
            messages.error(request, "Failed to Add Patient")
            return HttpResponseRedirect(reverse("add_patient"))


def edit_patient(request, pk):
    ward = models.Ward.objects.get(id=pk)
    return render(request, "Referal/edit_ward.html", {'ward': ward})


@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def edit_patient_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        ward_id = request.POST.get("ward_id")
        ward_type = request.POST.get("ward_type")
        ward_name = request.POST.get("ward_name")
        ward_desc = request.POST.get("ward_desc")
        liaizon = models.Facility_User.objects.get(user_id=request.user.id)
        facility = models.Facility.objects.get(id=liaizon.facility.id)

        try:
            w = models.Ward.objects.get(id=ward_id)
            w.ward_type = ward_type
            w.ward_name = ward_name
            w.ward_desc = ward_desc
            w.created_by = liaizon
            w.facility_id = facility

            w.save()
            messages.success(request, "Ward Updated Successfully")
            return HttpResponseRedirect(reverse("manage_ward"))
        except:
            messages.error(request, "Failed to Update Ward")
            return HttpResponseRedirect(reverse("manage_ward"))


@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def re_refer_request(request, pk):
    liaizon = models.Liaizon.objects.get(user_id=request.user.id)
    facility = models.Facility.objects.get(id=liaizon.facility.id)
    reference_to = models.ReferTo.objects.filter(facility__id=facility.id)
    facility_ref_list = []

    for reference in reference_to:
        facility_ref_list.append(reference.refer_to)

    facilitys = models.Facility.objects.filter(id__in=facility_ref_list)
    regions = ['ADDIS ABBABA', 'OROMIA', 'AMHARA', 'TIGRAY', 'SOUTH',
               'GAMBELLA', 'BENSHANGUL', 'HARRARI', 'DIREDAWA', 'SIDAMA', 'SOUTH WEST']
    pd = ['THE SAME TO REFERING FACILITY', 'NOT THE SAME TO REFERING FACILITY']
    services = models.Service.objects.all()

    re_referal_to = models.referalrequest.objects.get(id=pk)
    nam = liaizon.get_name
    hos = facility.facility_name
    return render(request, "Referal/re_refere_request.html", {"facilitys": facilitys, "regions": regions, "services": services, "re_referal_to": re_referal_to, "nam": nam, "hos": hos})


def re_referal_request_save_view(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        referal_id = request.POST.get("referal_id")
        refered_date = request.POST.get("refered_date")
        reason_for_rereferal = request.POST.get("reason_for_rereferal")

        facility = request.POST.get("referal_to")
        referal_to = models.Facility.objects.get(id=facility)
        liaizon = models.Liaizon.objects.get(user=request.user.id)

        required_srv = request.POST.get("required_service")
        # required_service = models.Service.objects.get(id=required_srv)

        try:
            refer_object = models.referalrequest.objects.get(id=referal_id)
            refer_object.reason_for_rereferal = reason_for_rereferal
            refer_object.referal_to = referal_to
            refer_object.re_referal_by = liaizon
            refer_object.re_referal_date = timezone.now()
            refer_object.status = "Re-direct"
            refer_object.save()

            messages.success(request, "Successfully Re Refer ")
            return HttpResponseRedirect(reverse("liaizon_approve_request"))
        except:
            messages.error(request, "Failed to Add Reference")
            return HttpResponseRedirect(reverse("re_refer_request", kwargs={"pk": referal_id}))


@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def patient_print_detail(request, pk):
    pad = models.referalrequest.objects.get(id=pk)
    context = {
        'pad': pad
    }
    pdf = render_to_pdf('pdf/print_patient_detail.html', context)
    return HttpResponse(pdf, content_type="application/pdf")


@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def patient_print_detail(request, pk):
    pad = models.referalrequest.objects.get(id=pk)
    context = {
        'pad': pad
    }
    pdf = render_to_pdf('pdf/print_patient_detail.html', context)
    return HttpResponse(pdf, content_type="application/pdf")


@login_required(login_url='liaizonlogin')
@user_passes_test(is_liaizon)
def patient_print_all(request):
    liaizon = models.Liaizon.objects.get(user_id=request.user.id)
    facility = models.Facility.objects.get(id=liaizon.facility.id)

    enquiry = models.referalrequest.objects.all().exclude(
        status='Pending').order_by('-id')
    context = {
        'pad': enquiry
    }
    pdf = render_to_pdf('pdf/print_patient_all.html', context)
    return HttpResponse(pdf, content_type="application/pdf")


@login_required(login_url='customerlogin')
@user_passes_test(is_CEO)
def ceo_print_all(request):
    liaizon = models.Liaizon.objects.get(user_id=request.user.id)
    facility = models.Facility.objects.get(id=liaizon.facility.id)

    enquiry = models.referalrequest.objects.all().exclude(
        status='Pending').order_by('-id')
    context = {
        'pad': enquiry
    }
    pdf = render_to_pdf('pdf/ceo_print_patient_all.html', context)
    return HttpResponse(pdf, content_type="application/pdf")
