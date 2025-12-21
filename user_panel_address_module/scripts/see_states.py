import json
import requests

from user_panel_address_module.model.state import State

URL = "https://gist.githubusercontent.com/samanzamani/7ab3046ae1f94348d852bde959349f92/raw/26a54fc147bf918bbcb6e15f0d7c59fa9eac46c7/gistfile1.txt"


def run():
    response = requests.get(URL)
    data = json.loads(response.text)

    for item in data:
        province_name = item.get('province', '').strip()
        cities = item.get('cities', [])

        if not province_name:
            continue

        # ایجاد استان به عنوان والد
        province, _ = State.objects.get_or_create(title=province_name, parent=None)

        for city_name in cities:
            city_name = city_name.strip()
            if city_name:
                State.objects.get_or_create(title=city_name, parent=province)

    print("✅ استان‌ها و شهرها با موفقیت اضافه شدند.")
