from django.urls import path

from . import views

app_name = 'gs'
urlpatterns = [
    path('', views.index, name='index'),
    
    # Home Page
    path('home/', views.home, name="home"),

    # Profil Page
    path('profil/', views.profil, name="profil"),

    # Session
    path('session/<int:session_id>/', views.session, name="session"),
    path('session/<int:session_id>/statistics/', views.session_statistics, name='session-statistics'),
    path('session/<int:session_id>/details', views.session_details, name="session-details"),

    # Gym views
    path('gyms/', views.gyms_homepage, name="gym-homepage"),
    path('gyms/<str:gym_abv>/', views.gym_details, name="gym"),
    path('gyms/<str:gym_abv>/problems/', views.problems_by_gym, name="gym-problems"),

    # Problem views
    path('problems/', views.problems_homepage, name="pb-homepage"),
    path('problems/<int:problem_id>/', views.problem_detail, name="pb-details"),
    path('problems/<int:problem_id>/review/', views.review_problem, name="pb-review"),
    path('problems/<int:problem_id>/ric/', views.evaluate_ric_problem, name="pb-ric"),
    path('problems/<int:problem_id>/rics/<int:ric_id>/', views.problem_ric, name="pb-ric-display"),
    path('problems/<int:problem_id>/reviews/<int:review_id>/', views.problem_review, name="pb-review-display"),
    path('problems/<int:problem_id>/reviews/', views.problem_reviews, name="pb-reviews"),
    path('problems/searchbar/', views.problem_searchbar, name="pb-searchbar"),
    path('problems/search-results', views.problem_search_results, name="pb-searchresults")
]
