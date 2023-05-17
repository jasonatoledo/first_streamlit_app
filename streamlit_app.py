import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy diner')

streamlit.header('Breakfast Menu')
streamlit.text("🥣 Omega 3 & Blueberry Oatmeal")
streamlit.text("🥗 Kale, Spinach, & Rocket Smoothie")
streamlit.text("🐔 Hard-Boiled Free-Range Egg")
streamlit.text("🥑🍞 Avocado Toast")
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# import pandas
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index("Fruit")

# pick list
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),["Avocado","Strawberries"])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# display table
streamlit.dataframe(fruits_to_show)


# create function
def get_fruityvice_data(this_fruit_choice):
  fruitvice_response = requests.get("https//fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

#New Section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input("What fruit would you like information about?")
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruitvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
# except URLError as e:
#   streamlit.error()
    
#     fruitvice_response = requests.get("https//fruityvice.com/api/fruit/" + fruit_choice)
#     fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
#     streamlit.dataframe(fruityvice_normalized)

  
# streamlit.write("The user entered", fruit_choice)

# # import requests
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

# # take the json version and normalize it
# fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
# # output it as table
# streamlit.dataframe(fruityvice_normalized)

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.text("The fruit load list contains:")
streamlit.dataframe(my_data_row)

# allow the end user to add a fruit to the list
add_my_fruit = streamlit.text_input("What fruit would you like to add?", "jackfruit")
streamlit.write('Thanks for adding', add_my_fruit)


