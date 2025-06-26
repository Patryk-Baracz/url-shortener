from django.urls import path
from .views import ShortenURLView, OriginalURLView, RedirectView

urlpatterns = [
    path('shorten/', ShortenURLView.as_view(), name='shorten_url'),
    path('original/<str:shortened_url>/', OriginalURLView.as_view(), name='original_url'),
    path('shrt/<str:shortened_url>/', RedirectView.as_view(), name='redirect_url'),
]