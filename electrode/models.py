from django.db import models


class ElectrodeLabel(models.Model):
    label_name = models.CharField(max_length=255)

    def __str__(self):
        return self.label_name


class ElectrodeCategory(models.Model):
    label = models.ForeignKey(ElectrodeLabel, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.label.label_name} - {self.category_name}"


class Electrode(models.Model):
    label = models.ForeignKey(ElectrodeLabel, on_delete=models.CASCADE)
    category = models.ForeignKey(ElectrodeCategory, on_delete=models.CASCADE)
    package = models.IntegerField(default=0, blank=True, null=True)  # pachka
    box = models.IntegerField(default=0, blank=True, null=True)  # karobka
    weight = models.FloatField(default=0, blank=True, null=True)
    # count_by_label = models.IntegerField(default=0, blank=True, null=True)
    added_date = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.label.label_name