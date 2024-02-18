from django.db import models
from math import sin, cos, sqrt, atan2, radians


class TruckModel(models.Model):
    name = models.CharField(max_length=255,
                            blank=False, null=False)
    type = models.CharField(max_length=255, choices=(
        ("Push Cart", "Push Cart"), ("Food Truck", "Food Truck")))
    locationx = models.DecimalField(max_digits=15, decimal_places=10)
    locationy = models.DecimalField(max_digits=15, decimal_places=10)
    status = models.CharField(max_length=255, choices=(
        ("accepted", "ACCEPTED"), ("requested", "REQUESTED")))
    rel_distance = models.DecimalField(
        max_digits=15, decimal_places=10, null=True, blank=True, default=0)

    @staticmethod
    async def calculate_distance_async(lt1, ln1, lt2=0, ln2=0):
        # Approximate radius of earth in km
        R = 6373.0

        # lat1 = radians(52.2296756)
        # lon1 = radians(21.0122287)
        # lat2 = radians(52.406374)
        # lon2 = radians(16.9251681)

        lat1 = radians(lt1)
        lon1 = radians(ln1)
        lat2 = radians(lt2)
        lon2 = radians(ln2)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c

        print("Should be: ", distance, "km")

        return await round(distance, 8)

    async def save(self, *args, **kwargs):
        self.rel_distance = await self.calculate_distance_async(self.locationx, self.locationy)  # noqa
        await super(TruckModel, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.type} - {self.name}"

    class Meta:
        indexes = [
            models.Index(fields=['rel_distance'])
        ]
