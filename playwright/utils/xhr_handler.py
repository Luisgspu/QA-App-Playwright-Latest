from playwright.sync_api import Page

def capture_xhr_responses(page: Page):
    xhr_responses = []

    def handle_response(response):
        if response.request.resource_type == 'xhr':
            xhr_responses.append({
                'url': response.url,
                'status': response.status,
                'body': response.body()  # Assuming you want the body as well
            })

    page.on('response', handle_response)
    return xhr_responses

def attach_xhr_to_allure(xhr_responses):
    import allure
    import json

    try:
        allure.attach(
            json.dumps(xhr_responses, indent=2),
            name="XHR Responses",
            attachment_type=allure.attachment_type.JSON
        )
    except Exception as e:
        logging.error(f"❌ Error attaching XHR data to Allure: {e}")