from django.urls import path

from data_consumption.views import UploadAndSaveView, ListBuildingsView, ListMeterView, ListMeterHourlyDataView, \
    ShowChartView

urlpatterns = [
    path("upload/", UploadAndSaveView.as_view()),
    path("buildings/", ListBuildingsView.as_view()),
    path("buildings/<int:pk>/meters/", ListMeterView.as_view()),
    path("buildings/<int:pk>/meters/<int:meter_id>/half-hourly-data/", ListMeterHourlyDataView.as_view()),
    path("meter/<int:pk>/show-chart/", ShowChartView.as_view())
]
