from django import forms

from data_consumption.models import MeterDataBulkUpload, HalfHourlyDataBulkUpload, BuildingDataBulkUpload


class MeterBulkUploadForm(forms.ModelForm):
    class Meta:
        model = MeterDataBulkUpload
        fields = ("meter_csv_file",)


class HalfHourlyUploadForm(forms.ModelForm):
    class Meta:
        model = HalfHourlyDataBulkUpload
        fields = ("half_hour_csv_file",)


class BuildingBulkUploadForm(forms.ModelForm):
    class Meta:
        model = BuildingDataBulkUpload
        fields = ("building_csv_file",)
