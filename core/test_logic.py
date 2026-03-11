import os 
import django
# set up django environment 

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'core.settings')
django.setup()

from api.models import Product, Category
from api.serializers import OrderSerializer

def run_test():
    print("--- Starting Stock Validation Test---")

    # 1. setup the data
    # we use get_or_create to prevent errors if you run this script multiple times
    cat, _ = Category.objects.get_or_create(name="Tech", defaults={'slug': 'tech'})

    # create a fresh product for this tewst
    prod = Product.objects.create(
        name="Test Laptop",
        price=1000,
        stock_quantity=5,
        category=cat
    )


    # 2 simulate the post request data
    data = {
        "custoomer_name": "Jane Doe",
        "items": [{"product": prod.id, "quantity":2}]

    }


    # 3 run the serializer logic 
    serializer = OrderSerializer(data=data)
    if serializer.is_valid():
        serializer.save() # this triggers your custom create() and subtracts stock
        prod.refresh_from_db()

        print(f"SUCCESS! Order created.")
        print(f"Initial Stock: 5")
        print(f"Remaining Stock: {prod.stock_quantity}") # should be 3
    else:
        print(f"FAILED! Errors: {serializer.errors}")

    #optional: clean the test so the db does not get cluttered
    #prod.delete()


if __name__ == "__main__":
    run_test()            
