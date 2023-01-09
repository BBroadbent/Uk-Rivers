from django.urls import path

from .views import ActivateAccount, SignUpView

urlpatterns = [
    # path('signup/', SignUpView.as_view(), name='signup'),
    # path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
]