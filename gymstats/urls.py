from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:gym_abv>/problems', views.problems_by_gym, name="problems"),
    path('problems/<int:id>', views.problem_detail, name="problem-details")
]