from django.contrib import admin
from watchlist_app.models import Movie, StreamPlatform, WatchList, Review
# Register your models here.
# admin.site.register(Movie)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ["name","active"]

admin.site.register(WatchList)
admin.site.register(StreamPlatform)
admin.site.register(Review)