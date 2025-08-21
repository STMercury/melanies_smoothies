# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Yout Smoothie!:cup_with_straw:")
st.write(
  """
  Choose the fuits you want in your custom Smoothie!
  """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('Your name in the Smoothie is: ', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingerients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)

time_to_insert = st.button('Submit Order') 



if ingerients_list and time_to_insert == True:
    ingerients_string = ''
    for fruit_chosen in ingerients_list:
        ingerients_string += fruit_chosen + ' '
    my_insert_stmt = """
    INSERT INTO smoothies.public.orders (ingredients, name_on_order)
    VALUES ('""" + ingerients_string + """', '""" + name_on_order + """')
    """
    if ingerients_string:
        session.sql(my_insert_stmt).collect()
        st.success('YOUR SMOOTHIE IS ORDERED!', icon="✅")
