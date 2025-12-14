from django.db import models

# Create your models here.


class Periode(models.Model):

    """
        Class des periodes des maintenances
    """

    name = models.CharField(max_length=35, blank=False)

    def __str__(self):
        return self.name
    

class Poste(models.Model):

    """
        Class poste(agents) pour maintenance!
    """

    name = models.CharField(max_length=30, blank=False)
    
    def __str__(self):
        return self.name


class Section(models.Model):
    
    """
        Class des setions dispo dans l'usine!
    """
    
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name
    

class Equipement(models.Model):
    
    """
        Class des équipements!
    """
    
    name = models.CharField(max_length=30, blank=False)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="EquipementSections")
    
    def __str__(self):
        return self.name



class ModeOperatoire(models.Model):
    
    """
        Class pour les mode opératoires!
    """
    
    name = models.CharField(max_length=100)
    opération = models.TextField()
    
    def __str__(self):
        return self.name



class MaintenancePreventive(models.Model):
    
    """
        Models pour les maintenances préventives!
    """
    
    activite = models.CharField(max_length=200, blank=False, null=False)
    periode = models.ForeignKey(Periode, on_delete=models.CASCADE, related_name="periodes")
    agent = models.ForeignKey(Poste, on_delete=models.CASCADE, related_name="agents")
    durree = models.FloatField(blank=False, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="sections")
    equipement = models.ForeignKey(Equipement, on_delete=models.CASCADE, related_name="equipements")
    etatMachine = models.BooleanField(default=0)
    priorite = models.IntegerField()
    coutPrevue = models.CharField(max_length=15)
    modeOperatoire = models.ForeignKey(ModeOperatoire, on_delete=models.CASCADE, related_name="modeOperatoires")
    dateTimeCreation = models.DateTimeField(auto_now=True)
    dateTimeDemarrageComptage = models.DateTimeField(null=True)
    dateTimeNextIntervention = models.DateTimeField(null=True)
    
    def __str__(self):
        return self.activite
    