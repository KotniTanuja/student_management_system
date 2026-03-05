from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Student


@login_required
def student_list(request):
    query = request.GET.get('q')

    if query:
        students = Student.objects.filter(
            Q(name__icontains=query) |
            Q(roll_number__icontains=query) |
            Q(course__icontains=query)
        )
    else:
        students = Student.objects.all()

    return render(request, 'tasks/student_list.html', {'students': students})


@login_required
def student_create(request):
    if request.method == "POST":
        name = request.POST['name']
        roll_number = request.POST['roll_number']
        email = request.POST['email']
        course = request.POST['course']

        Student.objects.create(
            name=name,
            roll_number=roll_number,
            email=email,
            course=course
        )

        return redirect('student_list')

    return render(request, 'tasks/student_form.html')


@login_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        student.name = request.POST['name']
        student.roll_number = request.POST['roll_number']
        student.email = request.POST['email']
        student.course = request.POST['course']
        student.save()

        return redirect('student_list')

    return render(request, 'tasks/student_form.html', {'student': student})


@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        student.delete()
        return redirect('student_list')

    return render(request, 'tasks/student_confirm_delete.html', {'student': student})


@login_required
def dashboard(request):
    total_students = Student.objects.count()
    total_courses = Student.objects.values('course').distinct().count()

    context = {
        'total_students': total_students,
        'total_courses': total_courses,
    }

    return render(request, 'tasks/dashboard.html', context)