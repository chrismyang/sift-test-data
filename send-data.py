import sift
import sys
# import requests
# import time
# import radar
# from dateutil.relativedelta import relativedelta
import uuid
import random
# import csv

# return_action_url               = 'https://api.siftscience.com/v203/events?return_action=true'
# events_url                      = 'https://api.siftscience.com/v203/events'
# sift_science_sandbox_api_key    = '30acf2e32f8c207f'
# sift_science_production_api_key = '8e6580678c3f1983'
# client                          = None
# timeout                         = 2
# bad                             = True

#################################
# description:
# either create users or send events. 
# create users: send to a specified api key, env for all users in list, over the last year. 
# send events: 
# for a specified event type (either create account or create content)
# for a specified number of users
# for a specified api key and env
# add a random event data from the rows in the table


#################################

# Generate create account event for each user. 
# def create_users(users):
#   now = datetime.datetime.now()
#   last_year = now -relativedelta(years=1)
#   timestamp = radar.random_datetime(start=last_year, stop=now)
#   timestamp_millis = int(round(timestamp.time() *1000))

#   properties = []
#   # probably shouldn't loop here. Need to loop on sending data. 
#   # for all users in user list
#   for user in users
#   properties.append({
#     'time' : timestamp_millis,
#     '$user_id' : user
#     })
#   return properties

# def get_address():
#   # return a random row of data from the address file
#   address = []
#   address.append({
#     '$name'                   : get_name(),
#     '$address_1'              : address_file.split('#')[0]
#     '$city'                   : address_file.split('#')[1]
#     '$region'                 : address_file.split('#')[2]
#     '$zipcode'                : address_file.split('#')[3]
#     '$country'                : 'US'
#     })
#   return address

# def get_name():
#   first_name = #random row of data from first name file
#   last_name = #random row of data from last name file
#   return first_name + " " + last_name

# def order_items():
#   # return a random row of data from the items file
#   item = []
#   item.append({
#     '$item_id'                : items_file.split('#')[0]
#     '$product_title'          : items_file.split('#')[1]
#     'size'                    : items_file.split('#')[2]
#     'color'                   : items_file.split('#')[3]
#     '$price'                  : items_file.split('#')[4]
#     '$sku'                    : items_file.split('#')[5]
#     '$brand'                  : items_file.split('#')[6]
#     '$category'               : items_file.split('#')[7]
#     '$tags'                   : {
#                                 items_file.split('#')[8],
#                                 items_file.split('#')[9],
#                                 items_file.split('#')[10]
#                                 }
#     })
#   return item

# def create_order():
#   # Generate create order event 
#   # item info
#   # shipping address
#   # billing address
#   event_properties = []
#   order_id = uuid.uuid4()
#   amount = random.randrange(1000000,500000000) #between 10 and 500 dollars

#   event_properties.append({
#     '$order_id'               : order_id,
#     '$amount'                 : amount,
#     '$currency_code'          : 'USD'
#     '$billing_address'        : get_address()
#     '$shipping_address'       : get_address()
#     '$items'                  : order_items()
#     })

#   return event_properties

# def create_content():
#   event_properties = []
#   content_id = uuid.uuid4()
#   amount = random.randrange(10000000,500000000) #between 10 and 500 dollars

#   event_properties.append({
#     '$content_id'             : content_id,
#     '$amount'                 : amount
#     '$subject'                : content_file.split('#')[0]
#     '$content'                : content_file.split('#')[1]
#     '$categories'             : content_file.split('#')[2]
#     '$currency_code'          : 'USD'
#     })

def loadRandomContentFile():
    data = []
    with open("content.txt", "r") as myfile:
        data = myfile.readlines()
    return data

def create_random_id():
    return str(uuid.uuid4())

def create_random_amount():
    return random.randrange(10000000,500000000) # between 10 and 500 dollars

def select_random_lines_contents():
    content = loadRandomContentFile()
    random_line_number = random.randint(0, len(content) - 1)
    content_line = content[random_line_number]
    contents = content_line.split('#')
    return contents

def select_random_subject():
    return select_random_lines_contents()[0]

def select_random_content():
    return select_random_lines_contents()[1]    

def select_random_categories():
    return [ select_random_lines_contents()[2] ]

def add_properties(base, to_add):
    z = base.copy()
    z.update(to_add)
    return z

def sendEvent(api_key, event_name, properties):
    user_id = ""
    random_session_id = create_random_id()

    client = sift.Client(api_key)
    
    amended_properties = add_properties(properties, {
        '$user_id'                : user_id,
        '$session_id'             : random_session_id,
    })

    response = client.track(event_name, amended_properties) 
    print response
    return response

def create_content(api_key, environment, number_of_users):
    random_content_id = create_random_id()
    random_amount = create_random_amount()
    random_subject = select_random_subject()
    random_content = select_random_content()
    random_categories = select_random_categories()
    currency_code = "USD"

    sendEvent(api_key, "$create_content", {
        '$content_id'             : random_content_id,
        '$amount'                 : random_amount,
        '$subject'                : random_subject,
        '$content'                : random_content,
        '$categories'             : random_categories,
        '$currency_code'          : currency_code
    })

def create_order():
    random_order_id = create_random_id()
    random_amount = create_random_amount()
    currency_code = "USD"
    random_billing_address = create_random_address()
    random_shipping_address = create_random_address()
    random_items = create_random_items()

    sendEvent(api_key, "$create_order", {
        '$order_id'               : random_order_id,
        '$amount'                 : random_amount,
        '$currency_code'          : currency_code,
        '$billing_address'        : random_billing_address,
        '$shipping_address'       : random_shipping_address,
        '$items'                  : random_items
    })

def parse_args(argv):
    return (argv[1], argv[2], argv[3], int(argv[4]))

if __name__ == '__main__':
    (command, api_key, environment, number_of_users) = parse_args(sys.argv)
    
    print "command=" + command + " api_key=" + api_key + " environment=" + environment + " number_of_users=" + str(number_of_users)

    for i in range(0, number_of_users):
        if command == "create-content":
            create_content(api_key, environment, number_of_users)   
