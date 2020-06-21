from django.urls import path
from . import views
urlpatterns = [
    path('ask/<str:username>/', views.ask_question),
    path('answer/', views.answer_question),
    path('follow/<str:username>/', views.toggle_follow),
    path('all-questions/', views.get_all_questions),
    path('all-answers/', views.get_all_answers),

    path('add-categories/', views.add_category),
    path('all-categories/',views.get_all_categories),
    path('get-users/', views.get_category_users)
]
