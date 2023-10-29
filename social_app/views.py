from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import TrigramSimilarity
import random
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
# Create your views here.


def log_out(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER'))
