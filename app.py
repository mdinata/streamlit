# Andi Dinata 2024
# For educational purpose

import pandas as pd
import streamlit as st
st.set_page_config(layout='wide')

with st.sidebar:
    st.subheader("Colab Coding")
    st.write("Ruko Magnetica Square A21\nLippo Cikarang")

tab1,tab2 = st.tabs(['Home','Project Showcase'])

with tab1:
    try:
        with open('README.md', "r") as file:
            markdown_content = file.read()
        st.markdown(markdown_content, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"The file `{file_path}` was not found.")
        
with tab2:
    with st.expander("Marketplace"):
        @st.cache_data
        def get_data():
            data = pd.read_excel('dataset_marketplace.xlsx')
            return data
        
        data = get_data()
        
        stores = data['store'].unique()
        category = sorted(list(data['category'].unique()),reverse=False)
        product = sorted(list(data['product'].unique()),reverse=False)
    
        with st.container(border=True):
            st.write("Filters")
            col1,col2,col3,col4 = st.columns(4)
            with col1:
                filter_store = st.selectbox("Filter Store",options=stores,index=None)
            with col2:
                filter_category = st.selectbox("Filter Category",options=category, index=None)
            with col3:
                filter_product = st.selectbox("Filter Product",options=product,index=None)
        
            if filter_category is None:
                min_price=data['price'].min()
                max_price=data['price'].max()
            else:
                min_price = data[data['category'] == filter_category]['price'].min()
                max_price = data[data['category'] == filter_category]['price'].max()
            with col4:   
                filter_price = st.slider("Price Filter",
                                        min_value=min_price,
                                        max_value=max_price,
                                        value=max_price)

        def filter_data(data):
            filtered_data = data.copy()
        
            if filter_store:
                filtered_data = filtered_data[filtered_data['store'] == filter_store]
            if filter_category:
                filtered_data = filtered_data[filtered_data['category'] == filter_category]
            if filter_product:
                filtered_data = filtered_data[filtered_data['product'] == filter_product]
            if filter_price:
                filtered_data = filtered_data[filtered_data['price'] <= filter_price]
                filtered_data = filtered_data.sort_values(by='price')
        
            return filtered_data
        
        filtered_data = filter_data(data)
        
        def grid_layout(cols, rows, filtered_data):
            st.header("🏪 Welcome to our Marketplace")
            st.write(f"There are {len(filtered_data)} products listed")
            for nr in range(rows):
                with st.container():
                    columns = st.columns(cols)
                    for nc,c in enumerate(columns):
                        with c:
                            with st.container(border=True):
                                row_data = filtered_data.iloc[nr * cols + nc]
                                st.image(f"images/{row_data['picture']}")
                                st.write(f"{row_data['product']}")
                                st.write(f"{row_data['description']}")
                                st.write(f"**Store:** {row_data['store']}")
                                st.write(f"**Price:** {row_data['price']}")
                                if st.button("🛒Cart",key=f"btncart{nr * cols + nc}"):
                                    st.write("Added to Cart")
                                if st.button("💲Buy",key=f"btnbuy{nr * cols + nc}"):
                                    st.write("Thank you")
        cols = 5
        rows = len(filtered_data) // cols
        
        grid_layout(cols, len(filtered_data) // cols, filtered_data)


    conversion_factor = {
                        'distance': {
                            'mm': 1,
                            'cm': 0.1,
                            'm': 0.001,
                            'km': 0.000001,
                            'inch': 0.0393701,
                            'feet': 0.00328084,
                            'yards': 0.00109361,
                            'miles': 6.2137e-7,
                            'AU': 6.68459e-12,
                            'light_year': 1.057e-16},
                        'weight': {
                            'gr': 1,
                            'kg': 0.001,
                            'mg': 1000,
                            'ton': 1e-6,
                            'pound': 0.00220462,
                            'ounce': 0.035274},
                        'speed': {
                            'm/s': 1,
                            'km/h': 3.6,
                            'miles/h': 2.23694,
                            'knot': 1.94384,
                            'light_speed': 3.33564e-9},
                        'volume':{
                            'lt': 1,
                            'ml': 1000,
                            'tbsp': 67.628,
                            'tsp': 202.884,
                            'm3': 0.001,
                            'km3': 1e-12},
                        'planet':{
                            'earth': 1,
                            'mercury': 0.056,
                            'venus': 0.866,
                            'mars': 0.151,
                            'jupiter': 1321,
                            'saturn': 763.6,
                            'uranus': 63.1,
                            'neptune': 57.7,
                            'sun': 1.4122e18},
                        'temperature': ['Celsius', 'Fahrenheit', 'Kelvin']}
    def show_formula(category, base_unit=None, target_unit=None):
        if category == 'temperature' and base_unit and target_unit:
            if base_unit == 'Celsius' and target_unit == 'Fahrenheit':
                st.latex(r'\text{F} = \text{C} \times \frac{9}{5} + 32')
            elif base_unit == 'Celsius' and target_unit == 'Kelvin':
                st.latex(r'\text{K} = \text{C} + 273.15')
            elif base_unit == 'Fahrenheit' and target_unit == 'Celsius':
                st.latex(r'\text{C} = (\text{F} - 32) \times \frac{5}{9}')
            elif base_unit == 'Fahrenheit' and target_unit == 'Kelvin':
                st.latex(r'\text{K} = (\text{F} - 32) \times \frac{5}{9} + 273.15')
            elif base_unit == 'Kelvin' and target_unit == 'Celsius':
                st.latex(r'\text{C} = \text{K} - 273.15')
            elif base_unit == 'Kelvin' and target_unit == 'Fahrenheit':
                st.latex(r'\text{F} = (\text{K} - 273.15) \times \frac{9}{5} + 32')
            else:
                st.latex(r'\text{Converted Value} = \text{Input Value}')
        else:
            st.latex(r'''
            \text{Converted Value} = \frac{\text{Input Value}}{\text{Conversion Factor of Base Unit}} \times \text{Conversion Factor of Target Unit}
            ''')

    def convert(input_value, category, base_unit, target_unit):
        if category == 'temperature':
            if base_unit == 'Celsius':
                if target_unit == 'Fahrenheit':
                    return input_value * 9 / 5 + 32
                elif target_unit == 'Kelvin':
                    return input_value + 273.15
            elif base_unit == 'Fahrenheit':
                if target_unit == 'Celsius':
                    return (input_value - 32) * 5 / 9
                elif target_unit == 'Kelvin':
                    return (input_value - 32) * 5 / 9 + 273.15
            elif base_unit == 'Kelvin':
                if target_unit == 'Celsius':
                    return input_value - 273.15
                elif target_unit == 'Fahrenheit':
                    return (input_value - 273.15) * 9 / 5 + 32
            return input_value 
        else:
            return input_value / conversion_factor[category][base_unit] * conversion_factor[category][target_unit]

    with st.expander("Converter"):
        if 'result' not in st.session_state:
            st.session_state.result = 0.0
        
        with st.container():
            col0, col1, col2, col3, col4 = st.columns(5)
        
            with col0:
                category = st.radio("Category", list(conversion_factor.keys()), key="category")
        
            with col1:
                input_value = st.number_input("Input Value", min_value=0.0, step=0.1, key="input_value")
        
            with col2:
                if category == 'temperature':
                    base_unit = st.radio("From", conversion_factor[category], key="base_unit")
                else:
                    base_unit = st.radio("From", conversion_factor[category], key="base_unit")
        
            with col3:
                if category == 'temperature':
                    target_unit = st.radio("To", conversion_factor[category], key="target_unit")
                else:
                    target_unit = st.radio("To", conversion_factor[category], key="target_unit")
        
            with col4:
                st.write("Converted Value")
                if base_unit and target_unit:
                    st.session_state.result = convert(input_value, category, base_unit, target_unit)
                if category == 'planet':
                    st.write(f'{target_unit} volume is {st.session_state.result:#,.3f} times of {base_unit}')
                else:
                    st.write(f'{st.session_state.result:#,.3f} {target_unit}')
        
        show_formula(category, base_unit, target_unit)
        
    with st.expander("Cashier"):
        data = pd.read_excel('dataset_cashier.xlsx')

        if 'transaction' not in st.session_state:
            st.session_state['transaction'] = pd.DataFrame(columns=['description', 'price', 'quantity', 'amount'])

        cashier_col1, cashier_col2, cashier_col3 = st.columns(3)

        with cashier_col1:
            with st.container(border=True,height=450):
                input_product = st.number_input("Product Code", step=1, value=0)
                preview_data = data[data['product_id'] == input_product][['description', 'price']]

                st.write('Product Information')
                st.dataframe(preview_data,use_container_width=True,hide_index=True)

                input_quantity = st.number_input("Quantity", step=1, value=0)

                if st.button("Add"):
                    if not preview_data.empty and input_quantity > 0:
                        description = preview_data['description'].values[0]
                        price = preview_data['price'].values[0]
                        
                        existing_item = st.session_state['transaction']['description'] == description

                        if existing_item.any():
                            index = st.session_state['transaction'][existing_item].index[0]
                            st.session_state['transaction'].at[index, 'quantity'] += input_quantity
                            st.session_state['transaction'].at[index, 'amount'] = (st.session_state['transaction'].at[index, 'quantity'] * price)
                        else:
                            cart = pd.DataFrame({
                                'description': [description],
                                'price': [price],
                                'quantity': [input_quantity],
                                'amount': [price * input_quantity]
                            })
                            st.session_state['transaction'] = pd.concat([st.session_state['transaction'], cart], ignore_index=True)
                    else:
                        st.warning("Invalid input")
        with cashier_col2:
            with st.container(height=450, border=True):
                st.write('Cart')
                st.dataframe(st.session_state['transaction'],hide_index=True,use_container_width=True)
        with cashier_col3:
            with st.container(border=True):
                total_amount = st.session_state['transaction']['amount'].sum()
                st.write("Total Amount")
                st.subheader(f"**${total_amount:.2f}**")
            with st.container(height=320,border=True):
                payment_input = st.number_input("Payment:",step=1)
                if st.button("Pay"):
                    if payment_input >= total_amount:
                        return_amount = payment_input - total_amount
                        receipt = "----- Receipt -----\n"
                        receipt += "Items Purchased:\n"
                        for idx, row in st.session_state['transaction'].iterrows():
                            receipt += f"- {row['quantity']}x {row['description']} (${row['amount']:.2f})\n"
                            
                        receipt += f"\nTotal: ${total_amount:.2f}\n"
                        receipt += f"Payment: ${payment_input:.2f}\n"
                        receipt += f"Return: ${return_amount:.2f}\n"
                        receipt += "-------------------"

                        st.text(receipt)
                    else:
                        st.error("Insufficient payment")
                if st.button("Clear"):
                    st.session_state['transaction'] = pd.DataFrame(columns=['description', 'price', 'quantity', 'amount'])
                    st.success("Transaction cleared")
    
