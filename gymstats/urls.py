from django.urls import path

from . import views

app_name = 'gs'
urlpatterns = [
    path('', views.index, name='index'),
    
    # Gym views
    path('gyms/', views.gyms_homepage, name="gym-homepage"),
    path('gyms/<str:gym_abv>/', views.gym_details, name="gym"),
    path('gyms/<str:gym_abv>/problems/', views.problems_by_gym, name="gym-problems"),

    # Problem views
    path('problems/', views.problems_homepage, name="pb-homepage"),
    path('problems/<int:problem_id>/', views.problem_detail, name="pb-details"),
    path('problems/<int:problem_id>/review/', views.review_problem, name="pb-review"),
    path('problems/<int:problem_id>/reviews/<int:review_id>/', views.problem_review, name="pb-review-display"),
    path('problems/<int:problem_id>/reviews/', views.problem_reviews, name="pb-reviews")
]
