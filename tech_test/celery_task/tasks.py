import json

from celery import shared_task
from celery.utils.log import get_task_logger

from data_consumption.models import BuildingData, MeterData, HalfHourlyData

logger = get_task_logger(__name__)


@shared_task
def create_building_data(length, tmp_data):
    data = json.loads(tmp_data)
    building_data =[]
    for i in range(length):
        id = data.get("id").get(str(i))
        name = data.get("name").get(str(i))
        building_data_exists = BuildingData.objects.filter(id=id).exists()
        if not building_data_exists:
            building_data.append(BuildingData(id=id, name=name))
        else:
            BuildingData.objects.filter(id=id).update(name=name)
    BuildingData.objects.bulk_create(building_data)


@shared_task
def create_meter_data(length, tmp_data):
    data = json.loads(tmp_data)
    meter_data = []
    for i in range(length):
        try:
            id = data.get("id").get(str(i))
            fuel = data.get("fuel").get(str(i))
            unit = data.get("unit").get(str(i))
            building_data = BuildingData.objects.get(id=data.get("building_id").get(str(i)))
            meter = MeterData.objects.filter(id=id)
            if not meter.exists():
                meter_data.append(
                    MeterData(id=id, fuel=fuel,
                              unit=unit,
                              building=building_data))
            else:
                MeterData.objects.filter(id=id).update(fuel=fuel, unit=unit, building=building_data)

        except BuildingData.DoesNotExist:
            continue

    MeterData.objects.bulk_create(meter_data)


@shared_task
def create_half_hourly_data(length, tmp_data):
    data = json.loads(tmp_data)
    half_hourly_data = []
    for i in range(length):
        try:
            consumption = data.get("consumption").get(str(i))
            reading_date_time = data.get("reading_date_time").get(str(i))
            meter = MeterData.objects.get(id=data.get("meter_id").get(str(i)))
            half_hourly_data.append(HalfHourlyData(consumption=consumption,
                                                   reading_date_time=reading_date_time,
                                                   meter=meter))

        except MeterData.DoesNotExist:
            continue
    HalfHourlyData.objects.bulk_create(half_hourly_data)
