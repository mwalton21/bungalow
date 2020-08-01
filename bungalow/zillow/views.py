import logging
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Listing
from . import forms
from . import data
log = logging.getLogger('zillow.views')

# Create your views here.
def index(request):
    context = {'listings': Listing.objects.order_by('-last_updated')}
    return render(request, 'zillow/index.html', context)


def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    return render(request, 'zillow/listing.html', {'listing': listing})

def sale_history(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    return render(request, 'zillow/sale_history.html', {'listing': listing})


def ingest(request):
    if request.method == 'POST':
        # this is when the file is being uploaded
        form = forms.UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # redirect to index page for simplicity
            data.ingest_data(form.cleaned_data['import_file'])
            return HttpResponseRedirect('/zillow/')
        # TODO handle errors
    else:
        form = forms.UploadFileForm()
    return render(request, 'zillow/import.html', {'form': form})
