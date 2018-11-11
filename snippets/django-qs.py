from rest_framework import viewsets

class BlogpostViewSet(viewsets.ModelViewSet):
    # queryset = Blogpost.objects.all().order_by('date')
    serializer_class = serializers.BlogpostSerializer

    def get_queryset(self):
        # Chances are, you're doing something more advanced here 
        # like filtering.
        Blogpost.objects.all().order_by('date')

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        qs = self.get_queryset()
        all_categories = Category.objects.filter(
            id__in=Blogpost.categories.through.objects.filter(
                blogpost__in=qs
            ).values('category_id')
        )
        category_names = {}
        for category in all_categories:
            category_names[category.id] = category.name

        categories_map = defaultdict(list)
        for m2m in Blogpost.categories.through.objects.filter(blogpost__in=qs):
            categories_map[m2m.blogpost_id].append(
                category_names[m2m.category_id]
            )

        for each in response.data:
            each['categories'] = categories_map.get(each['id'], [])

        return response