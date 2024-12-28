# PSDFinder

# Pennsylvania Tax Withholding Automation Script

## Summary
Pennsylvania has very specific tax withholding regulations, which differentiate between work and home locations. This delineation uses Political Subdivision Codes (PSD codes) to identify the specific withholding rate based on the employee's work and home addresses.

While it is possible to identify this information for individual addresses via a designated web address (https://apps.dced.pa.gov/Munstats-Public/FindLocalTax.aspx), there is no method to retrieve this data in bulk. This limitation presents challenges in ERP data conversion and for businesses performing manual payroll processing.

This script streamlines the process by accepting multiple addresses as input via a CSV file and outputting the corresponding tax withholding information for each address. This allows for easier access to withholding information in bulk.

## Specifics
- **Input:** The script accepts input in CSV format with the file name `addresses.csv`.
- **Automation:** 
  - Utilizes Selenium to interact with the web interface.
  - Identifies the appropriate HTML elements for each address field and populates them.
  - Triggers the search function on the web interface.
  - Captures the resulting HTML table containing the withholding information.
- **Output:** 
  - Parses the results using pandas.
  - Writes the processed data to a file named `results.csv`.

This approach simplifies the process of retrieving bulk tax withholding data, making it more efficient for both ERP integration and manual payroll processing tasks.
****

