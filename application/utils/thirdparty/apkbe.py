import time
import lxml
import requests

from bs4 import BeautifulSoup


class Apkbe:
    APKBE_BASE_URL = "https://www.apkbe.com"
    APKBE_RESPONSE_URL = 'https://www.apkbe.com/apk'

    def __init__(self, logger):
        self.logger = logger

    def get_page_count(self):
        page_count = 0
        try:
            response = requests.get(self.APKBE_RESPONSE_URL)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                page_links = soup.find('div', {'class': 'pagelist'})
                page_numbers = [int(link.text) for link in page_links if link.text.isdigit()]
                page_count = max(page_numbers)
            else:
                self.logger.error(f'Response status code is not 200, {response.status_code}')
        except requests.RequestException as e:
            self.logger.error(f'Error while getting response for page {page_count}: {e}')
        return page_count

    def fetch_all_apps(self):
        response_data_list = []
        page = 0
        page_count = self.get_page_count()

        while page_count > page:
            try:
                response = requests.get(self.APKBE_RESPONSE_URL.format(page))
                if response.status_code == 200:
                    response_data = response.text
                    response_data_list.append(response_data)
                else:
                    self.logger.error(f'Response status code is not 200, {response.status_code}')
            except requests.RequestException as e:
                self.logger.error(f'Error while getting response for page {page}: {e}')

            page += 1
            time.sleep(5)
            self.logger.info(f'The content of the page: {page} was successfully retrieved')

        return response_data_list

    def convert_app_img_to_base64(self, img_url):
        img_base64 = ''
        try:
            img_src = requests.get(img_url).content
            if img_src:
                img_base64 = base64.b64encode(img_src).decode('utf-8')
            else:
                self.logger.error(f'Response is empty, {img_url}')
        except:
            self.logger.error(f'Error while getting response, {img_url}')
        return img_base64

    def get_page_all_href(self, apkbe_response):
        all_href = []
        try:
            self.logger.info(f'Start getting hrefs from list...')
            soup = BeautifulSoup(apkbe_response, 'lxml')
            apps_list_table = soup.find('table', class_='apkList')
            apps_list = apps_list_table.find_all('td', {'class': 'icon'})
            for app in apps_list:
                app_href = app.find('a').get('href')
                all_href.append(app_href)
            self.logger.info(f'Success get all href from the list...')
        except:
            self.logger.error(f'Error while getting hrefs from page!')
        return all_href

    def get_app_response_with_url(self, url):
        web_page_app = ''
        try:
            response = requests.get(url)
            if response.status_code < 400:
                web_page_app = BeautifulSoup(response.text, 'lxml')
        except:
            self.logger.error(f'Error while getting response, {url}')
        return web_page_app

    def get_app_details(self, href):
        url = f"{self.APKBE_BASE_URL}{href}"
        found_app = {}
        try:
            web_page_app = self.get_app_response_with_url(url)
            if web_page_app:
                app_details = web_page_app.find('div', id='main')
                app_configs = app_details.find('div', id='apkMetaInfo').find_all('li', {'class': 'clearfix'})
                if app_details:
                    app_header_element = app_details.find('div', {'class': 'mainBody'})
                    app_title = app_header_element.find('h1').text
                    app_id = app_header_element.find('a', {'class': 'report-new-version'}).get('data-code')
                    app_img_url = app_header_element.find('img').get('src')
                    app_description = app_details.find('div', {'class': 'apkTabContent clearfix'}).text.strip()
                    app_download_href = web_page_app.find('a', {'class': 'downloadBtn'}).get('href')
                    app_download_url = f"{self.APKBE_BASE_URL}{app_download_href}"
                    found_app.update({'title': app_title, 'application_id': app_id, 'app_img': app_img_url, 'description': app_description, 'download_url': app_download_url})
                for app_config in app_configs:
                    app_config_header = app_config.find('span').text
                    app_config_value = app_config.find('em').text
                    if app_config_header == 'Category: ':
                        found_app.update({'category': app_config_value})
                    elif app_config_header == 'Requirement: ':
                        found_app.update({'requirement': app_config_value})
                    elif app_config_header == 'Updated: ':
                        found_app.update({'updated': app_config_value})

        except:
            self.logger.error(f'Error while getting app details from page')
        return found_app

    def get_apkbe_apps(self):
        found_apps = []
        apkbe_response_list = self.fetch_all_apps()
        for apkbe_response in apkbe_response_list:
            try:
                href_list = self.get_page_all_href(apkbe_response)
                for href in href_list:
                    found_app = self.get_app_details(href)
                    found_apps.append(found_app)
            except:
                self.logger.error(f'Error while getting apps from page')
        return found_apps
