from django.shortcuts import render
from users.models import Driver_info
from .models import Rideowner, Ridesharer,User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.core.mail import send_mail

def home(request):
    return render(request, 'ride/home.html')

def rideowner_home(request):
    return render(request, 'ride/rideowner_home.html')

def ridesharer_home(request):
    return render(request, 'ride/ridesharer_home.html')

def driver_home(request):
    driver = Driver_info.objects.filter(user = request.user.id).first()
    if driver.license_number == '':
        return render(request, 'ride/driver_register.html')
    return render(request, 'ride/driver_home.html')


class DriverListView(ListView):
    template_name = 'ride/driver_list.html'
    def get_queryset(self):
        return Rideowner.objects.filter(status__in=['open','pending'],
                                        passenger_num__lte=self.request.user.driver_info.max_number,
                                        required_type__in=['--', self.request.user.driver_info.vehicle_type],
                                        required_special__in=['', self.request.user.driver_info.special_info]).exclude(owner=self.request.user).order_by('arrive_date')



class DriverWorkListView(ListView):
    template_name = 'ride/driverwork_list.html'
    def get_queryset(self):
        return Rideowner.objects.filter(status='confirm',
                                        driver_name = self.request.user.username).exclude(owner=self.request.user).order_by('arrive_date')




class DriverPastListView(ListView):
    template_name = 'ride/driverpast_list.html'
    def get_queryset(self):
        return Rideowner.objects.filter(status='complete',
                                        driver_name = self.request.user.username).exclude(owner=self.request.user).order_by('arrive_date')



def confirm(request, rid):
    driver = Driver_info.objects.filter(user = request.user.id).first()
    ride = Rideowner.objects.filter(pk = rid).first();
    ride.status = 'confirm';
    ride.driver_name= request.user.username
    ride.driver_license = driver.license_number
    ride.save();
    send_mail(
        'Here is the message',
        'As a ride-owner, your ride has been comfirmed',
        'ride-share-service@outlook.com',
        [ride.owner.email],
        fail_silently=False,
    )
    sharer = User.objects.filter(username=ride.share_name).first()
    if sharer:
        send_mail(
            'Here is the message',
            'As a ride-sharer, your ride has been comfirmed',
            'ride-share-service@outlook.com',
            [sharer.email],
            fail_silently=False,
        )
    return render(request, 'ride/driver_home.html')

def complete(request, rid):
    ride = Rideowner.objects.filter(pk = rid).first();
    ride.status = 'complete';
    ride.save();
    return render(request, 'ride/driver_home.html')


class RideOwnerPastListView(ListView):
    template_name = 'ride/driverpast_list.html'
    def get_queryset(self):
        return Rideowner.objects.filter(status='complete', owner = self.request.user).order_by('arrive_date')



class RideOwnerListView(ListView):
    template_name = 'ride/rideowner_list.html'
    def get_queryset(self):
        return Rideowner.objects.filter(owner=self.request.user).exclude(status='complete').order_by('arrive_date')



class RideOwnerCreateView(LoginRequiredMixin, CreateView):
    model = Rideowner
    fields = ['addr', 'arrive_date', 'passenger_num', 'whether_share', 'max_share_num', 'required_type', 'required_special']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)



class RideOwnerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Rideowner
    fields = ['addr', 'arrive_date', 'passenger_num', 'whether_share', 'max_share_num', 'required_type', 'required_special']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        ride_owner = self.get_object()
        if self.request.user == ride_owner.owner:
            return True
        return False


class RideOwnerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Rideowner
    success_url = '/rideowner/listview/'

    def test_func(self):
        ride_owner = self.get_object()
        if self.request.user == ride_owner.owner:
            return True
        return False



class RideSharerCreateView(LoginRequiredMixin, CreateView):
    model = Ridesharer
    fields = ['addr', 'earliest_arrive_date', 'latest_arrive_date','passenger_num']

    def form_valid(self, form):
        form.instance.sharer = self.request.user
        return super().form_valid(form)


class SharerPickListView(ListView):
    template_name = 'ride/ridesharer_list.html'
    def get_queryset(self):
        share = self.request.user.ridesharer_set.last()
        return Rideowner.objects.filter(whether_share=True,
                                        addr=share.addr,
                                        status='open',
                                        arrive_date__gte=share.earliest_arrive_date,
                                        arrive_date__lte=share.latest_arrive_date,
                                        max_share_num__gte=share.passenger_num,
                                   ).exclude(owner=self.request.user).order_by('arrive_date')


class RideSharerResultListView(ListView):
    template_name = 'ride/ridesharerresult_list.html'
    def get_queryset(self):
        share = self.request.user.ridesharer_set.last()
        return Rideowner.objects.filter(share_name=self.request.user.username
                                   ).exclude(owner=self.request.user).exclude(status='complete').order_by('arrive_date')


class RideSharerPastListView(ListView):
    template_name = 'ride/driverpast_list.html'
    def get_queryset(self):
        return Rideowner.objects.filter(status='complete', share_name = self.request.user.username).order_by('arrive_date')



def join(request, rid):
    ride = Rideowner.objects.filter(pk = rid).first();
    share_person = Ridesharer.objects.filter(sharer = request.user.id).last()
    ride.status = 'pending'
    ride.share_name = request.user.username
    ride.share_num = share_person.passenger_num
    ride.passenger_num = ride.passenger_num + ride.share_num
    ride.save();
    return render(request, 'ride/ridesharer_home.html')


def cancel(request, rid):
    ride = Rideowner.objects.filter(pk = rid).first();
    share_person = Ridesharer.objects.filter(sharer = request.user.id).last()
    ride.status = 'open'
    ride.share_name = ''
    ride.passenger_num = ride.passenger_num - ride.share_num
    ride.share_num = 0
    ride.save();
    return render(request, 'ride/ridesharer_home.html')

