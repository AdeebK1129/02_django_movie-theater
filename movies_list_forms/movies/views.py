from django.shortcuts import render, redirect 
from django.http import JsonResponse
from .forms import MovieForm
from django.contrib import messages
from core.templatetags.core_extras import get_value_from_dict
import json

def get_cookie_data(request):
    movies = {}
    if 'movie_data' in request.session:
        try:
            movies = json.loads(request.session['movie_data'])
        except json.JSONDecodeError:
            pass
    return movies

def create_view(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movies = get_cookie_data(request)
            print(movies)
            new_id = int(max(movies.keys(), default=0)) + 1
            print(new_id)
            new_movie = form.cleaned_data
            print(new_movie)
            new_movie['id'] = new_id

            if any(movie['name'].lower() == new_movie['name'].lower() for movie in movies.values()):
                messages.error(request, 'Movie with the same name already exists.')
                return redirect('movies:create_view')

            movies[new_id] = new_movie
            request.session['movie_data'] = json.dumps(movies)
            messages.success(request, 'Movie created successfully.')
            return redirect('movies:list_view')
    else:
        form = MovieForm()
    return render(request, 'movies/create_view.html', {'form': form})

def edit_view(request, movie_id):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movies = get_cookie_data(request)
            print(movies)
            print(movie_id)
            new_movie = form.cleaned_data
            print(new_movie)
            new_movie['id'] = movie_id

            if any(movie['name'].lower() == new_movie['name'].lower() for movie in movies.values()):
                messages.error(request, 'Movie with the same name already exists.')
                return redirect('movies:edit_view')

            movies[movie_id] = new_movie
            request.session['movie_data'] = json.dumps(movies)
            messages.success(request, 'Movie edited successfully.')
            return redirect('movies:list_view')
    else:
        form = MovieForm()
    return render(request, 'movies/create_view.html', {'form': form})

def list_view(request):
    movies = get_cookie_data(request)
    movies_with_valid_ids = [movie for movie in movies.values() if isinstance(movie.get('id'), int)]
    return render(request, 'movies/list_view.html', {'movies': movies_with_valid_ids})

def delete_view(request, movie_id):
    if request.method == 'POST':
        movies = get_cookie_data(request)
        if str(movie_id) in movies:
            del movies[str(movie_id)]
            request.session['movie_data'] = json.dumps(movies)
            messages.success(request, 'Movie deleted successfully.')
            return redirect('movies:list_view')
        else:
            messages.error(request, 'Movie not found.')
            return redirect('movies:list_view')