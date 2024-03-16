from django.urls import path

from .views import ProfileUpdateView, ProfileDetailView

urlpatterms = [
    path('user/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('user/<str:slug>/', ProfileDetailView.as_view(), name='profile_detail')
]