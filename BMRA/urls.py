from django.urls import path
from . import views

app_name = 'BMRA'
urlpatterns = [
    path('', views.list_unused_BMUs, name='unused_BMUs'),
    path('regional_generation_bytype', views.regional_generation_bytype, name='regional_generation_bytype'),
    path('regional_demand', views.regional_demand, name='regional_demand'),
    path('live_boas', views.live_boas, name='live_boas'),
    path('test_chart_data', views.test_chart_data, name='test_chart_data'),
    path('test_chart', views.test_chart, name='test_chart'),
    path('d3_test', views.d3_test, name='d3_test'),
    path('d3_test2', views.d3_test2, name='d3_test2'),
    path('vega_test', views.vega_test, name='vega_test')
]
