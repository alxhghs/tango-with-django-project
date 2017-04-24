import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page


def populate():
    # First we will create lists of dictionaries containing pages
    # we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories.
    # This might seem a little confusing, but it allows us to iterate
    # through each data structure, and add the data to our models.

    # List with 3 dictionaries
    python_pages = [
        {"title": "Official Python Tutorial",
         "url": "http://docs.python.org/2/tutorial"},
        {"title": "How to Think like a Computer Scientist",
         "url": "http://www.greenteapress.com/thinkpython/"},
        {"title": "Learn Python in 10 Minutes",
         "url": "http://www.korokithakis.net/tutorials/python/"}
    ]

    # List with 3 dictionaries
    django_pages = [
        {"title": "Official Django Tutorial",
         "url": "https://docs.djangoproject.com/en/1.9/intro/tutorial101/"},
        {"title": "Django Rocks",
         "url": "http://www.djangorocks.com"},
        {"title": "How to Tango with Django",
         "url": "http://www.tangowithdjango.com/"}
    ]

    # List with 2 dictionaries
    other_pages = [
        {"title": "Bottle",
         "url": "http://bottlepy.org/docs/dev/"},
        {"title": "Flask",
         "url": "http://flask.pocoo.org"}
    ]

    # Dictionary of dictionaries for the categories
    cats = {
        "Python":
            {"pages": python_pages,
             "views": 128,
             "likes": 64},
        "Django":
            {"pages": django_pages,
             "views": 64,
             "likes": 32},
        "Other Frameworks":
            {"pages": other_pages,
             "views": 32,
             "likes": 16},
    }

    # Iterate over the categories and the data in the categories to
    # add the category names and the pages to the database
    for cat, cat_data in cats.items():
        c = add_cat(cat, views=cat_data["views"], likes=cat_data["likes"])
        for p in cat_data["pages"]:
            add_page(c, p["title"], p["url"])

    # Print out the categories we have added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))


def add_page(cat, title, url, views=0):
    # the [0] is so that p = the first object only and not the bool
    # it will only create a new data entry if it didn't exist before
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p


# Creates a Category object and uses get_or_create to see if the data
# entry already exists using the name attribute. If it doesn't exist,
# then it creates a new object and then in the next line the function
# saves the new object and then returns it.
def add_cat(name, views, likes):
    # the [0] is so that c = the first object only and not the bool
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

# Start execution here!
if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()
