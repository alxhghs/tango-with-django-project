# rango/urls.py

from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm


def index(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary
    # that will be passed to the template engine.
    print("views.index called by urls.py")
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': page_list}
    return render(request, 'rango/index.html', context_dict)


def about(request):
    return render(request, 'rango/about.html')
    

def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass
    # to the template rendering engine.
    print("\nshow_category called by urls.py")
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an
        # exception.
        print("views.show_category - "
              "Category.objects.get(slug=category_name_slug)")
        category = Category.objects.get(slug=category_name_slug)
        print("category exists...")
        # Retrieve all of the associated pages.
        # Note that filter() will return a list of page objects or
        # an empty list.
        pages = Page.objects.filter(category=category)
        # Adds our results list to the template context under name
        # pages.
        context_dict['pages'] = pages
        # We also add the category object from
        # the database to the context dictionary.
        # We'll use this in the template to verify that the category
        # exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything -
        # the template will display the "no category" message for us.
        print("except Category.DoesNotExist...")
        context_dict['category'] = None
        context_dict['pages'] = None

    # Go render the response and return it to the client.
    print("return render(request, 'rango/category.html, context_dict)\n")
    return render(request, 'rango/category.html', context_dict)


def add_category(request):
    form = CategoryForm()
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        # Have we been provided a valid form?
        if form.is_valid():
            # Save the new category to the database
            print("Form is valid, returning index(request)...")
            cat = form.save(commit=True)
            form.save(commit=True)
            print("views.add_category printing category name and url slug - "
                  "name: {}, slug: {}".format(cat, cat.slug))
            # Now that the category is saved
            # we could give a confirmation message
            # But since the most recent category added is on the index page
            # Then we can direct the user back to the index page.
            return index(request)
        else:
            # The supplied form contained errors -
            # just print them to the terminal.
            print("Printing errors...")
            print(form.errors)
    # Will handle the bad for, new form or no form supplied cases
    # Render the form with error messages (if any)
    print("views.add_category returned render b/c request.method != 'POST' "
          "or there are errors")
    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)
