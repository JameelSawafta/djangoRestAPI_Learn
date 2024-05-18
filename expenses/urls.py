from django.urls import path
from . import views

urlpatterns = [

    path('',views.ExpensesList.as_view(),name='expenses'),
    path('<int:id>',views.ExpenseDetail.as_view(),name='ExpenseDetail'),


]
