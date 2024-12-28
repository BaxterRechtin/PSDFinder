from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def parse_results_table(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", id="ContentPlaceHolder1_tblResults")

    if not table:
        return "No results table found."

    rows = table.find_all("tr", class_="ResultsRow")
    parsed_data = []

    for row in rows:
        columns = row.find_all("td")
        data = {
            "Location": columns[0].get_text(strip=True),
            "PSD Code": columns[1].get_text(strip=True),
            "Resident EIT": columns[2].get_text(strip=True),
            "Non-Resident EIT": columns[3].get_text(strip=True),
            "LST": columns[4].get_text(strip=True),
            "LST Low Income Exemption": columns[5].get_text(strip=True),
        }
        parsed_data.append(data)

    return parsed_data

def get_psd_code(home_address, home_city, home_zip_code, work_address, work_city, work_zip):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options)

    try:
        print("Opening the website...")
        driver.get("https://apps.dced.pa.gov/Munstats-Public/FindLocalTax.aspx")
        print("Website loaded. Waiting for elements...")

        wait = WebDriverWait(driver, 20)

        work_address_field = wait.until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_txtWorkStreet")))
        print("Work address field located.")
        work_city_field = driver.find_element(By.ID, "ContentPlaceHolder1_txtWorkCity")
        work_zip_field = driver.find_element(By.ID, "ContentPlaceHolder1_txtWorkZip")
        home_address_field = driver.find_element(By.ID, "ContentPlaceHolder1_txtHomeStreet")
        home_city_field = driver.find_element(By.ID, "ContentPlaceHolder1_txtHomeCity")
        home_zip_field = driver.find_element(By.ID, "ContentPlaceHolder1_txtHomeZip")
        search_button = driver.find_element(By.ID, "ContentPlaceHolder1_btnViewInformation")
        print("All input fields located.")

        work_address_field.send_keys(work_address)
        work_city_field.send_keys(work_city)
        work_zip_field.send_keys(work_zip)
        home_address_field.send_keys(home_address)
        home_city_field.send_keys(home_city)
        home_zip_field.send_keys(home_zip_code)
        print("Input fields populated.")

        search_button.click()
        print("Search button clicked. Waiting for results...")

        results_table = wait.until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_tblResults")))
        print("Results table located.")

        # Retrieve the HTML content of the results table
        results_html = results_table.get_attribute("outerHTML")
        print("Results table retrieved.")

        # Parse the results table
        parsed_results = parse_results_table(results_html)

        return parsed_results

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    finally:
        driver.quit()

if __name__ == "__main__":
    home_address = "11 MacBride Drive"
    home_city = "Harrisburg"
    home_zip_code = "19475"
    work_address = "1017 Dorrance Street"
    work_city = "Philadelphia"
    work_zip = "19146"

    results = get_psd_code(home_address, home_city, home_zip_code, work_address, work_city, work_zip)
    if results:
        print("Parsed Results:")
        for row in results:
            print(row)
    else:
        print("Failed to retrieve the results table.")
