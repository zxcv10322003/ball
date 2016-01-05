from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from baseball.models import Category, Page
from baseball.forms import CategoryForm, PageForm
from django.contrib.auth.decorators import login_required
# Create your views here.
def baseball(request):
    categories = Category.objects.order_by('-likes')
    context = {'categories':categories}
    return render(request, 'baseball/baseball.html',context)


def category(request, categoryID):
    context = {}
    try:
        category = Category.objects.get(id=categoryID)
        context['category'] = category
        context['pages'] = Page.objects.filter(category=category)
    except Category.DoesNotExist:
        pass
    return render(request, 'baseball/category.html', context)

@login_required
def addCategory(request):
    template = 'baseball/addCategory.html'
    if request.method=='GET':
        return render(request, template, {'form':CategoryForm()})
    # request.method=='POST'
    form = CategoryForm(request.POST)
    if not form.is_valid():
        return render(request, template, {'form':form})
    form.save()
    return redirect(reverse('baseball:baseball'))
# Or try this: return baseball(request)
 
@login_required
def addPage(request, categoryID):
    template = 'baseball/addPage.html'
    try:
        pageCategory = Category.objects.get(id=categoryID)
    except Category.DoesNotExist:
        return category(request, categoryID)
    context = {'category':pageCategory}
    if request.method=='GET':
        context['form'] = PageForm()
        return render(request, template, context)
    # request.method=='POST'
    form = PageForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, template, context)
    page = form.save(commit=False)
    page.category = pageCategory
    page.save()
    return redirect(reverse('baseball:category', args=(categoryID, )))

@login_required
def deleteCategory(request, categoryID):
    if request.method!='POST':
        return baseball(request)
    # request.method=='POST':
    categoryToDelete = Category.objects.get(id=categoryID)
    if categoryToDelete:
        categoryToDelete.delete()
    return redirect(reverse('baseball:baseball'))

@login_required
def deletePage(request, pageID):
    if request.method!='POST':
        return baseball(request)
    # request.method=='POST':
    pageToDelete = Page.objects.get(id=pageID)
    if pageToDelete:
        categoryID = pageToDelete.category.id
        pageToDelete.delete()
    else:
            categoryID = ''
    return redirect(reverse('baseball:category', args=(categoryID, )))

@login_required
def updateCategory(request, categoryID):
    template = 'baseball/updateCategory.html'
    try:
        category = Category.objects.get(id=categoryID)
    except Category.DoesNotExist:
        return baseball(request)
    if request.method=='GET':
        form = CategoryForm(instance=category)
        return render(request, template, {'form':form, 'category':category})
    # request.method=='POST'
    form = CategoryForm(request.POST, instance=category)
    if not form.is_valid():
        return render(request, template, {'form':form, 'category':category})
    form.save()
    return redirect(reverse('baseball:baseball'))

@login_required
def updatePage(request, pageID):
    template = 'baseball/updatePage.html'
    try:
        page = Page.objects.get(id=pageID)
    except Page.DoesNotExist:
            return category(request, '')
    if request.method=='GET':
            form = PageForm(instance=page)
            return render(request, template, {'form':form, 'page':page})
    # request.method=='POST'
    form = PageForm(request.POST, instance=page)
    if not form.is_valid():
        return render(request, template, {'form':form, 'page':page})
    form.save()
    return redirect(reverse('baseball:category', args=(page.category.id,)))