from django.shortcuts import render,redirect
from django.http import HttpResponse
from AIStoryGenerator.utils import *
import pandas as pd
from datetime import datetime
from django.urls import reverse
from urllib.parse import urlencode, quote
# Create your views here.

result = None
def home(request):
    global result
    if request.method == 'POST':
        story = request.POST.get('story', '')
        categories = request.POST.getlist('categories')  # Get a list of selected categories
        custom_category_toggle = request.POST.get('customCategoryToggle', '')
        custom_category = request.POST.get('customCategory', '')
        if custom_category_toggle:
            categories.append(custom_category)

        result = generate_complete_story(story, categories)
        if result is not None:
            return redirect('/review_story')

    categories = ['Adventure', 'Romance', 'Mystery', 'Sci-Fi', 'Fantasy', 'Historical', 'Drama', 'Comedy']
    return render(request, 'index.html', {'categories': categories})

from urllib.parse import parse_qs
def review_story(request):
    """data = {
        'story': "this is a sample story coming from backend!!!",
        'twists': [
        ["Twist 1 title ", "Twist 1 body data come here!!!"],
        ["Twist 2 title ", "Twist 2 body data come here!!!"],
        ["Twist 3 title ", "Twist 3 body data come here!!!"],
        ["Twist 4 title ", "Twist 4 body data come here!!!"],
        ["Twist 5 title ", "Twist 5 body data come here!!!"]]}"""
    global result
    data = {
        'story_title': result[0],
        'story': result[1],
        'twists': [[result[2][i], result[3][i]] for i in range(len(result[2]))]
    }
    if request.method == 'POST':
        story_title = request.POST.get('story_title', '')
        story = request.POST.get('story', '')
        twists_data = []
        for i in range(5):
            twist_title = request.POST.get('twist_title_'+str(i+1), '')
            twist_body = request.POST.get('twist_body_'+str(i+1), '')
            order = request.POST.get('twist_order_'+str(i+1), '')
            twists_data.append((twist_title, twist_body, order))
        # twists_data = [('Twist 1 Title', 'Twist 1 Body', 0), ('Twist 2 Title', 'Twist 2 Body', 1)]
        publish_story(story_title, story, twists_data)
        return redirect('/')
    return render(request, 'review_story.html', data)


def dashboard(request):
    dashboard_data = get_analytics()
    df = pd.DataFrame(dashboard_data)
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"dashboard_data_{current_datetime}.csv"
    df.to_csv(file_name, index=False)
    revenue = 12000
    return render(request, 'dashboard.html', {'dashboard_data': dashboard_data, 'revenue': revenue})