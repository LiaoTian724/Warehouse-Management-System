from django.shortcuts import render
from .models import Item
from accounts.models import UserProfile



def index(request):
    user = request.user

    if user.userprofile.role == "ADMIN":
        pending_count = UserProfile.objects.filter(
            status="PENDING"
        ).count()


        return render(
            request,
            "inventory/admin_index.html",
            {
                "pending_count": pending_count
            }
        )


    else:

        items = Item.objects.all()

        return render(
            request,
            "inventory/index.html",
            {
                "items": items
            }
        )




def inventory_list(request):

    items = Item.objects.all()


    return render(
        request,
        "inventory/inventory_list.html",
        {
            "items":items
        }
    )