from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from messaging.models import Message

User = get_user_model()

@login_required
def delete_user(request):
    """
    View to allow a logged-in user to delete their account.
    """
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, "Your account has been deleted successfully.")
        return redirect('home')  # Change 'home' to your actual landing page name
    return render(request, 'messaging/delete_user_confirm.html')


@login_required
def get_user_messages(request):
    """
    View to fetch messages sent by the logged-in user,
    including related receiver, editor, parent message,
    and prefetch replies for optimized DB queries.
    """
    user = request.user

    messages_qs = Message.objects.filter(sender=user).select_related(
        'receiver', 'edited_by', 'parent_message'
    ).prefetch_related(
        'replies'
    ).order_by('-timestamp')

    context = {
        'messages': messages_qs
    }
    return render(request, 'messaging/user_messages.html', context)
