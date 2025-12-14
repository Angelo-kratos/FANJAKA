# from django.shortcuts import render,
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.urls import get_resolver
from rest_framework.permissions import IsAuthenticated
from maintenance import models


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
            if activite != "all":
                
                try:
                    activites = models.MaintenancePreventive.objects.filter(activite__istartswith = activite)
                    for act in activites:
                        lst_data.append(act)
                    
                    activites = models.MaintenancePreventive.objects.filter(activite__icontains = activite)
                    for act in activites:
                        if act not in lst_data:
                            lst_data.append(act)
                    data = act.activite
                except:
                    data = "Erreur de récuperation  d'activite dans DB!!"
            
                
        except:
            data = "Manque d'argument sur maintenance with filtering!!"
    
    else:
        data = "Method not allowed!!"
        
    return Response(data)
