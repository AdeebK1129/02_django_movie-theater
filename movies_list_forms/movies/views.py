from django.shortcuts import render, redirect 
from django.http import JsonResponse
from .forms import MovieForm
import json

def get_cookie(request):
    movies = {}
    if 'movies' in request.COOKIES:
        try:
            movies = json.loads(request.COOKIES['movies'])
        except:
            pass
    return movies

def create_view(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movies = get_cookie(request)
            new_id = max(movies.keys(), default=0) + 1
            new_movie = form.cleaned_data
            new_movie['id'] = new_id
            movies[new_id] = new_movie
            response = redirect('list')
            response.set_cookie('movies', json.dumps(movies))
            return response
    else:
        form = MovieForm()
    return render(request, 'create_view.html', {'form': form})

def edit_view(request, movie_id):
    movies = get_cookie(request)
    movie = movies.get(movie_id, None)
    if request.method == 'POST' and movie:
        form = MovieForm(request.POST)
        if form.is_valid():
            movies[movie_id] = form.cleaned_data
            response = redirect('list')
            response.set_cookie('movies', json.dumps(movies))
            return response
    else:
        form = MovieForm(initial=movie)
    return render(request, 'edit_view.html', {'form': form, 'id': movie_id})

def list_view(request):
    movies = get_cookie(request)
    return render(request, 'list_view.html', {'movies': movies.values()})

def delete_view(request, movie_id):
    movies = get_cookie(request)
    if movie_id in movies:
        del movies[movie_id]
        response = redirect('list')
        response.set_cookie('movies', json.dumps(movies))
        return response
    return redirect('list')
