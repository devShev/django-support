from django.urls import path

from .views import MessageTicketAPI, TicketDetailAPI, TicketListAPI

urlpatterns = [
    path('tickets/', TicketListAPI.as_view(), name='tickets-list'),
    path('tickets/<int:pk>/', TicketDetailAPI.as_view()),
    path('tickets/<int:pk>/msg/', MessageTicketAPI.as_view()),
]
