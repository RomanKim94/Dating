from django.urls import path, include, re_path

from .views import PersonViewSet
from ..match.views import MatchViewSet

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('create/', PersonViewSet.as_view({'post': 'create'})),
    path('<int:id>/match/', MatchViewSet.as_view({'post': 'create'})),
    path('list/', PersonViewSet.as_view({'get': 'list'})),
    path('detail/<int:id>/', PersonViewSet.as_view({'get': 'retrieve'})),
]

