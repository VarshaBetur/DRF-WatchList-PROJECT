from rest_framework.response import Response
from watchlist_app.models import Movie, WatchList, StreamPlatform, Review
from watchlist_app.api.serializers import MovieSerializers, WatchListSerializers, StreamPlatformSerializers, ReviewSerializers
from watchlist_app.api.permissions import AdminOrReadOnly, IsReviewUserOrReadOnly
from watchlist_app.api.throttling import ReviewCreateThrottle, ReviewListThrottle
from watchlist_app.api.pagination import WatchListPagination,WatchListLOPagination,WatchListCPagination
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle,ScopedRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


from rest_framework.views import APIView


# Function Base Views
# @api_view(['GET','POST'])
# def movie_list(request):
#     if request.method=='GET':
#         movie_list=Movie.objects.all()
#         serializer = MovieSerializers(movie_list,many=True)            #serialize the data
#         return Response(serializer.data)
#
#     if request.method == 'POST':
#         serializer = MovieSerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET','PUT','DELETE'])
# def movie_details(request,pk):
#     try:
#         movie = Movie.objects.get(id=int(pk))
#     except Movie.DoesNotExist:
#         return Response({"error":"Movie Not Found"}, status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         serializer = MovieSerializers(movie)  # serialize the data
#         return Response(serializer.data)
#     if request.method == 'PUT':
#         serializer = MovieSerializers(movie,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)
#     if request.method == 'DELETE':
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


#Class Base Views
class MovieListView(APIView):
    def get(self,request):
        movie_list = Movie.objects.all()
        serializer = MovieSerializers(movie_list,many=True)            #serialize the data
        return Response(serializer.data)

    def post(self,request):
        serializer = MovieSerializers(data=request.data)  # serialize the data
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class MovieDetailsView(APIView):
    def get(self,request,pk):
        try:
            movie = Movie.objects.get(id=int(pk))
        except Movie.DoesNotExist:
            return Response({"error":"Movie Not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = MovieSerializers(movie)  # serialize the data
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request,pk):
        try:
            movie = Movie.objects.get(id=int(pk))
        except Movie.DoesNotExist:
            return Response({"error":"Movie Not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = MovieSerializers(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk):
        try:
            movie = Movie.objects.get(id=int(pk))
        except Movie.DoesNotExist:
            return Response({"error": "Movie Not Found"}, status=status.HTTP_404_NOT_FOUND)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 2. one api for movie detail, the platform name, the average rating
class WatchListView(APIView):
    permission_classes=[AdminOrReadOnly,]

    def get(self,request):
        watch_list = WatchList.objects.all()
        serializer = WatchListSerializers(watch_list,many=True)            #serialize the data
        return Response(serializer.data)

    def post(self,request):
        serializer = WatchListSerializers(data=request.data)  # serialize the data
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#to test filter
class WatchList(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializers
    permission_classes = [IsAuthenticated]
    # pagination_class = WatchListPagination
    # pagination_class = WatchListLOPagination
    pagination_class = WatchListCPagination


    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['platform__name']  #search for exact match ?platform__name=

    # filter_backends = [filters.SearchFilter]
    # search_fields = ['^title','=platform__name'] #search=1

    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['avg_rating']

# 3. one api for list of all the ratings for a particular movie
class WatchListDetailsView(APIView):
    permission_classes = [AdminOrReadOnly]
    def get(self,request,pk):
        try:
            watch_list = WatchList.objects.get(id=int(pk))
        except Movie.DoesNotExist:
            return Response({"error":"WatchList Not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializers(watch_list)  # serialize the data
        return Response(serializer.data,status=status.HTTP_200_OK)


    def put(self,request,pk):
        try:
            watch_list = WatchList.objects.get(id=int(pk))
        except Movie.DoesNotExist:
            return Response({"error":"WatchList Not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializers(watch_list, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk):
        try:
            watch_list = WatchList.objects.get(id=int(pk))
        except Movie.DoesNotExist:
            return Response({"error": "WatchList Not Found"}, status=status.HTTP_404_NOT_FOUND)
        watch_list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#6. User can search a movie by there name
# class SearchWatchListView(APIView):
#     def get(self,request,movie_name):
#         try:
#             watch_list = WatchList.objects.get(title=movie_name)
#         except Movie.DoesNotExist:
#             return Response({"error":"WatchList Not Found"}, status=status.HTTP_404_NOT_FOUND)
#         serializer = WatchListSerializers(watch_list)  # serialize the data
#         return Response(serializer.data,status=status.HTTP_200_OK)

# #5. User can filter the movies according to the ratings
# class FilterBasedOnRatingView(APIView):
#     def get(self, request, rating):
#         watch_list = WatchList.objects.all()
#         new_watch_list=[]
#         for movie in watch_list:
#             reviews_list=movie.reviews.all().values_list("rating", flat=True)
#             if len(reviews_list) >0:
#                 average_rating = sum(reviews_list) / len(reviews_list)
#                 if average_rating < rating:
#                     watch_list=watch_list.exclude(id=movie.id)
#             else:
#                 watch_list=watch_list.exclude(id=movie.id)
#         serializer = WatchListSerializers(watch_list, many=True)  # serialize the data
#         return Response(serializer.data)

#demo
#1 normal user can only create and update there ratings on the movie
#4. User can create, update there ratings
# class ReviewViews(APIView):
#     def post(self,request):
#         serializer = ReviewSerializers(data=request.data)  # serialize the data
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#
#     def put(self,request,pk):
#         try:
#             review = Review.objects.get(id=int(pk))
#         except Movie.DoesNotExist:
#             return Response({"error":"Review Not Found"}, status=status.HTTP_404_NOT_FOUND)
#         serializer = ReviewSerializers(review, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_200_OK)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class StreamPlatformView(APIView):
    permission_classes = [AdminOrReadOnly]
    def get(self, request):
        platforms=StreamPlatform.objects.all()
        serializer= StreamPlatformSerializers(platforms, many=True,context={'request': request})
        return Response(serializer.data)

    def post(self,request):
        serializer = StreamPlatformSerializers(data=request.data)  # serialize the data
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class StreamPlatformDetailsView(APIView):
    permission_classes = [AdminOrReadOnly]
    def get(self,request,pk):
        try:
            platform = StreamPlatform.objects.get(id=int(pk))
        except Movie.DoesNotExist:
            return Response({"error":"platform Not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializers(platform)  # serialize the data
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request,pk):
        try:
            platform = StreamPlatform.objects.get(id=int(pk))
        except Movie.DoesNotExist:
            return Response({"error":"platform Not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializers(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk):
        try:
            platform = StreamPlatform.objects.get(id=int(pk))
        except Movie.DoesNotExist:
            return Response({"error": "platform Not Found"}, status=status.HTTP_404_NOT_FOUND)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#using viewset
# class StreamPlatformViewSet(viewsets.ViewSet):
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializers(queryset, many=True)
#         return Response(serializer.data)
#
#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializers(watchlist)
#         return Response(serializer.data)
#using viewset
# ReadOnlyModelViewSet--allow us to just see the value(only GET and List method)
class StreamPlatformViewSet(viewsets.ModelViewSet):
    permission_classes = [AdminOrReadOnly]
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializers

#drf
#using Mixins and Generic View
#mixins are popular to perform common task we just need to provide basing setting

#using mixins
# class ReviewDetails(mixins.RetrieveModelMixin,
#                     generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializers
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#
# class ReviewList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializers
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


#using genericviews
class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializers
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]

    def get_queryset(self):
        return Review.objects.all()
    def perform_create(self, serializer):
        pk = self.kwargs["pk"]
        watch_list=WatchList.objects.get(id=pk)

        user=self.request.user
        review_queryset = Review.objects.filter(watchlist=watch_list, reviewer=user)
        if review_queryset.exists():
            raise ValidationError("you have already Reviewed this watchlist!")


        if watch_list.number_rating ==0:
            watch_list.avg_rating = serializer.validated_data["rating"]
        else:
            watch_list.avg_rating = (watch_list.avg_rating+serializer.validated_data["rating"])/2
        watch_list.number_rating = watch_list.number_rating+1
        watch_list.save()

        serializer.save(watchlist=watch_list, reviewer=user)


class ReviewList(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewListThrottle]

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Review.objects.filter(watchlist=pk)

class ReviewDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    permission_classes = [IsReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'


class UserReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['reviewer__username', 'active']

    def get_queryset(self):
        user = self.kwargs["username"]
        return Review.objects.filter(reviewer__username=user)