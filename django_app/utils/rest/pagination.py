from rest_framework.pagination import PageNumberPagination


class Pagination10(PageNumberPagination):
    page_size = 10
