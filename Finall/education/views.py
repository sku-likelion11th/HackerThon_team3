from django.shortcuts import render
import urllib.request
import json
import requests
import xml.etree.ElementTree as ET
from django.core.paginator import Paginator, PageNotAnInteger

# Create your views here.
def api_education_search(request):
    if request.method == "GET":
        with open('Finall/config.json') as json_file:
            config_data = json.load(json_file)
        client_educationKey = config_data["education"]["educationKey"]
        pageNo='1'
        numOfRows='200'
        url = 'http://apis.data.go.kr/B553701/SeominFinancialEducationContentsInfoService/getFinancialEducationContentsInfo'
        params ={'serviceKey' : client_educationKey, 'pageNo' : pageNo, 'numOfRows' : numOfRows }
        response = requests.get(url, params=params)
        rescode = response.status_code
        if rescode == 200:
            search = request.GET.get('search', '')
            tag = request.GET.get('tag', '')
            datas = response.text
            root = ET.fromstring(datas)
            datas = []
            for data in root.findall('body/items/item'):
                item_data = {}
                for child in data:
                    item_data[child.tag] = child.text
                datas.append(item_data)
            if search or tag:
                filtered_datas = []
                for data in datas:
                    search_condition = search in data['edcSbjcNm'] or search in data['edcSbjcIntrc'] or search in data['edcSmclsNm']
                    tag_condition = tag in data['edcSmclsNm']
                    if search_condition and tag_condition:
                        filtered_datas.append(data)
                datas = filtered_datas
            paginator = Paginator(datas, 18)
            page = request.GET.get('page')
            datas = paginator.get_page(page)
            try:
                curPage = paginator.page(page)
            except PageNotAnInteger:
                page = 1
                curPage = paginator.page(page)

            leftIndex = (int(page) - 3)
            if leftIndex < 1:
                leftIndex = 1

            rightIndex = (int(page) + 3)
            if rightIndex > paginator.num_pages:
                rightIndex = paginator.num_pages

            custom_range = range(leftIndex, rightIndex + 1)

        return render(request, 'education/Education.html', {'datas': datas, 'paginator': paginator, 'curPage': curPage, 'range': custom_range, 'page':page, 'search': search, 'tag': tag})
    else:
        return render(request, 'education/Education.html')