from django.http import JsonResponse
import requests


def dolar():
  url = "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=ir.cribillero@duocuc.cl&pass=Damelaapi88&firstdate=2024-05-01&timeseries=F073.TCO.PRE.Z.D&function=GetSeries"
    
  try:
    response = requests.get(url)
    response.raise_for_status()
    datos = response.json()
    valor = datos["Series"]["Obs"][-1]["value"]
    return valor
  except requests.exceptions.HTTPError as errh:
      return JsonResponse({'error': 'HTTP Error', 'message': str(errh)}, status=400)


def euro():
  url = "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=ir.cribillero@duocuc.cl&pass=Damelaapi88&firstdate=2024-05-01&timeseries=F072.CLP.EUR.N.O.D&function=GetSeries"
    
  try:
    response = requests.get(url)
    response.raise_for_status()
    datos = response.json()
    valor = datos["Series"]["Obs"][-1]["value"]
    return valor
  except requests.exceptions.HTTPError as errh:
      return JsonResponse({'error': 'HTTP Error', 'message': str(errh)}, status=400)