import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Create a session with a specific User-Agent to mimic a web browser
session = requests.Session()
session.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"

def get_all_forms(url):
    # Get all form elements from the specified URL
    soup = BeautifulSoup(session.get(url).content, "html.parser")
    return soup.find_all("form")

def get_form_details(form):
    # Extract important details (action, method, inputs) from a given form
    form_details_dict = {}
    action = form.attrs.get("action")
    method = form.attrs.get("method", "get")
    inputs = []

    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value", "")
        inputs.append({
            "type": input_type,
            "name": input_name,
            "value": input_value,
        })

    form_details_dict['action'] = action
    form_details_dict['method'] = method
    form_details_dict['inputs'] = inputs
    return form_details_dict

def is_vulnerable(response):
    # Check if the response contains common SQL injection error messages
    errors = {
        "quoted string not properly terminated",
        "unclosed quotation mark after the character string",
        "you have an error in your SQL syntax"
    }
    for error in errors:
        if error in response.content.decode().lower():
            return True
    return False

def sql_injection_scan(url):
    # Find forms on the specified URL and scan for SQL injection vulnerabilities
    forms = get_all_forms(url)
    print(f"[+] Detected {len(forms)} forms on {url}.")

    for form in forms:
        details = get_form_details(form)

        for i in "\"'":
            data = {}
            for input_tag in details["inputs"]:
                if input_tag["type"] == "hidden" or input_tag["value"]:
                    data[input_tag['name']] = input_tag["value"] + i
                elif input_tag["type"] != "submit":
                    data[input_tag['name']] = f"test{i}"

            print(url)
            get_form_details(form)

            try:
                if details["method"] == "post":
                    res = session.post(url, data=data)
                elif details["method"] == "get":
                    res = session.get(url, params=data)
                if is_vulnerable(res):
                    print("SQL injection attack vulnerability in link:", url)
                else:
                    print("No SQL injection attack vulnerability detected")
            except Exception as e:
                print("An error occurred during the request:", e)

if __name__ == "__main__":
    # Replace the URL with the URL you want to scan for SQL injection vulnerabilities
    url_to_be_checked = "https://facebook.com"
    sql_injection_scan(url_to_be_checked)
