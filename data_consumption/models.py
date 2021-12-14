from django.db import models


class Timestamp(models.Model):
    date_uploaded = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class BuildingData(models.Model):
    id = models.IntegerField(primary_key=True, editable=False, unique=True)
    name = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = "building_data"


class BuildingDataBulkUpload(Timestamp):
    building_csv_file = models.FileField(upload_to='data/building/bulkupload/')

    class Meta:
        db_table = "building_data_bulk_upload"


class MeterData(models.Model):
    id = models.IntegerField(primary_key=True, editable=False, unique=True)
    fuel = models.CharField(max_length=255, null=True)
    unit = models.CharField(max_length=20, null=True)
    building = models.ForeignKey(BuildingData, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "meter_data"


class MeterDataBulkUpload(Timestamp):
    meter_csv_file = models.FileField(upload_to='data/meter/bulkupload/')

    class Meta:
        db_table = "meter_data_bulk_upload"


class HalfHourlyData(models.Model):
    consumption = models.FloatField(null=True)
    reading_date_time = models.DateTimeField()
    meter = models.ForeignKey(MeterData, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "half_hourly_data"


class HalfHourlyDataBulkUpload(Timestamp):
    half_hour_csv_file = models.FileField(upload_to='data/halfhourly/bulkupload/')

    class Meta:
        db_table = "half_hour_data_bulk_upload"
