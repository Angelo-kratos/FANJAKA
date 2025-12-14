from rest_framework import serializers
from maintenance import models

class maintenancePreventiveSerializer(serializers.Serializer):
    
    class Meta:
        model = models.MaintenancePreventive
        fields = [
                    "activite", "periode", "agent", "durree", "section", "equipement",
                    "etatMachine", "priorite", "coutPrevue", "modeOperatoire", 
                    "dateTimeNextIntervention", "dateTimeDemarrageComptage"
                ]
