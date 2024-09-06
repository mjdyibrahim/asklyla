if activity_type == "adventure":
    location = travel_to # assuming the user wants to do activities at their destination
    activities = get_adventure_activities(location, activity_type)
    # add code to display the activities to the user
#In the above code, get_adventure_activities() is a function that will make a request to the Adrenaline API to retrieve a list of adventure activities in the specified location. We can define this function as follows:

