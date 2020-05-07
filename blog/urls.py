from django.urls import path

from .views import BlogList, BlogDetail, UserList, UserDetail
from .viewsets import UserViewSet, BlogViewSet
from rest_framework.routers import SimpleRouter

# for viewsets
'''
router = SimpleRouter()
router.register("users", UserViewSet)
router.register("", BlogViewSet)

urlpatterns = router.urls

'''

urlpatterns = [
    path('users/',UserList.as_view(),name='users'),
    path('users/<int:pk>/',UserDetail.as_view(), name='user'),
    path('',BlogList.as_view(),name='list'),
    path('<int:pk>',BlogDetail.as_view(),name='detail')
]
