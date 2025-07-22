from django.urls import path
from . import views
from django.urls import path
from .views import profile_view


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('get-balance/', views.get_balance, name='get_balance'),
    path('buy-ticket/', views.buy_ticket, name='buy_ticket'),  # just one route
    path('guide/', views.guide_view, name='guide'),
    path('ticket/', views.ticket_view, name='ticket'),
    path('purchase/', views.purchasing_view, name='purchase_ticket'),
    path('add_recharge/', views.add_recharge, name='add_recharge'),
    path('buy/', views.buy_ticket, name='buy_ticket'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),



]
