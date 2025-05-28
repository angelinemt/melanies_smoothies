# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests


# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  """ Choose the fruits you want in your custom Smoothie! """
)

#Add a namebox for Smoothie Orders
name_on_order = st.text_input('Name of Smoothie: ')
st.write('The name on your Smoothie will be: ', name_on_order)

#Display the Fruit Options List in your Streamlit 
cnx = st.connection("snowflake")
session = cnx.session()


my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON')) 
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

#Convert the Snowpark Dataframe to a Pandas Dataframe so we can use the LOC function  
pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()


# To add a multiselect 
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients: '
    , my_dataframe
    , max_selections = 5
)

#changing the LIST to a STRING 
#!! - dont put space in between the qoutes
ingredients_string = ''

#to see the result fromt the multi-select 
#to clean the bracket in the output, we put IF block. 
#IF block - it's called BLOCK because everything below it (that is indented) will be dependent on the IF statement. 
if ingredients_list: 
    
    #Convert list to a string
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
      
        st.subheader(fruit_chosen + ' Nutrition Information ')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
      
#st.write(ingredients_string)

#SQL STATEMENT 
my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
    values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

time_to_insert = st.button('Submit Order')

#this statement will put the output to the snowflake and will reflect there. 
if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")
