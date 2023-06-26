class CategoryServices:
    def find_categories(self):
        categories = ['buenas', 'tardes', 'que tal']
        return [{'category': c} for c in categories]