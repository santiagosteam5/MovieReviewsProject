from django.shortcuts import render
from .models import Movie
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

def home(request):
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm':searchTerm, 'movies':movies, 'name': 'Santiago Gomez'})

def about(request):
    return render(request, 'about.html')

def statistics_views(request):
    matplotlib.use('Agg')
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')
    genres = Movie.objects.values_list('genre', flat=True).distinct().order_by('genre')
    movie_counts_by_genres = {}
    movie_counts_by_year = {}
    for year in years:
        if year:
            movies_in_years = Movie.objects.filter(year=year)
        else:
            movies_in_years = Movie.objects.filter(year__isnull=True)
            year = "None"
        count = movies_in_years.count()
        movie_counts_by_year[year] = count

    for genre in genres:
        if genre:
            movie_by_genres = Movie.objects.filter(genre=genre)
        else:
            movie_by_genres = Movie.objects.filter(genre__isnull=True)
            genre = "None"
        count = movie_by_genres.count()
        movie_counts_by_genres[genre] = count

    bar_width = 0.5
    bar_spacing = 0.5
    bar_positions = range(len(movie_counts_by_year))

    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')

    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    bar_positions_g = range(len(movie_counts_by_genres))

    plt.bar(bar_positions_g, movie_counts_by_genres.values(), width=bar_width, align='center')

    plt.title('Movies per genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions_g, movie_counts_by_genres.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)
    bufferg = io.BytesIO()
    plt.savefig(bufferg, format='png')
    bufferg.seek(0)
    plt.close()

    imagegenre_png = bufferg.getvalue()
    bufferg.close()
    graphicg = base64.b64encode(imagegenre_png)
    graphicg = graphicg.decode('utf-8')

    return render(request, 'statistics.html', {'graphig':graphic})

