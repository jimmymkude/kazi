from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from .forms import UserForm, UserLoginForm
from .models import Post, User
from .serializers import PostSerializer


# Create your views here.


def logout_view(request):
    logout(request)
    return redirect('ajira:index')


class IndexView(generic.ListView):
    template_name = 'ajira/index.html'
    context_object_name = 'posts_list'

    def get(self, request):
        user = request.user
        if user.is_authenticated():
            return render(request, self.template_name, {'user': user})

        return render(request, self.template_name, {self.context_object_name: Post.objects.all()})


    def get_queryset(self):
        """
        :return: A list of posts to be displayed
        """
        return Post.objects.all()


class PostDetailView(generic.DetailView):
    model = Post
    template_name ='ajira/detail.html'
    context_object_name = 'post'


class PostCreateView(generic.CreateView):
    model = Post
    fields = ['image', 'title', 'description', 'link', 'company', 'lifetime_in_days']

    def form_valid(self, form):
        post = form.instance
        # get the signed in user's primary key

        post.user = get_object_or_404(User, pk=3)
        self.object = form.save()
        return HttpResponseRedirect(reverse('ajira:detail', args=(post.id,)))


# Sign up form
class UserFormView(generic.View):
    form_class = UserForm
    template_name = 'ajira/registration_form.html'

    # display blank form for user to sign up on
    def get(self, request):
        form = self.form_class(data=None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # cleaned (normalized) data
            username = form.cleaned_data['username']
            user.username = username
            user.email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # returns User object if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:
                # if user's account did not get banned or disabled
                if user.is_active:
                    login(request, user)
                    #request.user.username
                    return redirect('ajira:index')

        return render(request, self.template_name, {'form': form})


class UserLoginFormView(generic.View):
    form_class = UserLoginForm
    template_name = "ajira/login_form.html"

    # display blank form for user to sign in
    def get(self, request):
        form = self.form_class(data=None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(data=request.POST)

        username = request.POST['username']
        password = request.POST['password']

        # returns User objects if credentials are correct
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # if user's account did not get banned or disabled
            if user.is_active:
                login(request, user)
                # request.user.username
                return redirect('ajira:index')

        return render(request, self.template_name, {'form': form})


class AboutPageView(generic.TemplateView):
    template_name = "ajira/about.html"


# api/posts
class PostAPIView(APIView):

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self):
        pass























