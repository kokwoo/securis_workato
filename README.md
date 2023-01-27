# Securis Workato Script (For eBay API endpoint)
Convert eBays API into Workato object definition

## Environment

- Python 3.9.7

## What is this for

- Reduce time spend on converting eBay response payload which also correspond to majority of the input fields to Workato object definition.
- The script does not convert it exactly to how Workato formats it's object definition, we are required to still edit the output json file by removing the quotes.
- Ensure object definition are consistent.
- This script would be extremely helpful whenever eBay makes an update to the endpoint and we are required to edit the object definition on Workato.

## How does it work

- Go to an eBay endpoint page of a response payload you would like to convert i.e. [eBay get Inventory Item API page](https://developer.ebay.com/api-docs/sell/inventory/resources/inventory_item/methods/getInventoryItem)
- Find and copy the response payload show in the picture below into your clipboard ![alt text](https://github.com/kokwoo/securis_workato/blob/main/help1.png)
- Replace it with the file `ebay_version.json`
- Run the script with the instructions below
- You should see the output file `workato_object_definitions.json` as well as a pretty print of the object definition where you can use either to copy paste it into your connector SDK source code.


## Running the script

```
pip install -r requirements.txt
python main.py
```
