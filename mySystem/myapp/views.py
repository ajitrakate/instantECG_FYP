from turtle import done
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,UpdateView)
from django.contrib.auth import login
import json
from .forms import PatientSignUpForm, DoctorSignUpForm
from .models import User, Patient, Doctor, Appointment


# def dashboard(request):
#     param = {'user':request.user}
#     return render(request, 'dashboard.html', param)
@login_required
def myECGView(request):
    if request.user.pk==4:
        return render(request, 'ecgView.html')
    else:
        param = {'message':"No data found"}
        return render(request, 'myECG.html', param)

@login_required
def patientECG(request, pk):
    if pk==4:
        return render(request, 'patientsECGView.html')
    else:
        param = {'message':"No data found"}
        return render(request, 'patientsECG.html', param)


@login_required
def myPatients(request):
    mydoctor = request.user.pk
    appointments = Appointment.objects.filter(doctorID=mydoctor)
    patients = []
    for appointment in appointments:
        patient = Patient.objects.filter(user=appointment.patientID)[0]
        if not patient in patients:
            patients.append(patient)
    param = {'patients':patients}
    # return HttpResponse(json.dumps(param), content_type="application/json")
    print(patients)
    return render(request, 'mypatients.html', param)




class PatientSignUpView(CreateView):
    model = User
    form_class = PatientSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'patient'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('dashboard')



class DoctorSignUpView(CreateView):
    model = User
    form_class = DoctorSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'doctor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('dashboard')

class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    doctors = Doctor.objects.all()
    param = {'doctors':doctors}
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'myapp/home.html', param)

@login_required
def dashboard(request):
    if request.user.is_doctor:
        mydoctor = Doctor.objects.get(user=request.user)
        appointments = Appointment.objects.filter(doctorID=mydoctor.pk)
        totalAppointments = len(appointments)
    else:
        mypatient = Patient.objects.get(user=request.user)
        appointments = Appointment.objects.filter(patientID=mypatient.pk)
        totalAppointments = len(appointments)
    pendingApointments = 0
    appovedAppointments = 0
    myappointments = []
    for appointment in appointments:
        if appointment.status == "Approved":
            appovedAppointments += 1
        elif appointment.status == "Pending":
            pendingApointments += 1
            myappointments.append(appointment)
        else:
            pendingApointments += 1
    param = {'user': request.user, 'appointments':myappointments, 'totalAppointments':totalAppointments, 'appovedAppointments':appovedAppointments, 'pendingApointments':pendingApointments}
    return render(request, 'dashboard.html', param)

@login_required
def dashDoctors(request):
    doctors = Doctor.objects.all()
    param = {'doctors': doctors}
    for doctor in doctors:
        print(doctor.specialization)
    return render(request, 'dashDoctors.html', param)


@login_required
def bookAppointment(request, pk):
    dr = Doctor.objects.get(pk=pk)
    param = {'id':pk, 'username':dr.user.username}
    return render(request, 'bookAppointment.html', param)

@login_required
def book(request):
    doctorID = request.GET.get('doctorId')
    dr = Doctor.objects.get(pk=doctorID)
    doctorUsername = dr.user.username
    patient = Patient.objects.get(user=request.user)
    patientUsername = patient.user.username
    patientID = patient.pk
    date = request.GET.get('date')
    desc = request.GET.get('desc')
    appointment = Appointment.objects.create(doctorID=doctorID,patientID=patientID,patientUsername=patientUsername,doctorUsername=doctorUsername,date=date,status="Pending",description=desc)
    appointment.save()
    return redirect('dashboard')


@login_required
def approve(request,pk):
    appointment = Appointment.objects.get(pk=pk)
    appointment.status = "Approved"
    appointment.save()
    return redirect('dashboard')

@login_required
def reject(request, pk):
    appointment = Appointment.objects.get(pk=pk)
    appointment.status = "Rejected"
    appointment.save()
    return redirect('dashboard')

@login_required
def cancel(request,pk):
    appointment = Appointment.objects.get(pk=pk)
    appointment.delete()
    return redirect('dashboard')



@login_required
def profile(request):
    param = {'user': request.user}
    return render(request, 'profile.html', param)

@login_required
def createAppointment(request):
    param = {'user': request.user}
    return render(request, 'createAppointment.html', param)

@login_required
def allAppointments(request):
    if request.user.is_doctor:
        appointments = Appointment.objects.filter(doctorID=request.user.pk)
    else:
        appointments = Appointment.objects.filter(patientID=request.user.pk)
    param = {'appointments':appointments}
    return render(request, 'allAppointments.html', param)


# def home(request):
#     return render(request, 'myapp/home.html')

def about(request):
    return render(request, 'myapp/about.html')

def doctors(request):
    doctors = Doctor.objects.all()
    param = {'doctors':doctors}
    return render(request, 'myapp/doctors.html', param)

def contact(request):
    return render(request, 'myapp/contact.html')


@login_required
def getData(request,n):
    print(n)
    start = n
    interval = 0.01
    points = 101
    values = []
    for i in range(points):
        values.append(round(start,2))
        start += interval
 
    data = ['0', '0.00001023', '0.000019995', '0.00003627', '0.0000744', '0.000093', '0.0001116', '0.0001209', '0.0001023', '0.0000744', '0.0000372', '0', '-0.0000186', '-0.0000279', 
    '-0.0000279', '-0.0000372', '-0.0000465', '-0.0000558', '-0.0000651', '-0.0000744', '-0.0000837', '-0.000093', '-0.0001116', '-0.0001302', '-0.0001488', '-0.0001767', '-0.0002232',
     '-0.0002604', '-0.000279', '-0.0002511', '-0.000093', '0.000465', '0.00186', '0.002046', '0.0016275', '0', '-0.000186', '-0.000372', '-0.0004185', '-0.0003255', '-0.000186',
      '-0.0001395', '-0.000093', '-0.0000465', '-0.0000186', '-0.0000093', '0', '0', '0', '0', '0', '0', '0', '0', 
    '0', '0', '0', '0', '0', '0', '0.000009207', '0.0000186', '0.0000372', '0.0000465', '0.0000651', '0.0000837', '0.0001023', '0.0001209', '0.0001488', '0.0001953', '0.0002325', '0.0002511',
    '0.0002604', '0.0002418', '0.000186', '0.0001395', '0.000093', '0.0000558', '0.0000279', '0.0000186', '0.0000093', '0.0000093', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
    '0', '0', '0', '0', '0', '0', '0']
    lst = []
    param = {"lst":lst}
    for i in range(101):
        lst.append({"x":float(values[i]), "y":float(data[i])})
    return HttpResponse(json.dumps(param), content_type="application/json")