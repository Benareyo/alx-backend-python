from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from messaging.models import Message
from django.shortcuts import render


User = get_user_model()

@login_required
def delete_user(request):
    """
    View to allow a logged-in user to delete their account.
    """
    if request.method == 'POST':
        request.user.delete()
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
    messages_qs = Message.objects.filter(sender=request.user).select_related(
        'receiver', 'edited_by', 'parent_message'
    ).prefetch_related(
        'replies'
    ).order_by('-timestamp')

    context = {
        'messages': messages_qs
    }
    return render(request, 'messaging/user_messages.html', context)


@login_required
def get_unread_messages(request):
    """
    View to fetch unread messages for the logged-in user,
    optimized with the custom manager and only necessary fields.
    """
    unread_messages = Message.unread.for_user(request.user).select_related('sender').order_by('-timestamp')

    context = {
        'unread_messages': unread_messages
    }
    return render(request, 'messaging/unread_messages.html', context)
def unread_messages_view(request):
    unread_messages = Message.unread.unread_for_user(request.user).select_related('sender').order_by('-timestamp')
    
    context = {
        'unread_messages': unread_messages
    }
    return render(request, 'messaging/unread_messages.html', context)