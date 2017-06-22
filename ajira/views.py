from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.forms.models import model_to_dict
from itertools import chain

from .forms import UserForm, UserLoginForm, PostCreateForm, PostEditForm, UserEditProfileForm, UserAddCareerInterestsForm, JobTitleForm, LocationForm
from .models import Post, AjiraUser, CareerInterests, JobTitle, Location
from .serializers import PostSerializer

import re

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

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
            recommended_posts = Post.objects.all() #Post.objects.filter(title__contains='Computer')
            career_interests = None
            if user.career_interests:
                career_interests = CareerInterests.objects.get(pk=user.career_interests.id)

            if career_interests:
                job_titles = JobTitle.objects.filter(careerinterests=career_interests.id)
                job_locations = Location.objects.filter(careerinterests=career_interests.id)

                title_regex = '('
                for title in job_titles:
                    title_words = title.title.split()
                    for word in title_words:
                        title_regex += word.lower() + "|"
                title_regex = title_regex[:-1]
                title_regex += ')'

                print(title_regex)

                location_regex = '('
                for loc in job_locations:
                    location_regex += loc.region.lower() + "|"
                location_regex = location_regex[:-1]
                location_regex += ')'

                print(location_regex)

                recommended_posts = Post.objects.filter(title_lower__regex=title_regex)
                # recommended_posts = Post.objects.filter(title_lower__regex=r'(software|engineering)')
                print(recommended_posts)
            return render(request, self.template_name, {'user': user, self.context_object_name: recommended_posts})

        return render(request, self.template_name, {self.context_object_name: Post.objects.all()})


    def get_queryset(self):
        """
        :return: A list of posts to be displayed
        """
        return Post.objects.all()


class UserPostListView(generic.ListView):
    template_name = 'ajira/user_posts_list.html'
    context_object_name = 'user_posts'

    def get(self, request):
        user = request.user
        if user.is_authenticated():
            context = {'user': user, self.context_object_name: user.post_set.all()}
            return render(request, self.template_name, context)

        return render(request, self.template_name, {})


class UserPostEditView(generic.View):
    template_name = 'ajira/post_form.html'
    #context_object_name = 'post'
    form_class = PostEditForm

    # display filled in form for user to edit post
    def get(self, request, pk):
        if request.user.is_authenticated():
            post = Post.objects.get(pk=pk)
            form = self.form_class(instance=post)
            context = {
                'form': form,
                'edit': True,
                'post': post,
                'title': "Edit Post | Ajira"
            }
            return render(request, self.template_name, context)

        return HttpResponseRedirect(reverse('ajira:login'))

    # process form data
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        form = self.form_class(request.POST, request.FILES, instance=post)

        if form.is_valid():
            #post.user = request.user
            post.title_lower = post.title.lower()
            post.save()

            return HttpResponseRedirect(reverse('ajira:edit_posts'))

        return self.get(request, pk)#render(request, self.template_name, {'form': form})


class UserPostDeleteView(generic.DeleteView):
    model = Post
    success_url = reverse_lazy('ajira:edit_posts')


class PostDetailView(generic.DetailView):
    model = Post
    template_name ='ajira/detail.html'
    context_object_name = 'post'


class PostCreateView(generic.View):
    form_class = PostCreateForm
    template_name = 'ajira/post_form.html'

    # display blank form for user to create post if signed in
    def get(self, request):
        if request.user.is_authenticated():
            form = self.form_class(data=None)

            return render(request, self.template_name, {'form': form, 'edit': False})

        return HttpResponseRedirect(reverse('ajira:register'))

    # process form data
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.title_lower = post.title.lower()
            post.user = request.user
            post.save()

            return HttpResponseRedirect(reverse('ajira:detail', args=(post.id,)))

        return render(request, self.template_name, {'form': form})


    """
    def form_valid(self, form):
        post = form.instance

        # get the signed in user's primary key
        post.user = get_object_or_404(User, pk=3)
        self.object = form.save()
        return HttpResponseRedirect(reverse('ajira:detail', args=(post.id,)))
    """


# Sign up form
class UserFormView(generic.View):
    form_class = UserForm
    template_name = 'ajira/registration_form.html'

    # display blank form for user to sign up on
    def get(self, request):
        form = self.form_class(data=None)
        form.fields['password'].widget.attrs.update({
            'placeholder': 'Password'
        })

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
        form.fields['password'].widget.attrs.update({
            'placeholder': 'Password'
        })

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


class UserProfileView(generic.DetailView):
    model = AjiraUser
    template_name ='ajira/view_profile.html'
    context_object_name = 'user'


class UserProfileEditView(generic.View):
    template_name = 'ajira/edit_profile_form.html'
    #context_object_name = 'user'
    form_class = UserEditProfileForm

    # display filled in form for user to edit post
    def get(self, request, pk):
        if request.user.is_authenticated():
            user = AjiraUser.objects.get(pk=pk)
            form = self.form_class(instance=user)
            return render(request, self.template_name, {'form': form})

        return HttpResponseRedirect(reverse('ajira:login'))

    # process form data
    def post(self, request, pk):
        user = AjiraUser.objects.get(pk=pk)
        form = self.form_class(request.POST, request.FILES, instance=user)

        if form.is_valid():
            #post.user = request.user
            user.save()

            return HttpResponseRedirect(reverse('ajira:view_profile', args=pk))

        return render(request, self.template_name, {'form': form})


class AddCareerInterests(generic.View):
    form_class = UserAddCareerInterestsForm
    template_name = "ajira/career_interests.html"
    job_form_class = JobTitleForm
    location_form_class = LocationForm

    # display blank form for user to sign in
    def get(self, request, pk):
        user = AjiraUser.objects.get(pk=pk)
        career_interests = CareerInterests()
        if user.career_interests:
            career_interests = CareerInterests.objects.get(pk=user.career_interests.id)
        else:
            career_interests.save()

        job_titles = JobTitle.objects.filter(careerinterests=career_interests.id)
        job_locations = Location.objects.filter(careerinterests=career_interests.id)

        job_forms = []
        for title in job_titles:
            job_form = self.job_form_class(instance=title)
            job_forms.append(job_form)

        job_location_forms = []
        for loc in job_locations:
            location_form = self.location_form_class(instance=loc)
            job_location_forms.append(location_form)

        form = self.form_class(instance=career_interests)
        job_form = self.job_form_class(data=None)
        location_form = self.location_form_class(data=None)
        context = {
            'form': form,
            'job_form': job_form,
            'job_forms': job_forms,
            'num_job_forms': len(job_forms),
            'location_forms': job_location_forms,
            'num_location_forms': len(job_location_forms),
            'location_form': location_form,
            'title_loop_times': range(0, 3-len(job_forms)),
            'location_loop_times': range(0, (3 - len(job_location_forms)))
        }
        return render(request, self.template_name, context)

    # process form data
    def post(self, request, pk):
        user = AjiraUser.objects.get(pk=pk)
        career_interests = CareerInterests()
        if user.career_interests:
            career_interests = CareerInterests.objects.get(pk=user.career_interests.id)
        else:
            career_interests.save()

        job_titles = JobTitle.objects.filter(careerinterests=career_interests.id)
        job_locations = Location.objects.filter(careerinterests=career_interests.id)

        # Delete all titles in database to replace them with new ones
        for title in job_titles:
            title.delete()

        # Delete all locations in database to replace them with new ones
        for loc in job_locations:
            loc.delete()


        for title in request.POST.getlist('title'):
            job_title = JobTitle()
            job_title.title = title
            job_title.title_lower = title.lower()
            if job_title.title != '':
                job_title.save()
                career_interests.job_titles.add(job_title)

        name_list = request.POST.getlist('name')
        city_list = request.POST.getlist('city')
        region_list = request.POST.getlist('region')
        country_list = request.POST.getlist('country')

        for i in range(len(name_list)):
            job_loc = Location()
            job_loc.name = name_list[i]
            job_loc.city = city_list[i]
            job_loc.region = region_list[i]
            job_loc.country = country_list[i]

            if job_loc.is_valid():
                job_loc.save()
                career_interests.job_locations.add(job_loc)


        career_interests.save()
        user.career_interests = career_interests

        #### REMEMBER TO VALIDATE BEFORE PRODUCTION ####
        if self.is_valid(career_interests):
            user.save()

            return HttpResponseRedirect(reverse('ajira:index'))

        return self.get(request, user.id)

    def is_valid(self, career_interests):
        return True


class AjiraSearchListView(generic.View):
    """
        Display a List page filtered by the search query.
        """
    paginate_by = 10
    template_name = 'ajira/ajira_search_list_view.html'

    def get(self, request):
        # result = super(AjiraSearchListView, self).get_queryset()
        context = {}

        if ('query' in request.GET) and request.GET['query'].strip():

            query_string = request.GET['query']
            print (query_string)
            post_query = get_query(query_string, ['title_lower', 'description', 'company'])
            user_query = get_query(query_string, ['first_name', 'last_name'])

            print(post_query, user_query)

            # found_posts = Post.objects.filter(post_query).order_by('-pub_date')
            found_posts = Post.objects.filter(post_query)
            found_users = AjiraUser.objects.filter(user_query)

            print(found_posts, found_users)

            result_list = list(chain(found_posts, found_users))
            context = {
                'query_string': query_string,
                'result_list': result_list,
                'found_posts': found_posts,
                'found_users': found_users
            }
            print (result_list)
        print(context)
        return render(request, self.template_name, context)


def view_resume(request):
    resume_path = request.user.resume
    with open(resume_path, 'r') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'filename=my_resume.pdf'
        return response


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























