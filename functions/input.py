def collect_cofficiency(view_list, building_name_list):
    age_cofficiency = input("Please input the age cofficency (percentage per 1 year younger than reference flat)")
    size_cofficiency = input("Please input the size cofficency (percentage per 1 unit larger than reference flat)")
    floor_cofficiency = input("Please input the floor cofficency (percentage per 1 floor increase) than reference flat")
    headroom_cofficency = input("Please input the headroom cofficency (percentage per )")
    view_dictionary = {view: input(f"Please input the {view} cofficency (percentage per 1 {view} increase)") for view in view_list}
    building_dictionary = {input(f"Please input the {building_name} cofficency base 100)") for building_name in building_name_list}
    return age_cofficiency,size_cofficiency, floor_cofficiency, view_dictionary, headroom_cofficency, building_dictionary