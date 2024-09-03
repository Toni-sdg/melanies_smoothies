# Import python packages
import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

# Function to create a Snowflake session
def create_session():
    conn_params = {
        "account": "<your_account>",
        "user": "<your_user>",
        "password": "<your_password>",
        "role": "<your_role>",
        "warehouse": "<your_warehouse>",
        "database": "<your_database>",
        "schema": "<your_schema>"
    }
    return Session.builder.configs(conn_params).create()

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be:", name_on_order)

# Create Snowflake session
session = create_session()

# Retrieve fruit options from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
fruit_names = [row["FRUIT_NAME"] for row in my_dataframe.collect()]

# Display multiselect with fruit options
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:", fruit_names, max_selections=5
)

if ingredients_list:
    ingredients_string = ", ".join(ingredients_list)

    # Prepare and execute the insert statement
    my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders (ingredients, name_on_order)
    VALUES (%s, %s)
    """
    
    if st.button("Submit Order"):
        session.sql(my_insert_stmt, (ingredients_string, name_on_order)).collect()
        st.success('Your Smoothie is ordered', icon="✅")

