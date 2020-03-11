from models.alert import Alert

alerts = Alert.all()

for alert in alerts:
    print(alert.item_id)
    print(alert.item)
    alert.load_item_price()
    alert.notify_price_reached()

if not alerts:
    print("no alerts")