# views.py

from django.shortcuts import render
from django.http import JsonResponse
import subprocess
from .models import SpiderExecution

from .models import Spider
import importlib
from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings


def index(request):
    spiders = Spider.objects.all()
    spider_executions = SpiderExecution.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'spiders': spiders, 'spider_executions': spider_executions})


def run_spider(request):
    if request.method == 'POST':
        spider_name = request.POST.get('spider_name')
        try:
            spider = Spider.objects.get(name=spider_name)
            spider_module_name = f'imma.spiders.{spider.spider_file}'
            spider_class_name = spider.spider_class

            run_spider_sync(spider_name, spider_module_name, spider_class_name)

            return JsonResponse({'status': 'success', 'message': f'Spider "{spider_name}" execution started.'})
        except Spider.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': f'Spider "{spider_name}" not found.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


def run_spider_sync(spider_name, spider_module_name, spider_class_name):
    spider_module = importlib.import_module(spider_module_name)
    spider_class = getattr(spider_module, spider_class_name)

    execution = SpiderExecution.objects.create(spider_name=spider_name, status='running')

    settings = get_project_settings()
    settings.set('FEED_URI', f'scraped_data_{spider_name}.csv')
    settings.set('FEED_FORMAT', 'csv')
    settings.set('CONCURRENT_REQUESTS', 96)
    settings.set('DOWNLOAD_DELAY', 0.2)
    settings.set('HTTPCACHE_ENABLED', True)

    runner = CrawlerRunner(settings)
    runner.crawl(spider_class)
    runner.join()

    execution.status = 'completed'
    execution.save()


def save_file(request):
    if request.method == 'POST':
        file_name = request.POST.get('file_name')
        # Replace with the path to the scraped_data.csv file
        file_path = '../scraped_data.csv'

        try:
            # Save the file locally
            with open(file_path, 'rb') as file:
                data = file.read()
                with open(file_name, 'wb') as new_file:
                    new_file.write(data)
            return JsonResponse({'status': 'success', 'message': 'File saved successfully.'})
        except FileNotFoundError:
            return JsonResponse({'status': 'error', 'message': 'File not found.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
