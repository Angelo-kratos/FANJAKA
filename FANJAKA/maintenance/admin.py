from django.contrib import admin
from maintenance import models

tables = [
        models.Equipement, models.MaintenancePreventive, models.ModeOperatoire, models.Periode, models.Poste, models.Section
        ]

for table in tables:
    admin.site.register(table)


