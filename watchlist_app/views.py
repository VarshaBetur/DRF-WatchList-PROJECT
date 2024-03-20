from django.shortcuts import render
from watchlist_app.models import Movie
from django.http import JsonResponse

# Create your views here.
def movie_list(request):
    movie_list=Movie.objects.all().values()  #converting to iterable object
    data={"Movies":list(movie_list)}
    return JsonResponse(data)  #the data should be dictionary

def movie_details(request,pk):
    movie=Movie.objects.get(id=int(pk))
    data={"name":movie.name,
          "description":movie.description,
          "active":movie.active
        }
    return JsonResponse(data)
