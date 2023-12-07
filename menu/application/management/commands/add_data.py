from django.core.management.base import BaseCommand
from menu.application.models import Menu, MenuItem


class Command(BaseCommand):
    help = 'Сommand to download the data to database'

    def handle(self, *args, **kwargs):
        menu1 = Menu.objects.create(title='menu1', slug='menu1')
        menu2 = Menu.objects.create(title='menu2', slug='menu2')

        parent1 = MenuItem.objects.create(title='menu 1 category 1', slug='menu1_cat1', menu=menu1)
        MenuItem.objects.create(title='menu 1 category 1 subcategory 1', slug='menu1_cat1_sub1', menu=menu1,
                                parent=parent1)
        MenuItem.objects.create(title='menu 1 category 1 subcategory 2', slug='menu1_cat1_sub2', menu=menu1,
                                parent=parent1)

        parent2 = MenuItem.objects.create(title='menu 1 category 2', slug='menu1_cat2', menu=menu1)
        MenuItem.objects.create(title='menu 1 category 2 subcategory 1', slug='menu1_cat2_sub1', menu=menu1,
                                parent=parent2)
        MenuItem.objects.create(title='menu 1 category 2 subcategory 2', slug='menu1_cat2_sub2', menu=menu1,
                                parent=parent2)

        parent3 = MenuItem.objects.create(title='menu 2 category 1', slug='menu2_cat1', menu=menu2)
        MenuItem.objects.create(title='menu 2 category 1 subcategory 1', slug='menu2_cat1_sub1', menu=menu2,
                                parent=parent3)

        MenuItem.objects.create(title='menu 2 category 2', slug='menu2_cat2', menu=menu2)

        self.stdout.write('Done')
