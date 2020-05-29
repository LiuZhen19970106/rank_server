from django.http import HttpResponse
from django.shortcuts import render
from rank.models import UserInfo
import re

MIN = 1
MAX = UserInfo.objects.count()


def add_score(request, client_info):
    result = re.findall(r'client_nums=(.*?)&score=(.*)', client_info)
    client_nums = result[0][0]
    score = result[0][1]
    if UserInfo.objects.filter(client_nums=client_nums):
        queryset = UserInfo.objects.get(client_nums=client_nums)
        queryset.score = score
        queryset.save()
    else:
        UserInfo.objects.create(client_nums=client_nums, score=score)
    u_list = UserInfo.objects.all()
    return HttpResponse(u_list)


def show_rank(request, search_info):
    result = re.findall(r'client_nums=(.*?)&low_rank=(.*?)&high_rank=(.*)', search_info)
    client_nums = result[0][0]
    if result[0][1]:
        low_rank = int(result[0][1])
    else:
        low_rank = MIN
    if result[0][2]:
        high_rank = int(result[0][2])
    else:
        high_rank = MAX
    print(low_rank, high_rank)
    if not UserInfo.objects.filter(client_nums=client_nums):
        UserInfo.objects.create(client_nums=client_nums, score=0)
    rank_list = []
    queryset = UserInfo.objects.order_by('-score')
    rank = 1

    for info in queryset:
        rank_dic = {}
        if info.client_nums == client_nums:
            user_score = info.score
            user_rank = rank
        rank_dic["rank"] = rank
        rank_dic["client_nums"] = info.client_nums
        rank_dic["score"] = info.score
        rank_list.append(rank_dic)
        rank += 1
    rank_list = rank_list[low_rank - 1:high_rank]
    rank_dic = {}
    rank_dic["rank"] = user_rank
    rank_dic["client_nums"] = client_nums
    rank_dic["score"] = user_score
    rank_list.append(rank_dic)
    return render(request, 'rank.html', context={'rank_list': rank_list})
