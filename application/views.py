import json
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_protect
import pandas as pd
import csv
from django.template import loader
from sklearn import preprocessing,svm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score,accuracy_score, explained_variance_score, d2_pinball_score, d2_tweedie_score
from sklearn.tree import DecisionTreeClassifier
from django.http import FileResponse,HttpResponse
import joblib
from io import StringIO
from django.contrib.auth import login,authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from application.models import Project
from django.contrib.auth.models import User

def index(request):
    return render(request, "index.html")


@login_required
def skills(request):
    return render(request, "skills.html")

def logout_request(request):
    logout(request)
    return render(request,"index.html")
result={}


def edit_project(request, id):

    
    template = loader.get_template('teaching.html')
    context={
            'myproject':Project.objects.get(pk=id),
    }
    
    return HttpResponse(template.render(context, request))

@csrf_protect
def teaching(request):
    global result
    
    result={}
    data={}
    if request.user.is_authenticated :
        user=User.objects.get(pk=request.user.id)
        project=Project.objects.get(name="Project"+str(user.id))
        if request.method =='POST':
            data = json.load(request)
            # print(data)
            body = data.get('payload')
            features= body['features']
            skill = body['skill']
            target = body['target']
            project.target=target
            project.skill=skill
            
            
            dataset= list(map(str.strip, body['file'].split('\r\n')))
            for x in dataset:
                dataset[dataset.index(x)]=list(map(str.strip, dataset[dataset.index(x)].split(',')))
            
            with open("data/dataset_"+project.name+".csv", "w") as file:
                writer = csv.writer(file)
                for element in dataset:
                    writer.writerow(element)
            
            for x in features:
                if x is None:
                    features.pop(features.index(x))
            project.features=listToString(features)
            dataset= open('data/data.csv','rb')
            project.dataset.save("dataset_"+project.name+".csv",dataset)
            project.save()
            
            dataset=pd.read_csv('data/data.csv')
            # TODO Clean data
            X=dataset[features]
            y=dataset[target]
            print(X)
            if skill == "simple-linear" :
                simplelinear(X,y,project.name)
            
            if skill == "multiple-linear-regression" :
                multiplelinear(X,y, project.name)

            if skill == "classification" :
                classification(X,y, project.name)
            
            model= open('data/model.pkl','rb')
            project.model.save("model_"+project.name+".pkl", model)
            project.save()
            return HttpResponse(json.dumps(result), content_type='application/json')
        if request.method == 'GET':
            return render(request, "teaching.html")
    else:
        return redirect("/login")

# Download the trained model
def downloadModel(request):
    model= open('data/model.pkl','rb')
    return FileResponse(model)

# User registration
def register_request(request):

    if request.user.is_authenticated:

        return redirect('/')
    if request.method == 'POST':

        form = UserCreationForm(request.POST)
        print(request.POST)
        print(form.is_valid())
        if form.is_valid():
            user=form.save()
            # username = request.POST['username']
            # password = request.POST['password1']

            # user = authenticate(username=username, password=password)
            Project.objects.create(name="Project"+str(user.id), user=user)
            login(request,user)
            return redirect('/')
        else:
            return render(request, 'register.html', {'form':form})
    else:
        form = UserCreationForm()

        return render(request, 'register.html', {'form':form})

def login_request(request):
    if request.method == "POST":
        form= AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password) 
            if user is not None:
                Project.objects.get_or_create(name="Project"+str(user.id), user=user)
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/skills')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    form = AuthenticationForm()
    return render(request=request, template_name='login.html', context={"login_form":form})

def get_projects_by_user(request):
    user=User.objects.get(pk=request.user.id)
    if request.method=="POST" and request.user.is_authenticated:
        if request.POST['name']:
            print(request.POST['name'])
            Project.objects.get_or_create(name=request.POST['name'],user=user)
            template = loader.get_template('projects.html')

            redirect("/projects")

    if request.user.is_authenticated:
        user=User.objects.get(pk=request.user.id)

        user_projects= user.projects.all()
        template = loader.get_template('projects.html')
        context={
            'myprojects':user_projects,
        }
        # return HttpResponse(user_projects)
        return HttpResponse(template.render(context, request))
    redirect('/login')

def cleanNaN(dataset:pd.DataFrame, mode="median"):

    if mode =="median":
        for column in dataset.colums:
            median=dataset[column].median()
            dataset[column].fillna(median, inplace=True)

def simplelinear(X,y,project_name,test_size=0.25):
    print("Working on simple linear regression")
    X_train, X_test, y_train, y_test=splitdata(X,y)
    
    simple_linear = LinearRegression() 
    
    simple_linear.fit(X_train,y_train)

    #Save model
    joblib.dump(simple_linear,"data/model_"+project_name+".pkl")

    y_predict = simple_linear.predict(X_test)

    result.update({"explained_variance_score":explained_variance_score(y_test,y_predict)})
    result.update({"pinball_score":d2_pinball_score(y_test,y_predict)})
    result.update({"d2_tweedie_score":d2_tweedie_score(y_test,y_predict)})

def multiplelinear(X,y,project_name,test_size=0.25):
    print("Working on multiple linear regression")
    X_train, X_test, y_train, y_test=splitdata(X,y)

    multipleRegression= LinearRegression()
    multipleRegression.fit(X_train,y_train)

    #Save model
    joblib.dump(multipleRegression,"data/model_"+project_name+".pkl")
    y_predict = multipleRegression.predict(X_test)
    print(y_predict)
    print(y_test)
    
    result.update({"explained_variance_score":explained_variance_score(y_test,y_predict)})
    result.update({"pinball_score":d2_pinball_score(y_test,y_predict)})
    result.update({"d2_tweedie_score":d2_tweedie_score(y_test,y_predict)})
    


def classification(X, y,project_name,test_size=0.25):
    print("Working on classification")
    X_train, X_test, y_train, y_test=splitdata(X,y)
    classifier=DecisionTreeClassifier()
    classifier.fit(X_train,y_train)
    joblib.dump(classifier,"data/model_"+project_name+".pkl")
    y_predict = classifier.predict(X_test)
    cm= confusion_matrix(y_test,y_predict)
    result.update({"precision":precision_score(y_test,y_predict)})
    result.update({"accuracy":accuracy_score(y_test,y_predict)})
    result.update({"recall":recall_score(y_test,y_predict)})
    

def splitdata(X,y,test_size=0.25):
    return train_test_split(X,y,test_size=test_size,random_state=0)

def listToString(array):
    string =' '.join([str(elem) for elem in array])

    
    return string
def newcsv(dataframe):

    with open("data/data.csv", "w") as file:
                writer = csv.writer(file)
                for element in dataframe:
                    writer.writerow(element)
