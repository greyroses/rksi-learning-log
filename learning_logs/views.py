from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EntryForm, TopicForm
from .models import Entry, Topic


def index(request):
    return render(request, 'learning_logs/index.html')


@login_required
def topics(request):
    return render(request, 'learning_logs/topics.html', {'topics': Topic.objects.filter(owner=request.user)})


@login_required
def topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id, owner=request.user)
    return render(request, 'learning_logs/topic.html', {'topic': topic, 'entries': topic.entry_set.all()})


@login_required
def new_topic(request):
    form = TopicForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        topic = form.save(commit=False)
        topic.owner = request.user
        topic.save()
        return redirect('learning_logs:topics')
    return render(request, 'learning_logs/topic_form.html', {'form': form, 'heading': 'Новая тема'})


@login_required
def new_entry(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id, owner=request.user)
    form = EntryForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        entry = form.save(commit=False)
        entry.topic = topic
        entry.save()
        return redirect('learning_logs:topic', topic_id=topic.id)
    return render(request, 'learning_logs/entry_form.html', {'form': form, 'topic': topic, 'heading': 'Новая запись'})


@login_required
def edit_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id, topic__owner=request.user)
    form = EntryForm(request.POST or None, instance=entry)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('learning_logs:topic', topic_id=entry.topic.id)
    return render(request, 'learning_logs/entry_form.html', {'form': form, 'topic': entry.topic, 'heading': 'Изменить запись', 'entry': entry})
