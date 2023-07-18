from rest_framework.filters import BaseFilterBackend

class MinFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        min_id = request.query_params.get('min_id')
        if min_id:
            return queryset.filter(id__lt=min_id).order_by('-id')
        return queryset

class MaxFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        max_id = request.query_params.get('max_id')
        if max_id:
            return queryset.filter(id__gt=max_id).order_by('id')
        return queryset
