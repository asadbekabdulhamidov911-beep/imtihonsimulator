from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import datetime
from .models import Question, Option

def home(request):
    return render(request, "home.html")

def savollar(request):
    if request.method == "POST":
        total_questions = Question.objects.count()
        correct_answers = 0
        
        for key, value in request.POST.items():
            if key.startswith("question_"):
                option_id = value
                if Option.objects.filter(id=option_id, is_correct=True).exists():
                    correct_answers += 1

        end_time = timezone.now()
        start_time_iso = request.session.get('start_time')

        duration_str = "Noma'lum"
        if start_time_iso:
            start_time = datetime.fromisoformat(start_time_iso)
            duration = end_time - start_time
            
            total_seconds = int(duration.total_seconds())
            minutes, seconds = divmod(total_seconds, 60)
            hours, minutes = divmod(minutes, 60)
            
            if hours > 0:
                duration_str = f"{hours} soat {minutes} daqiqa {seconds} sekund"
            elif minutes > 0:
                duration_str = f"{minutes} daqiqa {seconds} sekund"
            else:
                duration_str = f"{seconds} sekund"

            request.session['start_time_formatted'] = start_time.strftime("%H:%M:%S")
            request.session['end_time_formatted'] = end_time.strftime("%H:%M:%S")
            request.session['duration'] = duration_str

        request.session['correct_answers'] = correct_answers
        request.session['total_questions'] = total_questions
        return redirect("javob")

    request.session['start_time'] = timezone.now().isoformat()

    questions = Question.objects.prefetch_related('options').all()
    return render(request, "savollar.html", {"questions": questions})

def javob(request):
    correct = request.session.get('correct_answers', 0)
    total = request.session.get('total_questions', 0)
    start_time = request.session.get('start_time_formatted', '-')
    end_time = request.session.get('end_time_formatted', '-')
    duration = request.session.get('duration', '-')
    
    score_percentage = 0
    if total > 0:
        score_percentage = int((correct / total) * 100)

    context = {
        "correct": correct,
        "total": total,
        "percentage": score_percentage,
        "start_time": start_time,
        "end_time": end_time,
        "duration": duration
    }
    return render(request, "javob.html", context)

def admin_panel(request):
    if request.method == "POST":
        delete_id = request.POST.get("delete_question_id")
        if delete_id:
            question = get_object_or_404(Question, id=delete_id)
            question.delete()
            return redirect("admin_panel")

        question_text = request.POST.get("question_text")
        options = request.POST.getlist("options")
        correct_index = int(request.POST.get("correct_option", 0))

        if question_text and options:
            question = Question.objects.create(text=question_text)
            for idx, opt_text in enumerate(options):
                if opt_text.strip():
                    Option.objects.create(
                        question=question,
                        text=opt_text,
                        is_correct=(idx == correct_index)
                    )
        return redirect("admin_panel")

    questions = Question.objects.prefetch_related('options').all()
    return render(request, "admin.html", {"questions": questions})