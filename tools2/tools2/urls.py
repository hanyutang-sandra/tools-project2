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

    re_path(r'^end$', sunscreen.views.end, name='end'),

    re_path(r'^section/(?P<section_id>\d+)$', sunscreen.views.section, name='section'),
    re_path(r'^discuss', sunscreen.views.discuss, name='discuss_expert'),
    re_path(r'^teach', sunscreen.views.group, name='discuss_group'),
    re_path(r'^quiz/(?P<quiz_id>.+)$', sunscreen.views.quiz, name='quiz'),
    re_path(r'^checkquiz/(?P<quiz_id>.+)$', sunscreen.views.checkquiz, name='checkquiz'),
    re_path(r'^final', sunscreen.views.final, name='final'),
    re_path(r'^checkfinal', sunscreen.views.checkfinal, name='checkfinal'),

    re_path(r'^add-expertpost$', sunscreen.views.add_expertpost, name='add-expertpost'),
    re_path(r'^add-grouppost$', sunscreen.views.add_grouppost, name='add-grouppost'),

    re_path(r'^get-expert-stream-posts$', sunscreen.views.get_expert_stream_posts, name='get-expert-stream-posts'),
    re_path(r'^get-expert-stream-changes$', sunscreen.views.get_expert_stream_changes, name='get-expert-stream-changes'),
    re_path(r'^get-expert-stream-changes/(?P<time>.+)$', sunscreen.views.get_expert_stream_changes, name='get-expert-stream-changes'),

    re_path(r'^get-group-stream-posts$', sunscreen.views.get_group_stream_posts, name='get-expert-stream-posts'),
    re_path(r'^get-group-stream-changes$', sunscreen.views.get_group_stream_changes, name='get-expert-stream-changes'),
    re_path(r'^get-group-stream-changes/(?P<time>.+)$', sunscreen.views.get_group_stream_changes, name='get-expert-stream-changes'),
    
    re_path(r'^get-comments/(?P<post_id>\d+)$', sunscreen.views.get_comments),
    re_path(r'^get-comments/(?P<post_id>\d+)/(?P<time>.+)$', sunscreen.views.get_comments),
    re_path(r'^get-comment-changes/(?P<post_id>\d+)/$', sunscreen.views.get_comment_changes),
    re_path(r'^get-comment-changes/(?P<post_id>\d+)/(?P<time>.+)$', sunscreen.views.get_comment_changes),
    re_path(r'^add-comment/(?P<post_id>\d+)$', sunscreen.views.add_comment),

    re_path(r'^logout$', auth_views.logout_then_login, name='logout'),
]
