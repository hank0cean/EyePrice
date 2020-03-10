from models.alert import Alert

alert = Alert("6189bd4861ca4537b4b11734a1de15a4", 20)
alert.save_to_mongo()
