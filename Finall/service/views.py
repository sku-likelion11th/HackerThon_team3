from django.shortcuts import render
import urllib.request
import json
from django.core.paginator import Paginator, PageNotAnInteger

def main_page(request):
    return render(request, 'main/index.html')

# Create your views here.
def api_service_search(request):
    if request.method == "GET":
        with open('Finall/config.json') as json_file:
            config_data = json.load(json_file)
        client_key = config_data["service"]["serviceKey"]
        page = "5"
        perPage = "500"
        url = "https://api.odcloud.kr/api/gov24/v3/serviceList?page="+page+"&perPage="+perPage
        service_request = urllib.request.Request(url)
        service_request.add_header("Authorization","Infuser "+client_key)
        response = urllib.request.urlopen(service_request)
        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            result = json.loads(response_body.decode('utf-8'))
            datas = result.get('data')
            paginator = Paginator(datas, 20)
            page = request.GET.get('page')
            datas = paginator.get_page(page)
            try:
                curPage = paginator.page(page)
            except PageNotAnInteger:
                page = 1
                curPage = paginator.page(page)
            leftIndex = (int(page)-3)
            if leftIndex<1:
                leftIndex=1
            rightIndex = (int(page)+3)
            if rightIndex>paginator.num_pages:
                rightIndex=paginator.num_pages
            custom_range=range(leftIndex, rightIndex+1)
        return render(request, 'service/Benefit.html', {'datas' : datas, 'paginator':paginator, 'curPage': curPage, 'range': custom_range})
    else:
        return render(request, 'service/Benefit.html')

def search(request):
    with open('Finall/config.json') as json_file:
            config_data = json.load(json_file)
    client_key = config_data["service"]["serviceKey"]
    page = "5"
    perPage = "100"
    url = "https://api.odcloud.kr/api/gov24/v3/serviceList?page="+page+"&perPage="+perPage
    service_request = urllib.request.Request(url)
    service_request.add_header("Authorization","Infuser "+client_key)
    response = urllib.request.urlopen(service_request)
    rescode = response.getcode()
    if (rescode == 200):
        response_body = response.read()
        result = json.loads(response_body.decode('utf-8'))
        datas = result.get('data')
        search = request.GET.get('search','')
        if search:
            datas = [x for x in datas if (search in x['지원대상'] or search in x['선정기준'])]
            return render(request, 'service/Benefit.html', {'datas' : datas})
        return render(request, 'service/Benefit.html', {'datas' : datas})
    else:
        return render(request, 'service/Benefit.html')