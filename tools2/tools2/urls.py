"""tools2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.conf.urls import url, include
from django.urls import re_path, path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
import sunscreen.views

urlpatterns = [
    path('admin/', admin.site.urls),

    re_path(r'^$', sunscreen.views.front, name='front'),

    re_path(r'^register$', sunscreen.views.register, name='register'),
    re_path(r'^login$', sunscreen.views.userlogin, name='login'),
    re_path(r'^join$', sunscreen.views.join, name='join'),

    re_path(r'^section/(?P<section_id>\d+)$', sunscreen.views.section, name='section'),
    re_path(r'^discuss', sunscreen.views.discuss, name='discuss_expert'),
    re_path(r'^quiz/(?P<quiz_id>\d+)$', sunscreen.views.quiz, name='quiz'),
    re_path(r'^submitquiz', sunscreen.views.submitquiz, name='submitquiz'),

    re_path(r'^add-post$', sunscreen.views.add_post, name='add-post'),

    re_path(r'^get-global-stream-posts$', sunscreen.views.get_expert_stream_posts, name='get-global-stream-posts'),
    re_path(r'^get-global-stream-changes$', sunscreen.views.get_expert_stream_changes, name='get-global-stream-changes'),
    re_path(r'^get-global-stream-changes/(?P<time>.+)$', sunscreen.views.get_expert_stream_changes, name='get-global-stream-changes'),

    re_path(r'^get-group-stream-posts$', sunscreen.views.get_group_stream_posts, name='get-group-stream-posts'),
    re_path(r'^get-group-stream-changes$', sunscreen.views.get_group_stream_changes, name='get-group-stream-changes'),
    re_path(r'^get-group-stream-changes/(?P<time>.+)$', sunscreen.views.get_group_stream_changes, name='get-group-stream-changes'),
    
    re_path(r'^get-comments/(?P<post_id>\d+)$', sunscreen.views.get_comments),
    re_path(r'^get-comments/(?P<post_id>\d+)/(?P<time>.+)$', sunscreen.views.get_comments),
    re_path(r'^get-comment-changes/(?P<post_id>\d+)/$', sunscreen.views.get_comment_changes),
    re_path(r'^get-comment-changes/(?P<post_id>\d+)/(?P<time>.+)$', sunscreen.views.get_comment_changes),
    re_path(r'^add-comment/(?P<post_id>\d+)$', sunscreen.views.add_comment),

    re_path(r'^logout$', auth_views.logout_then_login, name='logout'),
]
