from django.shortcuts import render, redirect, get_object_or_404
from .models import Conference

# LIST
def conference_list(request):
    conferences = Conference.objects.all()
    return render(request, 'conference/list.html', {'conferences': conferences})


# CREATE
def conference_create(request):
    if request.method == 'POST':
        Conference.objects.create(
            title=request.POST['title'],
            theme=request.POST['theme'],
            location=request.POST['location'],
            place=request.POST['place'],
            start_date=request.POST['start_date'],
            end_date=request.POST['end_date'],
            description=request.POST['description'],
        )
        return redirect('conference_list')

    return render(request, 'conference/create.html')


# DETAIL
def conference_detail(request, id):
    conference = get_object_or_404(Conference, id=id)
    return render(request, 'conference/detail.html', {'conference': conference})


# UPDATE
def conference_update(request, id):
    conference = get_object_or_404(Conference, id=id)

    if request.method == 'POST':
        conference.title = request.POST['title']
        conference.theme = request.POST['theme']
        conference.location = request.POST['location']
        conference.place = request.POST['place']
        conference.start_date = request.POST['start_date']
        conference.end_date = request.POST['end_date']
        conference.description = request.POST['description']
        conference.save()
        return redirect('conference_list')

    return render(request, 'conference/update.html', {'conference': conference})


# DELETE
def conference_delete(request, id):
    conference = get_object_or_404(Conference, id=id)

    if request.method == 'POST':
        conference.delete()
        return redirect('conference_list')

    return render(request, 'conference/delete.html', {'conference': conference})
