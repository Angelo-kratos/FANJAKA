# from django.shortcuts import render,
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.urls import get_resolver
from rest_framework.permissions import IsAuthenticated
from maintenance import models
from maintenance import serializers
from django.utils import timezone
from django.utils.dateparse import parse_datetime


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_urls(request):
    resolver = get_resolver()
    urls = []

    def explore(patterns, prefix=""):
        for entry in patterns:
            if hasattr(entry, "url_patterns"):  # include()
                explore(entry.url_patterns, prefix + str(entry.pattern))
            else:
                urls.append(prefix + str(entry.pattern))

    explore(resolver.url_patterns)

    # Filtrer : si l'app maintenance est déclarée sous "maintenance/"
    filtered = [u for u in urls if u.startswith("mnt")]

    return Response({"urls": filtered})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def maintenanceWithFiltering(request):
    
    """
        Maintenance with filtering
    """
    
    if request.method == "POST":
        
        try:
            
            activite = request.data.get("activite")
            periode = request.data.get("periode")
            agent = request.data.get("agent")
            equipement = request.data.get("equipement")
            section = request.data.get("section")
            
            lst_data = []
            lst_preventive = []
            if activite != "all" and len(activite) !=0:
                
                try:
                    activites = models.MaintenancePreventive.objects.filter(activite__istartswith = activite)
                    for act in activites:
                        lst_data.append(act)
                    
                    activites = models.MaintenancePreventive.objects.filter(activite__icontains = activite)
                    for act in activites:
                        if act not in lst_data:
                            lst_data.append(act)
                    
                except:
                    data = "Erreur de récuperation  d'activite dans DB!!"
            
        
            if periode != "all":
                try:
                    periode = models.Periode.objects.get(name=periode)
                    if periode:
                        try:
                            
                            if len(lst_data) == 0:
                                activites = models.MaintenancePreventive.objects.filter(periode=periode)
                                for act in activites:
                                    lst_data.append(act)
                            
                            else:
                                for preventive in lst_data:
                                    if preventive.periode != periode:
                                        lst_data.remove(preventive)
                            
                        except:
                            data ="Error to get activites dans DB!"
                except:
                    data = "Error to get this periode in DB!"
            
            
            if agent != "all":
                try:
                    agent = models.Poste.objects.get(name=agent)
                    if agent:
                        try:
                            
                            if len(lst_data) == 0:
                                activites = models.MaintenancePreventive.objects.filter(agent=agent)
                                for act in activites:
                                    lst_data.append(act)
                            
                            else:
                                for preventive in lst_data:
                                    if preventive.agent != agent:
                                        lst_data.remove(preventive)
                            
                        except:
                            data ="Error to get Agent dans DB!"
                except:
                    data = "Error to get this agent in DB!"
                    
                    
            if equipement != "all":
                try:
                    equipement = models.Equipement.objects.get(name=equipement)
                    if equipement:
                        try:
                            if len(lst_data) == 0:
                                activites = models.MaintenancePreventive.objects.filter(equipement=equipement)
                                for act in activites:
                                    lst_data.append(act)
                            
                            else:
                                for preventive in lst_data:
                                    if preventive.equipement != equipement:
                                        lst_data.remove(preventive)
                            
                        except:
                            data ="Error to get Equipement dans DB!"
                except:
                    data = "Error to get this equipement in DB!"
                    
            if section != "all":
                try:
                    section = models.Section.objects.get(name=section)
                    if section:
                        try:
                            
                            if len(lst_data) == 0:
                                activites = models.MaintenancePreventive.objects.filter(section=section)
                                for act in activites:
                                    lst_data.append(act)
                            
                            else:
                                for preventive in lst_data:
                                    if preventive.section != section:
                                        lst_data.remove(preventive)
                            
                        except:
                            data ="Error to get Section dans DB!"
                except:
                    data = "Error to get this section in DB!"
                    
            elif periode == "all" and len(activite) == 0 and agent == "all" and equipement == "all" and section == "all":
                activites = models.MaintenancePreventive.objects.all()
                for act in activites:
                    lst_data.append(act)
                    
            
            serializer = serializers.maintenancePreventiveSerializer(lst_data, many=True)
            print(serializer.data)
            
            preventives = serializer.data
            for data in preventives:
                
                data['periode'] = models.Periode.objects.get(id = data['periode']).name
                data['agent'] = models.Poste.objects.get(id = data['agent']).name
                data['section'] = models.Section.objects.get(id = data['section']).name
                data['equipement'] = models.Equipement.objects.get(id = data['equipement']).name
                modeOperatoire = models.ModeOperatoire.objects.get(id = data['modeOperatoire'])
                data['modeOperatoireTitle'] = modeOperatoire.name
                data['modeOperatoire'] = modeOperatoire.operation
                
        
        except:
            data = "Manque d'argument sur maintenance with filtering!!"
    
    else:
        data = "Method not allowed!!"
        
    return Response({
                    'status' : "succes",
                    'count' : len(preventives),
                    'data' : preventives
                    }                
                )


{
    
   "activite" : "",
    "periode" : "",
    "agent" : "",
    "durree" : "",
    "section" : "",
    "equipement" : "",
    "etatMachine" : "",
    "priorite" : "",
    "coutPrevue" : "",
    "modeOperatoire" : "",
    "dateTimeDemarrageComptage" : "",
    
}

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def addPreventive(request):
    
    """
        Ajouter du programme de preventive dans DB!!
    """
    
    if request.method == "POST":
        try:
            activite, priorite = request.data.get("activite"), request.data.get("priorite")
            periode, agent = request.data.get("periode"), request.data.get("agent")
            durree, etatMachine = request.data.get("durree"), request.data.get('etatMachine')
            section, equipement = request.data.get("section"), request.data.get("equipement")
            coutPrevue, modeOperatoire = request.data.get("coutPrevue"), request.data.get("modeOperatoire")
            dateTimeDemarrageComptage = request.data.get("dateTimeDemarrageComptage")
            
            if len(activite) != 0:
                if periode:
                    try:
                        periode = models.Periode.objects.get(name=periode)
                        
                        if periode:
                            try:
                                agent = models.Poste.objects.get(name=agent)
                                
                                if agent:
                                    try:
                                        section = models.Section.objects.get(name=section)

                                        if section:
                                            try:
                                                equipement = models.Equipement.objects.get(name=equipement)
                                                
                                                if equipement:
                                                    try:
                                                        modeOperatoire = models.ModeOperatoire.objects.get(name=modeOperatoire)
                                                        if modeOperatoire:
                                                            try:
                                                                priorite = int(priorite)
                                                                
                                                                if priorite:
                                                                    try:
                                                                        durree = float(durree)
                                                                        if durree:
                                                                            etatMachine = bool(durree)
                                                                            try:
                                                                                dt = parse_datetime(dateTimeDemarrageComptage)
                                                                                dateTimeDemarrageComptage = timezone.make_aware(dt)

                                                                                data = {
    
                                                                                            "activite" : activite,
                                                                                            "periode" : periode,
                                                                                            "agent" : agent,
                                                                                            "durree" : durree,
                                                                                            "section" : section,
                                                                                            "equipement" : equipement,
                                                                                            "etatMachine" : etatMachine,
                                                                                            "priorite" : priorite,
                                                                                            "coutPrevue" : coutPrevue,
                                                                                            "modeOperatoire" : modeOperatoire,
                                                                                            "dateTimeDemarrageComptage" : dateTimeDemarrageComptage,
                                                                                            
                                                                                        }
                                                                                    
                                                                                serializer = serializers.maintenancePreventiveSerializer(data=data)
                                                                                
                                                                            except:
                                                                                data = "Error on Date Demarrage!!"
                                                 
                                                                    except:
                                                                        data = "Error durree!!"
                                                            
                                                            except:
                                                                data = "Error priorite!!"
                                                    except:
                                                        data = "Error mode Operatoire!!"
                                            
                                            except:
                                                data = "Error equipement!!"
                                                
                                    except:
                                        data = "Error section!!"
                            
                            except:
                                data = "Error agent!!"
                    except:
                        data = "Error periode!"
        
        except:
            data = "Error on your request data!"
            