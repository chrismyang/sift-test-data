import sift
import sys
import uuid
import random

def loadRandomContentFile(content_filename):
    data = []
    with open(content_filename, "r") as myfile:
        data = myfile.readlines()
    return data

def create_random_id():
    return str(uuid.uuid4())

def create_random_amount():
    return random.randrange(10000000,500000000) # between 10 and 500 dollars

def select_random_lines_contents(content_filename):
    content = loadRandomContentFile(content_filename)
    random_line_number = random.randint(0, len(content) - 1)
    content_line = content[random_line_number]
    contents = content_line.split('#')
    return contents

def select_random_subject():
    return select_random_lines_contents("content.txt")[0]

def select_random_content():
    return select_random_lines_contents("content.txt")[1]    

def select_random_categories():
    return [ select_random_lines_contents("content.txt")[2] ]

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

def create_content(api_key, environment):
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

def create_random_address():
    address_list = select_random_lines_contents("addresses.csv")

    return {
        '$address_1'              : address_list[0],
        '$city'                   : address_list[1],
        '$region'                 : address_list[2],
        '$zipcode'                : address_list[3],
        '$country'                : 'US'
    }

def create_random_items():
    item_list = select_random_lines_contents("items.txt")
    tags = [item_list[8], item_list[9], item_list[10]]

    item = {
        '$item_id'                : item_list[0],
        '$product_title'          : item_list[1],
        'size'                    : item_list[2],
        'color'                   : item_list[3],
        '$price'                  : item_list[4],
        '$sku'                    : item_list[5],
        '$brand'                  : item_list[6],
        '$category'               : item_list[7],
        '$tags'                   : tags
    }
  
    return [ item ]

def create_order(api_key, environment):
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

def print_usage():
    print "Usage: python send-data.py [create-order | create-content] [api_key] [environment] [number_of_users]"

def parse_args(argv):
    if len(argv) < 5:
        print_usage()
        sys.exit(1)
    else:
        return (argv[1], argv[2], argv[3], int(argv[4]))

if __name__ == '__main__':
    (command, api_key, environment, number_of_users) = parse_args(sys.argv)
    
    print "command=" + command + " api_key=" + api_key + " environment=" + environment + " number_of_users=" + str(number_of_users)

    for i in range(0, number_of_users):
        if command == "create-content":
            create_content(api_key, environment)   
        elif command == "create-order":
            create_order(api_key, environment)
        else:
            raise Exception("Unrecognized command " + command)    
