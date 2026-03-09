from rest_framework import serializers
from maintenance import models

class maintenancePreventiveSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.MaintenancePreventive
        fields = [
                   "id","activite", "periode", "agent", "durree", "section", "equipement",
                    "etatMachine", "priorite", "coutPrevue", "modeOperatoire", 
                    "dateTimeNextIntervention", "dateTimeDemarrageComptage"
                ]
