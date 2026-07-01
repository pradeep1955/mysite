from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EventForm, MaterialForm, TaskForm
from .models import EventSchedule, Material


@login_required
def event_list(request):
    events = EventSchedule.objects.all().order_by("date", "time")

    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            print("Event Saved!")
            return redirect("event_list")
    else:
        form = EventForm()

    return render(
        request,
        "event/event_list.html",
        {
            "events": events,
            "form": form,
        },
    )


def event_detail(request, event_id):
    event = get_object_or_404(EventSchedule, id=event_id)
    materials = event.materials.all()
    tasks = event.tasks.all()

    return render(
        request,
        "event/event_detail.html",
        {
            "event": event,
            "materials": materials,
            "tasks": tasks,
        },
    )


def event_edit(request, event_id):
    event = get_object_or_404(EventSchedule, id=event_id)

    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect("event_list")
    else:
        form = EventForm(instance=event)

    return render(request, "event/event_edit.html", {"form": form, "event": event})


def add_task(request, event_id):
    event = get_object_or_404(EventSchedule, id=event_id)

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.event = event
            task.save()
            return redirect("event_detail", event_id=event.id)
    else:
        form = TaskForm()

    return render(request, "event/add_task.html", {"form": form, "event": event})


def add_material(request, event_id):
    event = get_object_or_404(EventSchedule, id=event_id)

    if request.method == "POST":
        form = MaterialForm(request.POST)
        if form.is_valid():
            material = form.save(commit=False)
            material.event = event
            material.save()
            return redirect("event_list")
    else:
        form = MaterialForm()

    return render(
        request,
        "event/add_material.html",
        {
            "form": form,
            "event": event,
        },
    )


def edit_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)

    if request.method == "POST":
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            return redirect("event_detail", event_id=material.event.id)
    else:
        form = MaterialForm(instance=material)

    return render(request, "event/edit_material.html", {"form": form, "material": material})


def delete_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    event_id = material.event.id

    if request.method == "POST":
        material.delete()
        return redirect("event_detail", event_id=event_id)

    return render(
        request,
        "event/delete_material_confirm.html",
        {
            "material": material,
        },
    )
