from xhtml2pdf import pisa
from .forms import SalaryForm
from django.template.loader import get_template
from django.urls import reverse
from .forms import RecruitmentPostForm
import csv
from reportlab.pdfgen import canvas
from io import BytesIO
from django.utils import timezone
from .models import RecruitmentPost
from django.template.loader import render_to_string
from django.http import HttpResponse
from .models import Salary
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from Authentication.models import HR, Manager, Staff, Director


@login_required
def hr_dashboard(request):
    hr = HR.objects.get(id=request.session['user_id'])
    return render(request, 'hr/hr_dashboard.html', {'hr': hr})


def employee_panel(request):
    return render(request, 'hr/employee_panel.html')


def hr_profile(request):
    if request.session.get('role') == 'hr':
        try:
            hr = HR.objects.get(id=request.session['user_id'])
        except HR.DoesNotExist:
            hr = None
    else:
        return redirect('user_login')

    return render(request, 'hr/hr_profile.html', {'hr': hr})


from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Staff, Manager
from django.contrib.auth.decorators import login_required


def manage_employees(request):
    hr_id = request.session.get('user_id')
    hr = get_object_or_404(HR, id=hr_id)
    company_code = hr.company_code

    staff_list = Staff.objects.filter(company_code=company_code, is_suspended=False)
    manager_list = Manager.objects.filter(company_code=company_code, is_suspended=False)

    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        manager_id = request.POST.get('manager_id')

        if staff_id and manager_id:
            staff = get_object_or_404(Staff, id=staff_id)
            manager = get_object_or_404(Manager, id=manager_id)

            if staff.department == manager.department:
                staff.manager = manager
                staff.save()
                messages.success(request, f"✅ {staff.full_name} assigned to {manager.full_name} successfully.")
            else:
                messages.error(request, "⚠️ Manager and Staff departments must match!")

    total_employees = staff_list.count() + manager_list.count()

    context = {
        'staff_list': staff_list,
        'manager_list': manager_list,
        'total_employees': total_employees,
    }
    return render(request, 'hr/manage_employees.html', context)

def manual_team_shuffle(request):
    staff_list = Staff.objects.all()
    manager_list = Manager.objects.all()

    return render(request, 'hr/manual_team_shuffle.html', {
        'staff_list': staff_list,
        'manager_list': manager_list,
    })


def save_team_shuffling(request):
    if request.method == 'POST':
        for staff_id, manager_id in request.POST.items():
            if staff_id.startswith('staff_'):
                try:
                    staff = Staff.objects.get(id=staff_id.split('_')[1])
                    manager = Manager.objects.get(id=manager_id)
                    staff.manager = manager
                    staff.department = manager.department
                    staff.save()
                except (Staff.DoesNotExist, Manager.DoesNotExist):
                    pass
    return redirect('manage_employees')


from django.views.decorators.http import require_http_methods


@require_http_methods(["GET", "POST"])
def assign_manager(request, staff_id):
    staff_member = get_object_or_404(Staff, pk=staff_id)

    if request.method == 'POST':
        manager_id = request.POST.get('manager')
        if manager_id:
            manager = get_object_or_404(Manager, pk=manager_id)
            staff_member.manager = manager
            staff_member.save()
            messages.success(request, f'Manager assigned to {staff_member.full_name}.')
            return redirect('manage_employees')
        else:
            messages.error(request, 'Please select a valid manager.')

    managers = Manager.objects.all()
    return render(request, 'hr/assign_manager.html', {'staff': staff_member, 'managers': managers})


def edit_staff(request, staff_id):
    staff = get_object_or_404(Staff, pk=staff_id)
    if request.method == 'POST':
        staff.full_name = request.POST['full_name']
        staff.email = request.POST['email']
        staff.contact_number = request.POST['contact_number']
        staff.department = request.POST['department']
        staff.position = request.POST['position']
        staff.save()
        messages.success(request, 'Staff updated successfully.')
        return redirect('manage_employees')
    return render(request, 'hr/edit_staff.html', {'staff': staff})


def edit_manager(request, manager_id):
    manager = get_object_or_404(Manager, pk=manager_id)
    if request.method == 'POST':
        manager.full_name = request.POST['full_name']
        manager.email = request.POST['email']
        manager.phone = request.POST['phone']
        manager.department = request.POST['department']
        manager.designation = request.POST['designation']
        manager.save()
        messages.success(request, 'Manager updated successfully.')
        return redirect('manage_employees')
    return render(request, 'hr/director_edit_manager.html', {'manager': manager})



def recruitment_list(request):
    posts = RecruitmentPost.objects.all()

    for post in posts:
        if post.offer_letter:
            post.absolute_offer_url = request.build_absolute_uri(post.offer_letter.url)
        else:
            post.absolute_offer_url = ""

    return render(request, 'hr/recruitment_list.html', {'posts': posts})


def add_recruitment(request):
    if request.method == 'POST':
        form = RecruitmentPostForm(request.POST, request.FILES)  # Also include request.FILES if using FileField
        if form.is_valid():
            form.save()
            return redirect('recruitment_list')
        else:
            print(form.errors)  # Print errors to console for debugging
    else:
        form = RecruitmentPostForm()

    return render(request, 'hr/add_recruitment.html', {
        'form': form,
        'form_title': 'Add Recruitment Post'
    })


def edit_recruitment(request, post_id):
    post = get_object_or_404(RecruitmentPost, id=post_id)
    if request.method == 'POST':
        form = RecruitmentPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Recruitment post updated successfully.')
            return redirect('recruitment_list')
    else:
        form = RecruitmentPostForm(instance=post)
    return render(request, 'hr/add_recruitment.html', {'form': form, 'form_title': 'Edit Recruitment Post'})


def delete_recruitment(request, post_id):
    post = get_object_or_404(RecruitmentPost, id=post_id)
    post.delete()
    messages.success(request, 'Recruitment post deleted.')
    return redirect('recruitment_list')


def lock_recruitment(request, post_id):
    post = get_object_or_404(RecruitmentPost, id=post_id)
    post.is_locked = True
    post.save()
    messages.success(request, 'Post locked successfully.')
    return redirect('recruitment_list')


def upload_offer_letter(request, post_id):
    post = get_object_or_404(RecruitmentPost, id=post_id)
    if request.method == 'POST' and 'offer_letter' in request.FILES:
        post.offer_letter = request.FILES['offer_letter']
        post.save()
        messages.success(request, 'Offer letter uploaded.')
    return redirect('recruitment_list')


def download_recruitment_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="recruitment_posts.csv"'

    writer = csv.writer(response)
    writer.writerow(['Title', 'Department', 'Posted', 'Deadline', 'Status'])

    posts = RecruitmentPost.objects.all()
    for post in posts:
        writer.writerow([post.title, post.department, post.posted_date, post.last_date, post.status])

    return response


def download_recruitment_pdf(request):
    posts = RecruitmentPost.objects.all()
    html_string = render_to_string('hr/recruitment_pdf_template.html', {'posts': posts})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="recruitment_posts.pdf"'
    pisa.CreatePDF(html_string, dest=response)
    return response


def recruitment_list(request):
    posts = RecruitmentPost.objects.all().order_by('-posted_date')
    # Add absolute URLs for sharing
    for post in posts:
        post.absolute_offer_url = request.build_absolute_uri(post.offer_letter.url) if post.offer_letter else ""
        post.get_absolute_url = request.build_absolute_uri(reverse('recruitment_detail', args=[post.pk]))
    return render(request, 'hr/recruitment_list.html', {'posts': posts})


def recruitment_detail(request, pk):
    post = get_object_or_404(RecruitmentPost, pk=pk)
    return render(request, 'hr/recruitment_detail.html', {'post': post})


def export_recruitment(request):
    format = request.GET.get('format', 'csv')
    posts = RecruitmentPost.objects.all()

    if format == 'pdf':
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="recruitment_list.pdf"'

        buffer = BytesIO()
        p = canvas.Canvas(buffer)

        # PDF Header
        p.drawString(100, 800, "Recruitment Posts List")
        p.drawString(100, 780, "Generated on: " + timezone.now().strftime("%Y-%m-%d"))

        # PDF Content
        y = 750
        for post in posts:
            p.drawString(100, y, f"Title: {post.title}")
            p.drawString(100, y - 20, f"Department: {post.department}")
            p.drawString(100, y - 40, f"Posted: {post.posted_date.strftime('%Y-%m-%d')}")
            p.drawString(100, y - 60, f"Deadline: {post.last_date.strftime('%Y-%m-%d')}")
            p.drawString(100, y - 80, f"Status: {post.status}")
            y -= 100

            if y < 100:
                p.showPage()
                y = 750

        p.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

    else:  # CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="recruitment_list.csv"'

        writer = csv.writer(response)
        writer.writerow(['Title', 'Department', 'Posted Date', 'Deadline', 'Status', 'Vacancies', 'URL'])

        for post in posts:
            writer.writerow([
                post.title,
                post.department,
                post.posted_date.strftime('%Y-%m-%d'),
                post.last_date.strftime('%Y-%m-%d'),
                post.status,
                post.vacancies,
                request.build_absolute_uri(reverse('recruitment_detail', args=[post.pk]))
            ])

        return response


def add_salary(request):
    if request.method == 'POST':
        form = SalaryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('salary_list')
    else:
        form = SalaryForm(request.GET or None)

    return render(request, 'hr/salary_form.html', {'form': form})


def salary_list(request):
    query = request.GET.get('q', '')

    salaries = Salary.objects.all()
    if query:
        salaries = salaries.filter(
            Q(staff__full_name__icontains=query) |
            Q(manager__full_name__icontains=query)
        )

    return render(request, 'hr/salary_list.html', {'salaries': salaries})


def download_payslip(request, salary_id):
    # Fetch the salary object by ID
    salary = get_object_or_404(Salary, id=salary_id)

    # Your custom salary slip HTML template
    template_path = 'hr/salary_slip_template.html'

    # Context data to pass to template
    context = {'salary': salary}

    # Create response object with PDF type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="payslip_{salary.id}.pdf"'

    # Render HTML template to a string
    template = get_template(template_path)
    html = template.render(context)

    # Generate PDF from the HTML
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Handle PDF creation error
    if pisa_status.err:
        return HttpResponse('Error generating PDF: %s' % pisa_status.err)

    return response
