from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login

from .forms import UploadPostForm, UserForm
from .models import Post, User
from .file_handler import handle_uploaded_file


# Create your views here.


def upload_file(request, post_id):
    if request.method == 'POST':
        form = UploadPostForm(request.POST, request.FILES)
        if form.is_valid():
            #handle_uploaded_file(request.FILES['file'], post_id)
            #instance = Post(file_field=request.FILES['file'])
            #instance.save()
            # return HttpResponseRedirect('/success/url/')
            # return HttpResponseRedirect(reverse('ajira:results', args=(question.id,)))
            return HttpResponseRedirect(reverse('ajira:about'))
    else:
        form = UploadPostForm()
    return render(request, 'upload.html', {'form': form})


class IndexView(generic.ListView):
    template_name = 'ajira/index.html'
    context_object_name = 'posts_list'

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

            # returns User objects if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:
                # if user's account did not get banned or disabled
                if user.is_active:
                    login(request, user)
                    #request.user.username
                    return redirect('ajira:index')

        return render(request, self.template_name, {'form': form})



class AboutPageView(generic.TemplateView):
    template_name = "ajira/about.html"























