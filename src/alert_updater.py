from models.alert import Alert
from models.item import Item

print(f"Item.get_by_id: {Item.get_by_id('6189bd4861ca4537b4b11734a1de15a4')}")

alerts = Alert.all()

for alert in alerts:
    alert.load_item_price()
    alert.notify_price_reached()
    print()
    print(alert.json())

if not alerts:
    print("no alerts")