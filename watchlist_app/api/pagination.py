from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination, CursorPagination

class WatchListPagination(PageNumberPagination):
    page_size = 4
    page_query_param = 'page_num'  #control page param
    page_size_query_param ='size' #override the page_size
    max_page_size = 5
    last_page_strings = 'last'  #page/page_num=last

class WatchListLOPagination(LimitOffsetPagination):
    default_limit=2
    limit_query_param = 'page_limit' #overide limit
    offset_query_param = 'start' #overide offset
    max_limit =4

class WatchListCPagination(CursorPagination):
    page_size = 4
    ordering = 'title'