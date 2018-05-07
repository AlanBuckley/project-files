from django.shortcuts import render, HttpResponse, redirect
from fyp_project.forms import SignupForm, EditProfileForm
from django.contrib.auth.models import User
from fyp_project.models import Tweets, MLCache, CleanMessage, AuthUser
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate
from django.db.models import Count
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
import json

# Create your views here.
def login(request):
    return render(request, 'login.html')

def signup(request):
    if request.method =='POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return redirect('/fyp_project/')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})

def homepage(request):
    nosocialmediamessages = Tweets.objects.count()
    twitterTweets = Tweets.objects.all()[0:15]
    # load affective word counts
    context = RequestContext(request)

    cleanmessage = CleanMessage.objects.all()[:1]
    false_negatives = ''
    false_positives = ''
    precision = ''
    recall = ''
    true_negatives = ''
    true_positives = ''
    totalTweets = ''
    fScore = ''

    for a in cleanmessage:
        false_negatives = a.false_negatives
        false_positives = a.false_positives
        precision = a.precision
        recall = a.recall
        true_negatives = a.true_negatives
        true_positives = a.true_positives
        totalTweets = a.totalTweets
        fScore = a.fScore

    mlcache = MLCache.objects.all()[:1]
    affective_counts_cyberbullying_json = ''

    for x in mlcache:
        affective_counts_cyberbullying_json = x.affective_counts_cyberbullying_json

    affective_cyber_dict = json.loads(affective_counts_cyberbullying_json)

    affective_count_list_sadness = []
    affective_count_list_anticipation = []
    affective_count_list_disgust = []
    affective_count_list_positive = []
    affective_count_list_anger = []
    affective_count_list_joy = []
    affective_count_list_fear = []
    affective_count_list_trust = []
    affective_count_list_negative = []
    affective_count_list_surprise = []

    affective_count_list_sadness.append(affective_cyber_dict['sadness'])
    affective_count_list_anticipation.append(affective_cyber_dict['anticipation'])
    affective_count_list_disgust.append(affective_cyber_dict['disgust'])
    affective_count_list_positive.append(affective_cyber_dict['positive'])
    affective_count_list_anger.append(affective_cyber_dict['anger'])
    affective_count_list_joy.append(affective_cyber_dict['joy'])
    affective_count_list_fear.append(affective_cyber_dict['fear'])
    affective_count_list_trust.append(affective_cyber_dict['trust'])
    affective_count_list_negative.append(affective_cyber_dict['negative'])
    affective_count_list_surprise.append(affective_cyber_dict['surprise'])

    affective_cyber_count_list_sadness_str = ','.join(map(str, affective_count_list_sadness))
    affective_cyber_count_list_anticipation_str = ','.join(map(str, affective_count_list_anticipation))
    affective_cyber_count_list_disgust_str = ','.join(map(str, affective_count_list_disgust))
    affective_cyber_count_list_positive_str = ','.join(map(str, affective_count_list_positive))
    affective_cyber_count_list_anger_str = ','.join(map(str, affective_count_list_anger))
    affective_cyber_count_list_joy_str = ','.join(map(str, affective_count_list_joy))
    affective_cyber_count_list_fear_str = ','.join(map(str, affective_count_list_fear))
    affective_cyber_count_list_trust_str = ','.join(map(str, affective_count_list_trust))
    affective_cyber_count_list_negative_str = ','.join(map(str, affective_count_list_negative))
    affective_cyber_count_list_surprise_str = ','.join(map(str, affective_count_list_surprise))

    context_dict = {'affective_cyber_count_list_sadness_str': affective_cyber_count_list_sadness_str,'affective_cyber_count_list_anticipation_str': affective_cyber_count_list_anticipation_str,'affective_cyber_count_list_disgust_str': affective_cyber_count_list_disgust_str,'affective_cyber_count_list_positive_str': affective_cyber_count_list_positive_str,'affective_cyber_count_list_anger_str': affective_cyber_count_list_anger_str,'affective_cyber_count_list_joy_str': affective_cyber_count_list_joy_str,'affective_cyber_count_list_fear_str': affective_cyber_count_list_fear_str,'affective_cyber_count_list_trust_str': affective_cyber_count_list_trust_str,'affective_cyber_count_list_negative_str': affective_cyber_count_list_negative_str,'affective_cyber_count_list_surprise_str': affective_cyber_count_list_surprise_str, 'nosocialmediamessages': nosocialmediamessages, 'twitterTweets': twitterTweets,'false_negatives': false_negatives, 'false_positives':false_positives,'precision': precision, 'recall': recall, 'true_positives':true_positives, 'true_negatives': true_negatives, 'totalTweets': totalTweets, 'fScore': fScore}
    #context_dict2 = {}

    return render_to_response('homepage.html', context_dict)
    #return render(request, 'homepage.html', context_dict)
    #return render(request, 'homepage.html')

def Cyberbullying_info(request):
    return render(request, 'Cyberbullying_info.html')

def emotionalHealthInfo(request):
    return render(request, 'emotionalHealthInfo.html')

def about(request):
    return render(request, 'about.html')

def logout(request):
    return render(request, 'logout.html')

@login_required
def profile(request):
    args = {'user': request.user}
    return render(request, 'profile.html', args)

def runscript(request):
    if request.method == 'GET':
        form = TwitterHandle()
    else:
        if form.is_valid():
          info = request.POST['twitter_handle']
          output = script_function(twitter_handle)
          return render(request, 'homepage.html', {'twitter_handle': twitter_handle, 'output': output})
    return render(request, 'homepage.html', {'form': form})

    twitterhandle = AuthUser.objects.filter(username)

def script_function( post_from_form ):
    print (post_from_form) #//optional,check what the function received from the submit;
    return subprocess.call(["python", "/tweetloader.py"])
    return subprocess.check_call(['/tweetloader.py', post_from_form])

@login_required
def editProfile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save
            return redirect('/fyp_project/profile')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'editProfile.html', args)

@login_required
def changePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data = request.POST, user=request.user)

        if form.is_valid():
            form.save
            update_session_auth_hash(request, form.user)
            return redirect('/fyp_project/profile')
        else:
            return redirect('/fyp_project/changePassword')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}

        return render(request, 'changePassword.html', args)
