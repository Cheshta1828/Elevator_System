from django.urls import path
from .views import *

urlpatterns = [
    path('buildings/', BuildingView.as_view({'get': 'list', 'post': 'create'}), name='building-list'),
    path('buildings/<int:pk>/', BuildingView.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='building-detail'),
    path('elevator/', ElevatorView.as_view({'get': 'list', 'post': 'create'}), name='elevator-list'),
    path('elevator/<int:pk>/', ElevatorView.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='elevator-detail'),
     path('request_outside_elevator/', ElevatorOutsideRequestView.as_view(), name='elevator-outside-request'),
    path('elevator_status/', ElevatorStatus.as_view(), name='elevator-status'),
    path('request_inside_elevator/',ElevatorInsideRequestView.as_view(), name='elevator-inside-request')
]
