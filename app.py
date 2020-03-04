from models.item import Item

obra_dinn_url = "https://store.steampowered.com/app/653530/Return_of_the_Obra_Dinn/"
hitman2_url = "https://store.steampowered.com/app/863550/HITMAN_2/"
tag_name = "div"
query = {"class": "game_purchase_price price"}

obra_dinn = Item(obra_dinn_url, tag_name, query)
# obra_dinn.save_to_mongo()

# items_loaded = Item.all()

print(obra_dinn.load_price())
