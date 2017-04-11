from django.conf.urls import url, include
from django.contrib import admin

from users.views import IndexView, ActiveUserView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="active"),
    url(r'^user/', include('users.urls', namespace="user")),
]
