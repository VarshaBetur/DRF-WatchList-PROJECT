from django.urls import path, include

# from watchlist_app.api.views import movie_list,movie_details


from watchlist_app.api.views import (
    MovieDetailsView,
    MovieListView,
    StreamPlatformView,
    WatchListView,
    WatchListDetailsView,
    StreamPlatformDetailsView,
    ReviewList,
    ReviewDetails,
    ReviewCreate,
    StreamPlatformViewSet,
    UserReviewList,
    WatchList
)
from rest_framework.routers import DefaultRouter
# from watchlist_app.api.views import FilterBasedOnRatingView,SearchWatchListView, ReviewViews

router = DefaultRouter()
router.register('streamplatform',StreamPlatformViewSet,basename='streamplatform')
urlpatterns = [
    # function based view
    # path("list/", movie_list, name="movie-list"),
    # path("<int:pk>", movie_details, name="movie-details"),


    # class based view
    path("list/", MovieListView.as_view(), name="movie-list"),
    path("<int:pk>", MovieDetailsView.as_view(), name="movie-details"),

    path("new-list/", WatchList.as_view(), name="watchlist"),
    path("watch-list/", WatchListView.as_view(), name="watch-list"),
    path("watch-list-details/<int:pk>/", WatchListDetailsView.as_view(), name="watch-list-details"),
    # path("search-watch-list/<str:movie_name>/", SearchWatchListView.as_view(), name="search-watch-list-by-name"),

    path('',include(router.urls)),
    path("stream/", StreamPlatformView.as_view(), name="stream-list"),
    path("stream/<int:pk>/", StreamPlatformDetailsView.as_view(), name="streamplatform-detail"),

    #demo urls
    # path("create-review/",ReviewViews.as_view(),name="create_review"),
    # path("update-review/<int:pk>",ReviewViews.as_view(),name="update_review"),
    # path("rating-based-filter/<int:rating>",FilterBasedOnRatingView.as_view(),name="filter-based-on-rating")

    # path("review/", ReviewList.as_view(),name="review-list"),
    # path("review/<int:pk>", ReviewDetails.as_view(),name="review-details"),

    path("<int:pk>/review-create/", ReviewCreate.as_view(),name="review-create"),
    path("<int:pk>/review/", ReviewList.as_view(),name="review-list"), #all the reviews for a particular movie
    path("review/<int:pk>/", ReviewDetails.as_view(),name="review-details"), #fetch particular review
    path("review/<str:username>/", UserReviewList.as_view(),name="user-review-list")


]