from django.urls import path
from . import views
from .views import (RideOwnerCreateView,
                    RideOwnerListView,
                    RideOwnerPastListView,
                    RideOwnerUpdateView,
                    RideOwnerDeleteView,
                    DriverListView,
                    DriverWorkListView,
                    DriverPastListView,
                    RideSharerCreateView,
                    RideSharerPastListView,
                    SharerPickListView,
                    RideSharerResultListView)


urlpatterns = [
    path('', views.home, name='ride-home'),
    path('driver/', views.driver_home, name='driver_searching'),
    path('driver/listview/', DriverListView.as_view(), name='driver-list'),
    path('driver/worklistview/', DriverWorkListView.as_view(), name='driverwork-list'),
    path('driver/pastlistview/', DriverPastListView.as_view(), name='driverpast-list'),
    path('driver/<int:rid>/confirm/', views.confirm, name='driver-confirm'),
    path('driver/<int:rid>/complete/', views.complete, name='driver-complete'),
    #Owner Website links
    path('rideowner/', views.rideowner_home, name='rideowner-home'),
    path('rideowner/new/', RideOwnerCreateView.as_view(), name='rideowner-create'),
    path('rideowner/listview/', RideOwnerListView.as_view(), name='rideowner-list'),
    path('rideowner/pastlistview/', RideOwnerPastListView.as_view(), name='rideownerpast-list'),
    path('rideowner/listview/<int:pk>/update/', RideOwnerUpdateView.as_view(), name='rideowner-update'),
    path('rideowner/listview/<int:pk>/delete/', RideOwnerDeleteView.as_view(), name='rideowner-delete'),
    path('ridesharer/', views.ridesharer_home, name='ridesharer-home'),
    #path('ridesharer/', views.ridesharer_home, name='ridesharer-home'),
    path('ridesharer/new/', RideSharerCreateView.as_view(), name='ridesharer-create'),
    path('ridesharer/listview/', SharerPickListView.as_view(), name='ridesharer-list'),
    path('ridesharer/pastlistview/', RideSharerPastListView.as_view(), name='ridesharerpast-list'),
    path('ridesharer/<int:rid>/join/', views.join, name='share-join'),
    path('ridesharer/<int:rid>/cancel/', views.cancel, name='share-cancel'),
    path('ridesharer/resultlistview/', RideSharerResultListView.as_view(), name='ridesharerresult-list'),
]
