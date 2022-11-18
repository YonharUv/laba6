from .models import Article
from django.shortcuts import render
from django.http import Http404
from django.shortcuts import redirect  
from django.contrib.auth.models import User 
from django.contrib.auth import login, logout, authenticate

def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
        raise Http404

def archive(request):
    return render(request, 'archive.html', {"posts": Article.objects.all()})

def create_post(request):
    if not request.user.is_anonymous:
        if request.method == "POST":
        # обработать данные формы, если метод POST
            form = {
                'text': request.POST["text"], 'title': request.POST["title"]
            }
        # в словаре form будет храниться информация, введенная пользователем
            if form["text"] and form["title"]:
                if  Article.objects.filter(title = form['title']).exists():
                        form['errors'] = u"Статья с таким именем уже есть"
                        return render(request, 'new.html', {'form': form})
                else:
                    Article.objects.create(text=form["text"], title=form["title"], author=request.user)
                    return redirect('archive')
            else:
        # если введенные данные некорректны
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'new.html', {'form': form})
        else:
        # просто вернуть страницу с формой, если метод GET
            return render(request, 'new.html', {})
    else:
        raise Http404

def add_user(request):
    if request.method == "POST":
        form = {
            'usr': request.POST["usr"],
            'email': request.POST["email"], 
            'passwd': request.POST["passwd"]
        }
        if form["usr"] and form["email"] and form["passwd"]:
            try:
                User.objects.get(username = form['usr'])
                User.objects.get(email=form['email'])
                form['errors'] = u"Пользователем с таким именем или почтой уже есть"
                return render(request, 'add_user.html', {'form': form})
            except User.DoesNotExist:
                User.objects.create_user(form['usr'], form['email'], form['passwd'])
                login(request, authenticate(request, username=form['usr'], password=form['passwd']))
                return redirect('archive')

        else:
            form['errors'] = u"Не все поля заполнены"
        return render(request, 'add_user.html', {'form': form})
    else:
        return render(request, 'add_user.html', {})

def logout_user(request):
    logout(request)
    return redirect('archive')

def login_user(request):
    if request.method == "POST":
        form = {
            'usr': request.POST['usr'],
            'passwd': request.POST['passwd']
        }
        if form['usr'] and form['passwd']:
            user = authenticate(username=form['usr'], password=form['passwd'])
            if user is None:
                form['error'] = u'Такого пользователя не существует'
                return render(request, 'login.html', {'form': form})
            else:
                login(request, user)
                return redirect('archive')
        else:
            form['errors'] = u'Не все поля заполнены'
            return render(request, 'login.html', {'form': form})
    else:
        return render(request, 'login.html', {})