from django.urls import path
from .views import TicketListAPI, TicketDetailAPI, MessageTicketAPI

urlpatterns = [
    path('tickets/', TicketListAPI.as_view()),
    path('tickets/<int:pk>/', TicketDetailAPI.as_view()),
    path('ticket/<int:pk>/answer/', MessageTicketAPI.as_view()),
]