from celery.result import AsyncResult
from celery.exceptions import TaskError

from scrapers import StyleInForm
from google_data_manager import rewrite_data_to_sheet
from conf import STYLEINFORM_RETRY_TIMES, STYLEINFORM_REPORT_SHEET, STYLEINFORM_SHEET_NAME
from utils import read_data, clear_intermediate_file

from scheduling import app


@app.task()
def scraper_task_run():
    print('Start scrapper task')
    clear_intermediate_file()
    scraper = StyleInForm()
    print('Total count of products on start: ', scraper.all_products_count)
    scraper.parse_all_products()
    print('Total count of products on end: ', scraper.all_products_count)


@app.task()
def data_checker_task_run(task_id: str):
    print('Started data checker')
    scraper = StyleInForm()
    trying: int = 1
    task_result = AsyncResult(id=task_id)

    while True:
        if task_result.state == 'FAILURE' and trying <= STYLEINFORM_RETRY_TIMES:
            scraper_task_run.delay()
            trying += 1
            continue

        if not task_result.successful() and trying <= STYLEINFORM_RETRY_TIMES:
            continue

        data = read_data()

        if not data and trying > STYLEINFORM_RETRY_TIMES:
            raise TaskError('Not found data after scraping and ending retries limit')

        elif not data and trying <= STYLEINFORM_RETRY_TIMES:
            trying += 1
            scraper_task_run.delay()
            continue

        collected_data, collected_count = data['products'], data['products_count']

        if collected_count < scraper.all_products_count and trying <= STYLEINFORM_RETRY_TIMES:
            scraper_task_run.delay()
            trying += 1
            continue
        else:
            collected_gh_data = [
                [i['product_sku'], i['inventory_qty'] if i.get('inventory_qty') else '',
                 i['inventory_text'] if i.get('inventory_text') else '']
                for i in collected_data if i and i.get('product_sku')
            ]
            rewrite_data_to_sheet(STYLEINFORM_REPORT_SHEET, collected_gh_data, STYLEINFORM_SHEET_NAME)
            print('Successfully added new data to google sheet ')
            break


@app.task()
def run():
    task = scraper_task_run.delay()
    data_checker_task_run.delay(task.task_id)
