from .models import Technology, Saved


class DataMixin:
    def get_saves_data(self, email, show_cat):
        saved = Saved.objects.filter(email=email).values_list("detail_id", flat=True)
        technology = Technology.objects.filter(lang__slug=show_cat).select_related('lang')
        show_cat = show_cat
        context = {'technology': technology,
                   'saved': saved,
                   'show_cat': show_cat}
        return context