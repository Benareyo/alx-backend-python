from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from messaging.models import Message
from django.views.decorators.cache import cache_page
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from .models import Message
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@cache_page(60)  # <-- 60 seconds cache timeout
@login_required
def conversation_messages(request, conversation_id):
    messages = Message.objects.filter(conversation_id=conversation_id).select_related('sender', 'receiver').only('id', 'sender', 'receiver', 'content', 'timestamp')
    return render(request, 'messaging/conversation_messages.html', {'messages': messages})
@login_required
def conversation_messages(request, conversation_id):
    messages = Message.objects.filter(conversation_id=conversation_id).select_related('sender', 'receiver').only('id', 'sender', 'receiver', 'content', 'timestamp')
    return render(request, 'messaging/conversation_messages.html', {'messages': messages})

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
def unread_messages_view(request):
    """
    View to fetch unread messages for the logged-in user,
    using the custom unread manager method and optimized with .only().
    """
    unread_messages = Message.unread.unread_for_user(request.user).select_related('sender').order_by('-timestamp').only(
        'id', 'sender', 'content', 'timestamp'
    )

    context = {
        'unread_messages': unread_messages
    }
    return render(request, 'messaging/unread_messages.html', context)
