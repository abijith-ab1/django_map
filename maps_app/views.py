from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseForbidden
from allauth.account.models import EmailAddress
from django.contrib.auth.decorators import login_required
from django.conf import settings
import folium
import geocoder

from .models import SearchHistory
from .forms import SearchForm

def email_verified_required(function):
    @login_required
    def wrap(request, *args, **kwargs):
        if request.user.emailaddress_set.filter(verified=True).exists():
            return function(request, *args, **kwargs)
        else:
            return redirect(reverse('account_email_verification_sent'))
    return wrap

@login_required
@email_verified_required
def maps_view(request):
    form = SearchForm(request.POST or None)
    m = None
    if form.is_valid():
        search_term = form.cleaned_data.get('search_term')
        location = geocoder.osm(search_term)
        if location:
            lat = location.lat
            lng = location.lng
            country = location.country
            if lat is not None and lng is not None:
                SearchHistory.objects.create(
                    user=request.user,
                    search_term=search_term,
                    location_name=search_term,
                    location_image=f"https://maps.googleapis.com/maps/api/streetview?size=600x400&location={lat},{lng}&key={settings.GOOGLE_MAPS_API_KEY}"
                )
                m = folium.Map(location=[lat, lng], zoom_start=10)
                folium.Marker([lat, lng], tooltip='Click for more',
                                popup=country).add_to(m)
                m = m._repr_html_()
                context = {
                    'm': m,
                    'form': form,
                    'history': SearchHistory.objects.filter(user=request.user).order_by('-searched_at'),
                    'google_api_key': settings.GOOGLE_MAPS_API_KEY
                }
                return render(request, 'maps_app/maps.html', context)
    else:
        form = SearchForm()

    context = {
        'm': m,
        'form': form,
        'history': SearchHistory.objects.filter(user=request.user).order_by('-searched_at'),
        'google_api_key': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, 'maps_app/maps.html', context)



@login_required
def delete_page(request):
    history = SearchHistory.objects.filter(user=request.user)
    return render(request, 'maps_app/deletehistory.html', {'history': history})

@login_required
def delete_history(request, history_id):
    history = SearchHistory.objects.get(id=history_id, user=request.user)
    if history:
        history.delete()
        return redirect('delete_page')
