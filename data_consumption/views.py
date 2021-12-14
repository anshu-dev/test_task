from calendar import monthrange

import pandas as pd
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from matplotlib.backends.backend_agg import FigureCanvasAgg

from data_consumption.forms import MeterBulkUploadForm, HalfHourlyUploadForm, BuildingBulkUploadForm
from data_consumption.models import BuildingData, MeterData, HalfHourlyData
from tech_test.celery_task.tasks import create_building_data, create_meter_data, \
    create_half_hourly_data
import matplotlib.pyplot as plt


class UploadAndSaveView(View):

    @staticmethod
    def get(request):
        meter_form = MeterBulkUploadForm()
        half_hourly_form = HalfHourlyUploadForm()
        building_form = BuildingBulkUploadForm()
        return render(request, 'index.html', {'meter_form': meter_form, 'half_hourly_form': half_hourly_form,
                                              'building_form': building_form})

    @staticmethod
    def post(request):
        building_form = BuildingBulkUploadForm(data=request.POST, files=request.FILES)
        if building_form.is_valid():
            building_file = building_form.save()
            tmp_data = pd.read_csv(building_file.building_csv_file.name)
            tmp_data = tmp_data.loc[:, ~tmp_data.columns.str.contains('^Unnamed')]
            tmp_data = tmp_data.dropna(how='any', axis=0)
            length = len(tmp_data)
            create_building_data.delay(length, tmp_data.to_json())
        meter_form = MeterBulkUploadForm(data=request.POST, files=request.FILES)
        if meter_form.is_valid():
            meter_file = meter_form.save()
            tmp_data = pd.read_csv(meter_file.meter_csv_file.name)
            tmp_data = tmp_data.loc[:, ~tmp_data.columns.str.contains('^Unnamed')]
            tmp_data = tmp_data.dropna(how='any', axis=0)
            length = len(tmp_data)
            create_meter_data.delay(length, tmp_data.to_json())
        half_hourly_form = HalfHourlyUploadForm(data=request.POST, files=request.FILES)
        if half_hourly_form.is_valid():
            half_hourly_file = half_hourly_form.save()
            tmp_data = pd.read_csv(half_hourly_file.half_hour_csv_file.name)
            tmp_data = tmp_data.loc[:, ~tmp_data.columns.str.contains('^Unnamed')]
            tmp_data = tmp_data.dropna(how='any', axis=0)
            length = len(tmp_data)
            create_half_hourly_data.delay(length, tmp_data.to_json())
        return redirect("/buildings/")


class ListBuildingsView(ListView):
    model = BuildingData
    template_name = 'building_list.html'
    context_object_name = 'buildings'


class ListMeterView(ListView):
    model = MeterData
    template_name = 'meter_list.html'
    context_object_name = 'meters'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(building__id=self.kwargs['pk'])


class ListMeterHourlyDataView(ListView):
    model = HalfHourlyData
    template_name = 'half_hourly_data.html'
    context_object_name = 'half_hourly_data'

    def get_queryset(self):
        qs = super().get_queryset()
        return {"queryset": qs.filter(meter__id=self.kwargs['meter_id']), "meter_id": self.kwargs['meter_id']}


class ShowChartView(View):
    Months = ['January', 'FebruaryFebruary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']

    def get(self, _, pk):
        days = []
        consumption = []
        half_hourly_obj = HalfHourlyData.objects.filter(meter__id=pk).first()
        last_day = monthrange(half_hourly_obj.reading_date_time.year, half_hourly_obj.reading_date_time.month)[1]
        for day in range(1, last_day + 1):
            consumption.append(HalfHourlyData.objects.filter(meter__id=pk, reading_date_time__day=day).aggregate(
                daily_consumption=Sum('consumption'))["daily_consumption"])
            days.append(day)
        fig = plt.figure(figsize=(10, 5))
        ax = plt.gca()
        plt.xlabel('Days')
        plt.ylabel('Consumption (kWh)')
        plt.title(f'Daily Consumption For Month {self.Months[half_hourly_obj.reading_date_time.month - 1]}')
        consumption = [x if x else 0.0 for x in consumption]
        ax.bar(days, consumption)
        canvas = FigureCanvasAgg(fig)
        response = HttpResponse(content_type='image/png')
        canvas.print_png(response)
        return response
