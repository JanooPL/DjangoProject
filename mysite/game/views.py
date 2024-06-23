from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Game
from django.http import JsonResponse
from django.utils import timezone

#Rejestracja i logowanie oparte na domyślnym modelu User
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login_view")
    else:
        form = UserCreationForm()
    return render(request, "game/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("index")
    else:
        form = AuthenticationForm()
    return render(request, "game/login.html", {"form": form})

@login_required(login_url='/login')
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("login_view")
    
#Widok wszystkich gier
@login_required(login_url='/login')
def index(request):
    if request.method == 'POST':
        if 'create_room' in request.POST:  # Jeśli użytkownik chce stworzyć nowy pokój
            game = Game.objects.create()
            game.gamer1 = request.user
            game.save()
            return redirect('game_view', game_id=game.game_id)
        elif 'join_room' in request.POST:  # Jeśli użytkownik chce dołączyć do istniejącego pokoju
            game_id = request.POST['game_id']
            game = get_object_or_404(Game, game_id=game_id)
            if game.gamer1 != request.user and game.gamer2 != request.user:
                game.gamer2 = request.user
                game.save()
        
            return redirect('game_view', game_id=game_id)
    else:
        try:
            user = request.user    
            game_room = Game.objects.all().filter(Q(gamer1=user) | Q(gamer2=user) | Q(gamer1=None) | Q(gamer2=None))
        except:
            game_room = None
        return render(request, 'game/index.html', {'game_room': game_room})

#Moje gry
@login_required(login_url='/login')
def index_my_view(request):
    if request.method == "POST":
        game_id = request.POST['game_id']
        game = get_object_or_404(Game, game_id=game_id)
        game.delete()
        return redirect('index_my_view')
    else:
        try:    
            user = request.user
            game_room = Game.objects.all().filter(Q(gamer1=user) | Q(gamer2=user))
        except:
            game_room = None
        return render(request, 'game/index_my.html', {'game_room': game_room})

@login_required(login_url='/login')
def game_view(request, game_id):
    if request.method == 'POST':
        #wykonaj ruch
        if 'move' in request.POST:
            game = get_object_or_404(Game, game_id=game_id)
            position = request.POST['position']

            game.make_move(int(position)) #wywołanie metody w klasie modelu
            return redirect('game_view', game_id=game_id)
        else:
            # W przypadku innych formularzy POST zwróć błąd lub przekierowanie
            redirect('index_my_view')
        
    else:
        #wczytaj rozgrywkę
        game = get_object_or_404(Game, game_id=game_id)
        user = request.user
        
        if game.gamer1 == user or game.gamer2 == user:
            board = list(game.board)
            return render(request, 'game/game.html', {'game': game, 'board': board})
        else:
            redirect('index_my_view')
    
#reset stanu gry
@login_required(login_url='/login')
def reset_view(request, game_id):
    if request.method == 'POST':
        if 'reset' in request.POST:
            game = get_object_or_404(Game, game_id=game_id)
            game.reset()
            
            return redirect('game_view', game_id=game_id)

#wyjście z gry
@login_required(login_url='/login')
def out_view(request, game_id):
    if request.method == 'POST':
        if 'out' in request.POST:
            game = get_object_or_404(Game, game_id=game_id)
            user = request.user

            if game.gamer1 == user:
                game.gamer1 = None
            elif game.gamer2 == user:
                game.gamer2 = None
            game.save()
            
            if game.gamer1 is None and game.gamer2 is None:
                game.delete()

            return redirect(index)



@login_required(login_url='/login')
def check_game_changes(request, game_id):
    game = get_object_or_404(Game, game_id=game_id)
    last_checked_time = request.session.get('last_checked_time', None)
    
    if last_checked_time is None or timezone.datetime.fromisoformat(last_checked_time) < game.updated_at:
        request.session['last_checked_time'] = timezone.now().isoformat()
        return JsonResponse({'changes': True})
    else:
        return JsonResponse({'changes': False})