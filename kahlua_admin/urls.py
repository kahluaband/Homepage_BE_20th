from django.urls import path
from .views.tickets_views import FreshmanViewSet
from .views.application_views import ApplicationRetrieveView

app_name = 'kahlua_admin'

urlpatterns = [
    path('tickets/freshman_tickets/', FreshmanViewSet.as_view({'get':'list'}), name='freshman_list'),
    path('application/apply_forms/', ApplicationRetrieveView.as_view(), name='view_apply_forms'),
]
