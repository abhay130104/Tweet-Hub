from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm, UserRegistrationForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

def main(request):
    return render(request, 'main.html')

def list_tweet(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'list_tweet.html', {'tweets': tweets})

@login_required
def create_tweet(request):
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit = False)
            tweet.user = request.user
            tweet.save()
            return redirect('list_tweet')
    else:
        form = TweetForm()
    return render(request, 'tweet_form.html', {'form':form})

@login_required
def edit_tweet(request, tweet_id):

    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)

    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit = False)
            tweet.user = request.user
            tweet.save()
            return redirect('list_tweet')

    else:
        form = TweetForm(instance=tweet)
    return render(request, 'tweet_form.html', {'form':form})

@login_required
def delete_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user = request.user)

    if request.method == "POST":
        tweet.delete()
        return redirect('list_tweet')
    return render(request, 'tweet_deleted_confirm.html', {'tweet':tweet})

def register(request):
     
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('list_tweet')
        
        else:
            form = UserRegistrationForm()

    form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form':form})

def search_view(request):
    query = request.GET.get('q', '')
    tweets = Tweet.objects.filter(text__icontains=query).order_by('-created_at')
    return render(request, 'search_results.html', {'tweets': tweets, 'query': query})

