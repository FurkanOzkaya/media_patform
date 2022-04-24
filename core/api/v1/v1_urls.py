from xml.etree.ElementInclude import include
from django.conf import settings
from django.urls import path
from core.api.v1.views.all_info import AllInfoAPI
from core.api.v1.views.channel import ChannelAPI
from core.api.v1.views.contents import ContentsAPI
from core.api.v1.views.sub_channel import SubChannelAPI


urlpatterns = [
    path('all-info/', AllInfoAPI.as_view()),
    path('channel/', ChannelAPI.as_view()),
    # str used for 400 case /as will return 400 not valid int 404 to 400
    path('sub-channel/<str:id>', SubChannelAPI.as_view()),
    path('contents/<str:id>', ContentsAPI.as_view()),
]
