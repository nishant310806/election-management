from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .models import Election, Candidate, Vote

@login_required
def election_list(request):
    elections = Election.objects.filter(is_active=True)
    return render(request, 'elections/election_list.html', {
        'elections': elections
    })

@login_required
def candidate_list(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    now = timezone.now()

    if not election.is_active:
        messages.error(request, "Election is not active.")
        return redirect('election_list')

    if now < election.start_time or now > election.end_time:
        messages.error(request, "Voting is not allowed at this time.")
        return redirect('election_list')

    # ✅ ADD THIS HERE
    has_voted = Vote.objects.filter(
        user=request.user,
        election=election
    ).exists()

    candidates = Candidate.objects.filter(
        election=election,
        is_approved=True
    )

    return render(request, 'elections/candidate_list.html', {
        'election': election,
        'candidates': candidates,
        'has_voted': has_voted,  
    })


@login_required
def cast_vote(request, candidate_id):
    candidate = get_object_or_404(Candidate, id=candidate_id)
    election = candidate.election
    now = timezone.now()

    if not election.is_active:
        messages.error(request, "Election is not active.")
        return redirect('election_list')

    if now < election.start_time or now > election.end_time:
        messages.error(request, "Voting time is over or not started.")
        return redirect('election_list')

    if Vote.objects.filter(user=request.user, election=election).exists():
        messages.error(request, "You have already voted.")
        return redirect('election_list')

    Vote.objects.create(
        user=request.user,
        election=election,
        candidate=candidate
    )

    candidate.votes += 1
    candidate.save()

    messages.success(request, "Your vote has been cast successfully.")
    return redirect('election_list')
