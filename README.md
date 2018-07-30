# mccptester

This web app is developed for the monitoring of the Multi-Channel-Commerce-Platform (MCCP) developed. 
Inventory is tracked against IMS/WMS
Shipment status is tracked against TMS

Besides the above, it also caters for Shopee new open platform authorisation. This is an interim solution while SmartOSC works on the final version

Below is a short summary of the items monitored.

url: mccptester.herokuapp.com

## Development
Server side code developed on python.
API end points hosted using Flask
HTML, CSS and Javascript hosted using Flask

## Product info
### 1. Account
Link your MCCP account with you IMS and TMS account

### 2. Inventory
Extracts a list of all products from MCCP and its inventory from MCCP and IMS. Discrepancies are highlighted and there is the option to conduct the sync.

### 3. Orders
Not developed yet

### 4. Shipments
Not developed yet

### 5. Shopee
Use this is extract shop_id. This authorises our app to access the Shopee account. You will be redirected to shopee for login after clicking submit. Upon successful login, you will be redirected back to the page and the shop_id will be displayed
