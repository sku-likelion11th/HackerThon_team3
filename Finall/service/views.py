from django.shortcuts import render
import urllib.request
import json
from django.core.paginator import Paginator, PageNotAnInteger

# Create your views here.
def main_page(request):
    return render(request, 'main/index.html')

def api_service_search(request):
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
        tag = request.GET.get('tag','')
        if search or tag:
            filtered_datas = []
            for data in datas:
                search_condition = search in data['지원대상'] or search in data['선정기준'] or search in data['서비스명']
                tag_condition = tag in data['서비스분야']
                if search_condition and tag_condition:
                    filtered_datas.append(data)
            datas = filtered_datas
        paginator = Paginator(datas,18)
        page = request.GET.get('page')
        datas = paginator.get_page(page)
        try:
            curPage = paginator.page(page)
        except PageNotAnInteger:
            page=1
            curPage = paginator.page(page)
        leftIndex = (int(page)-3)
        if leftIndex<1:
            leftIndex=1
        rightIndex = (int(page)+3)
        if rightIndex>paginator.num_pages:
            rightIndex=paginator.num_pages
        custom_range=range(leftIndex, rightIndex+1)
        return render(request, 'service/Benefit.html', {'datas' : datas, 'paginator': paginator, 'curPage': curPage, 'range': custom_range, 'search':search, 'tag':tag, 'page':page})
    else:
        return render(request, 'service/Benefit.html')