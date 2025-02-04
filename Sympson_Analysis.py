import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re
from matplotlib.colors import ListedColormap
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import random
import numpy as np
from PIL import Image

st.set_page_config(page_title="The Simpsons - Analysis",
                   page_icon="bar_chart:",
                   layout="wide")





df= pd.read_csv("simpsons_episodes.csv")
df['original_air_date'] = pd.to_datetime(df['original_air_date'])
df['year'] = df['original_air_date'].dt.year

#______________ Side bar ___________
st.sidebar.title("The Simpsons Analysis")
st.sidebar.header("Please filter here:")
category = st.sidebar.selectbox(
    "Category",
    [" ", "Season", "Characters", "Writers", "Directors", "Episodes", "Correlations"]
)


if category == "Correlations":
    feature_options = [" ", "Viewers & Ratings", "Viewers & Season", "Season & Ratings"] 
elif category == "Others":
    feature_options = [" ", "ABC", "General Dashboard"] 
else:
    feature_options = [" ", "Top 5 (More popular)", "Bottom 5 (Less popular)", "Overall Performance"]

feature = st.sidebar.selectbox(
    "Feature to analyze",
    feature_options
)

# Display image if no category is selected
if category == " ":
    image_path = "images_simpsons/01. Intro.jpg"
    image = Image.open(image_path)
    st.image(image, use_column_width=True)





###Season
# Filter info by user selection
if category == "Season" and feature == "Top 5 (More popular)":
    top_5_us_viewers = df.groupby("season")["us_viewers_in_millions"].mean().nlargest(5).reset_index()
    fig3 = px.bar(top_5_us_viewers, x="season", y="us_viewers_in_millions", title="Top 5 Seasons by US Viewers (Millions)")
    fig3.update_layout(width=450, height=450)  # graphic size
    
    
    st.write("\n")  # space between graphics
    
    top_5_imdb_ratings = df.groupby("season")["imdb_rating"].mean().nlargest(5).reset_index()
    fig1 = px.bar(top_5_imdb_ratings, x="season", y="imdb_rating", title="Top 5 Seasons by Imdb Rating")
    
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.plotly_chart(fig3, use_container_width=True)
        

if category == "Season" and feature == "Bottom 5 (Less popular)":
    top_5_us_viewers = df.groupby("season")["us_viewers_in_millions"].mean().reset_index()
    top_5_us_viewers = top_5_us_viewers.sort_values(by="us_viewers_in_millions", ascending=True).head(5)
    fig3 = px.bar(top_5_us_viewers, x="season", y="us_viewers_in_millions", title="Bottom 5 Seasons by US Viewers (Millions)")
    fig3.update_layout(width=450, height=450, bargap=0.1)  
    
    
    
    top_5_imdb_ratings = df.groupby("season")["imdb_rating"].mean().nsmallest(5).reset_index()
    top_5_imdb_ratings = top_5_imdb_ratings.dropna()
    fig1 = px.bar(top_5_imdb_ratings, x="season", y="imdb_rating", title="Bottom 5 Seasons by Imdb Rating")
    
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.plotly_chart(fig3, use_container_width=True)

if category == "Season" and feature == "Overall Performance":
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    # Calculate the average of the values in "us_viewers_in_millions" grouped by "year"
    year_avg_us_viewers = df.groupby('year')['us_viewers_in_millions'].mean().reset_index()

    # Calculate the average ratings grouped by year
    year_avg_ratings = df.groupby('year')[['imdb_rating', 'tmdb_rating']].mean().reset_index()

    # Create a figure with subplots
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add bar trace for average US viewers
    fig.add_trace(go.Bar(x=year_avg_us_viewers['year'], y=year_avg_us_viewers['us_viewers_in_millions'],
                         name='Average US Viewers (Millions)',
                         marker_color='blue'), secondary_y=False)

    # Add line trace for average IMDb rating
    fig.add_trace(go.Scatter(x=year_avg_ratings['year'], y=year_avg_ratings['imdb_rating'],
                             mode='lines+markers',
                             name='Average IMDb Rating',
                             line=dict(color='red')), secondary_y=True)


    # Update layout
    fig.update_layout(title='Average US Viewers and IMDb Ratings Over Time',
                      xaxis_title='Year',
                      yaxis_title='Average US Viewers (Millions)',
                      yaxis2_title='Average Rating',
                      legend=dict(x=0, y=1.4),
                      title_x=0.5)

    # Show the figure
    st.plotly_chart(fig, use_container_width=True)

if category == "Characters" and feature == "Top 5 (More popular)":
    
    # Subtitle
    st.subheader("Top 5 Characters According to number of views")
    # List of characters
    characters_list = ["Homer", "Marge", "Bart", "Lisa", "Maggie", "Ned", "Maude", "Rod", "Todd", "Burns", "Smithers", "Krusty", "Milhouse", "Nelson", "Ralph", "Wiggum", "Lou", "Eddie", "Moe", "Lenny", "Carl", "Barney", "Lovejoy", "Helen", "Clancy", "Seymour", "Edna", "Patty", "Selma", "Quimby", "Sideshow Bob", "Jimbo", "Kearney", "Dolph", "Willie", "Dr. Hibbert", "Bernice", "Itchy", "Scratchy", "Apu", "Manjula", "Comic Book Guy", "Frink", "Snake", "Hans", "Uter", "Duffman", "Bumblebee Man", "Squeaky-Voiced Teen", "Jasper", "Fat Tony", "Disco Stu", "Gil", "Crazy Cat Lady", "Brandine", "Cletus", "Luann", "Akira", "Dr. Nick", "Chalmers", "Rainier Wolfcastle", "Blue-Haired Lawyer", "Judge Snyder", "Troy McClure", "Lindsey Naegle", "Kirk", "Artie Ziff", "Herb Powell", "Cecil", "Mona", "Amber Dempsey", "Laura Powers", "Jessica", "Darcy", "Hugo", "Bleeding Gums Murphy", "Rabbi Krustofski", "Astronaut", "Tom", "Lurleen Lumpkin", "Jub-Jub", "Scott Christian", "Dewey Largo", "Lunchlady Doris", "Otto", "Wendell", "Lewis", "Sherri", "Terri", "Database", "Martin Prince", "Allison Taylor", "Jasper Beardley", "Groundskeeper", "Willie", "Dr.", "Hibbert", "Blue", "Lawyer", "Judge", "Snyder", "Troy", "McClure", "Lindsey", "Naegle", "Kirk", "Artie", "Ziff", "Herb", "Powell", "Cecil", "Mona", "Amber", "Dempsey", "Laura", "Powers", "Jessica", "Darcy", "Hugo", "Rabbi", "Krustofski", "Astronaut", "Tom", "Jub-Jub", "Scott", "Christian", "Dewey", "Largo", "Lunchlady", "Doris", "Otto", "Wendell", "Lewis", "Sherri", "Terri", "Database", "Martin", "Prince", "Allison", "Taylor", "Jasper"]

    # Function to find characters in the description
    def find_characters(description):
        characters = []
        for character in characters_list:
            if re.search(r'\b{}\b'.format(re.escape(character)), description, re.IGNORECASE):
                characters.append(character)
        return characters

    # Create the new "characters" column
    df['characters'] = df['description'].apply(find_characters)

    # Create a new DataFrame with the sum of 'us_viewers_in_millions' per character
    characters_views = df.explode('characters').groupby('characters')['us_viewers_in_millions'].sum().reset_index()

    # Sort the DataFrame by the sum of 'us_viewers_in_millions' in descending order
    characters_views = characters_views.sort_values(by='us_viewers_in_millions', ascending=False)

     # Select the top 5 characters and reset the index to start from 1
    characters_views_top_5 = characters_views.head(5).reset_index(drop=True).rename_axis('Rank')

    # Add 1 to the index to start from 1
    characters_views_top_5.index += 1

    # Display the DataFrame
    st.dataframe(characters_views_top_5)

    # Load and display image
    image_path = "images_simpsons/1.jpg"
    image = Image.open(image_path)
    st.image(image, caption=' ', use_column_width=True)
    
    # Define the color map
    color_map = {
        "Homer": "yellow",
        "Bart": "blue",
        "Lisa": "red",
        "Marge": "green",
        "Burns": "lightblue"
    }

    # Create a bar chart 
    fig = px.bar(characters_views_top_5, x='characters', y='us_viewers_in_millions',
                title='Top 5 Characters by US Viewers in Millions',
                color='characters', color_discrete_map=color_map)

    # Set the x-axis label
    fig.update_xaxes(title_text='Characters')

    # Set the y-axis label
    fig.update_yaxes(title_text='US Viewers in Millions')

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
    


    #IMDb Rating
    # Subtitle
    st.subheader("Top 5 Characters According to IMDb Rating")
    # Convert the lists in the 'characters' column to individual values
    df2 = df.explode('characters')
    # Create a new DataFrame with the average of 'imdb_rating' per character
    characters_imdb_avg = df2.groupby('characters')['imdb_rating'].mean().reset_index()

    # Sort the DataFrame by the average of 'imdb_rating' in descending order
    characters_imdb_avg = characters_imdb_avg.sort_values(by='imdb_rating', ascending=False)

    # Select the top 5 characters and reset the index to start from 1
    characters_imdb_avg_top_5 = characters_imdb_avg.head(5).reset_index(drop=True)

    # Add 1 to the index to start from 1
    characters_imdb_avg_top_5.index += 1

    # Display the DataFrame with the average of 'imdb_rating' per character
    st.dataframe(characters_imdb_avg_top_5)
    
    # Load and display image
    image_path = "images_simpsons/2.jpg"
    image = Image.open(image_path)
    st.image(image, caption=' ', use_column_width=True)
    # Define a list of random colors
    random_colors = []
    for _ in range(5):
        random_colors.append(f"rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})")

    # Create a bar chart 
    fig = px.bar(characters_imdb_avg_top_5, x='characters', y='imdb_rating',
                title='Top 5 Characters by IMDb Rating',
                color='characters', color_discrete_sequence=random_colors)

    # Set the x-axis label
    fig.update_xaxes(title_text='Characters')

    # Set the y-axis label
    fig.update_yaxes(title_text='IMDb Rating')

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)


if category == "Characters" and feature == "Bottom 5 (Less popular)":
    
    # Subtitle
    st.subheader("Bottom 5 Characters According to number of views")

     # List of characters
    characters_list = ["Homer", "Marge", "Bart", "Lisa", "Maggie", "Ned", "Maude", "Rod", "Todd", "Burns", "Smithers", "Krusty", "Milhouse", "Nelson", "Ralph", "Wiggum", "Lou", "Eddie", "Moe", "Lenny", "Carl", "Barney", "Lovejoy", "Helen", "Clancy", "Seymour", "Edna", "Patty", "Selma", "Quimby", "Sideshow Bob", "Jimbo", "Kearney", "Dolph", "Willie", "Dr. Hibbert", "Bernice", "Itchy", "Scratchy", "Apu", "Manjula", "Comic Book Guy", "Frink", "Snake", "Hans", "Uter", "Duffman", "Bumblebee Man", "Squeaky-Voiced Teen", "Jasper", "Fat Tony", "Disco Stu", "Gil", "Crazy Cat Lady", "Brandine", "Cletus", "Luann", "Akira", "Dr. Nick", "Chalmers", "Rainier Wolfcastle", "Blue-Haired Lawyer", "Judge Snyder", "Troy McClure", "Lindsey Naegle", "Kirk", "Artie Ziff", "Herb Powell", "Cecil", "Mona", "Amber Dempsey", "Laura Powers", "Jessica", "Darcy", "Hugo", "Bleeding Gums Murphy", "Rabbi Krustofski", "Astronaut", "Tom", "Lurleen Lumpkin", "Jub-Jub", "Scott Christian", "Dewey Largo", "Lunchlady Doris", "Otto", "Wendell", "Lewis", "Sherri", "Terri", "Database", "Martin Prince", "Allison Taylor", "Jasper Beardley", "Groundskeeper", "Willie", "Dr.", "Hibbert", "Blue", "Lawyer", "Judge", "Snyder", "Troy", "McClure", "Lindsey", "Naegle", "Kirk", "Artie", "Ziff", "Herb", "Powell", "Cecil", "Mona", "Amber", "Dempsey", "Laura", "Powers", "Jessica", "Darcy", "Hugo", "Rabbi", "Krustofski", "Astronaut", "Tom", "Jub-Jub", "Scott", "Christian", "Dewey", "Largo", "Lunchlady", "Doris", "Otto", "Wendell", "Lewis", "Sherri", "Terri", "Database", "Martin", "Prince", "Allison", "Taylor", "Jasper"]

    # Function to find characters in the description
    def find_characters(description):
        characters = []
        for character in characters_list:
            if re.search(r'\b{}\b'.format(re.escape(character)), description, re.IGNORECASE):
                characters.append(character)
        return characters

    # Create the new "characters" column
    df['characters'] = df['description'].apply(find_characters)

    # Convert the lists in the 'characters' column to individual values
    df2 = df.explode('characters')

    # Create a new DataFrame with the sum of 'us_viewers_in_millions' per character
    characters_views = df.explode('characters').groupby('characters')['us_viewers_in_millions'].sum().reset_index()

    # Sort the DataFrame by the sum of 'us_viewers_in_millions' in descending order
    characters_views = characters_views.sort_values(by='us_viewers_in_millions', ascending=False)

     # Select the top 5 characters and reset the index to start from 1
    characters_views_bottom_5 = characters_views.tail(5).reset_index(drop=True).rename_axis('Rank')

    # Add 1 to the index to start from 1
    characters_views_bottom_5.index += 1

    # Display the DataFrame
    st.dataframe(characters_views_bottom_5)

    # Load and display image
    image_path = "images_simpsons/3.jpg"
    image = Image.open(image_path)
    st.image(image, caption=' ', use_column_width=True)
    # Define a list of random colors
    random_colors = []
    for _ in range(5):
        random_colors.append(f"rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})")

    # Create a bar chart 
    fig = px.bar(characters_views_bottom_5, x='characters', y='us_viewers_in_millions',
                title='Bottom 5 Characters by US Viewers in Millions',
                color='characters', color_discrete_sequence=random_colors)

    # Set the x-axis label
    fig.update_xaxes(title_text='Characters')

    # Set the y-axis label
    fig.update_yaxes(title_text='US Viewers in Millions')

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)

    #IMDb Rating
    
    # Subtitle
    st.subheader("Bottom 5 Characters According to IMDb Rating")

    # Convert the lists in the 'characters' column to individual values
    df2 = df.explode('characters')
    # Create a new DataFrame with the average of 'imdb_rating' per character
    characters_imdb_avg = df2.groupby('characters')['imdb_rating'].mean().reset_index()

    # Sort the DataFrame by the average of 'imdb_rating' in descending order
    characters_imdb_avg = characters_imdb_avg.sort_values(by='imdb_rating', ascending=False)

    # Select the bottom 5 characters and reset the index to start from 1
    characters_imdb_avg_bottom_5 = characters_imdb_avg.tail(5).reset_index(drop=True)

    # Add 1 to the index to start from 1
    characters_imdb_avg_bottom_5.index += 1

    # Show DataFrame with the average of 'imdb_rating' per character
    st.dataframe(characters_imdb_avg_bottom_5)

    # Load and display image
    image_path = "images_simpsons/4.jpg"
    image = Image.open(image_path)
    st.image(image, caption=' ', use_column_width=True)

    # Define a list of random colors
    random_colors = []
    for _ in range(5):
        random_colors.append(f"rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})")

    # Create a bar chart 
    fig = px.bar(characters_imdb_avg_bottom_5, x='characters', y='imdb_rating',
                title='Bottom 5 Characters by IMDb Rating',
                color='characters', color_discrete_sequence=random_colors)

    # Set the x-axis label
    fig.update_xaxes(title_text='Characters')

    # Set the y-axis label
    fig.update_yaxes(title_text='IMDb Rating')

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)

if category == "Characters" and feature == "Overall Performance":
   
    # Load and display image
    image_path = "images_simpsons/5.jpg"
    image = Image.open(image_path)
    st.image(image, caption=' ', use_column_width=True)
   
    
    # List of characters
    characters_list = ["Homer", "Marge", "Bart", "Lisa", "Maggie", "Ned", "Maude", "Rod", "Todd", "Burns", "Smithers", "Krusty", "Milhouse", "Nelson", "Ralph", "Wiggum", "Lou", "Eddie", "Moe", "Lenny", "Carl", "Barney", "Lovejoy", "Helen", "Clancy", "Seymour", "Edna", "Patty", "Selma", "Quimby", "Sideshow Bob", "Jimbo", "Kearney", "Dolph", "Willie", "Dr. Hibbert", "Bernice", "Itchy", "Scratchy", "Apu", "Manjula", "Comic Book Guy", "Frink", "Snake", "Hans", "Uter", "Duffman", "Bumblebee Man", "Squeaky-Voiced Teen", "Jasper", "Fat Tony", "Disco Stu", "Gil", "Crazy Cat Lady", "Brandine", "Cletus", "Luann", "Akira", "Dr. Nick", "Chalmers", "Rainier Wolfcastle", "Blue-Haired Lawyer", "Judge Snyder", "Troy McClure", "Lindsey Naegle", "Kirk", "Artie Ziff", "Herb Powell", "Cecil", "Mona", "Amber Dempsey", "Laura Powers", "Jessica", "Darcy", "Hugo", "Bleeding Gums Murphy", "Rabbi Krustofski", "Astronaut", "Tom", "Lurleen Lumpkin", "Jub-Jub", "Scott Christian", "Dewey Largo", "Lunchlady Doris", "Otto", "Wendell", "Lewis", "Sherri", "Terri", "Database", "Martin Prince", "Allison Taylor", "Jasper Beardley", "Groundskeeper", "Willie", "Dr.", "Hibbert", "Blue", "Lawyer", "Judge", "Snyder", "Troy", "McClure", "Lindsey", "Naegle", "Kirk", "Artie", "Ziff", "Herb", "Powell", "Cecil", "Mona", "Amber", "Dempsey", "Laura", "Powers", "Jessica", "Darcy", "Hugo", "Rabbi", "Krustofski", "Astronaut", "Tom", "Jub-Jub", "Scott", "Christian", "Dewey", "Largo", "Lunchlady", "Doris", "Otto", "Wendell", "Lewis", "Sherri", "Terri", "Database", "Martin", "Prince", "Allison", "Taylor", "Jasper"]
    st.subheader(r"According to number of views   |   |              According to IMDb Rating")
    # Function to find characters in the description
    def find_characters(description):
        characters = []
        for character in characters_list:
            if re.search(r'\b{}\b'.format(re.escape(character)), description, re.IGNORECASE):
                characters.append(character)
        return characters

    # Create the new "characters" column
    df['characters'] = df['description'].apply(find_characters)

    # Convert the lists in the 'characters' column to individual values
    df2 = df.explode('characters')

    # Create a new DataFrame with the sum of 'us_viewers_in_millions' per character
    characters_views = df.explode('characters').groupby('characters')['us_viewers_in_millions'].sum().reset_index()

    # Sort the DataFrame by the sum of 'us_viewers_in_millions' in descending order
    characters_views = characters_views.sort_values(by='us_viewers_in_millions', ascending=False)
    # Reset the index and rename the index column
    characters_views = characters_views.reset_index(drop=True).rename_axis('Rank')
    # Add 1 to the index to start from 1
    characters_views.index += 1

   

    # Create a new DataFrame with the average of 'tmdb_rating' per character
    characters_imdb_avg = df2.groupby('characters')['imdb_rating'].mean().reset_index()

    # Sort the DataFrame by the average of 'imdb_rating' in descending order
    characters_imdb_avg = characters_imdb_avg.sort_values(by='imdb_rating', ascending=False)
    # Reset the index and rename the index column
    characters_imdb_avg = characters_imdb_avg.reset_index(drop=True).rename_axis('Rank')
    # Add 1 to the index to start from 1
    characters_imdb_avg.index += 1

   

    # Display DataFrames side by side
    left_column, right_column = st.columns(2)

    with left_column:
        st.dataframe(characters_views)

    with right_column:
        st.dataframe(characters_imdb_avg)

    


###WRITERS
    
if category == "Writers" and feature == "Top 5 (More popular)":
    # Subtitle
    st.subheader("Top 5 Writers According to number of views")
    # Divide the screen into two columns
    left_column, right_column = st.columns(2)

    with left_column:
        top_5_writerss_more_views = df.groupby('written_by')['us_viewers_in_millions'].mean().nlargest(5)
        st.dataframe(top_5_writerss_more_views)

    with right_column:
        # Load and display image
        # Image path
        image_path = "images_simpsons/6.jpg"
        image = Image.open(image_path)
        #size picture
        new_width = image.width // 2
        new_height = image.height // 2
        resized_image = image.resize((new_width, new_height))
        # Show picture
        st.image(resized_image, caption=' ')
    
    # Plotting the line chart
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(top_5_writerss_more_views.index, top_5_writerss_more_views.values, marker='o')
    ax.set_xlabel('Written By')
    ax.set_ylabel('Mean Viewers (Millions)')
    ax.set_title('Top 5 Writers by Mean Viewers')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True)
    plt.tight_layout()

    # Setting y-axis limit to start from 0
    ax.set_ylim(bottom=0)

    plt.tight_layout()

    # Displaying the plot in Streamlit
    st.pyplot(fig)

    # Subtitle
    st.subheader("Top 5 Writers According to IMDb Rating")
    
    # Divide the screen into two columns
    left_column, right_column = st.columns(2)

    with left_column:
        top_5_writerss_more_views = df.groupby('written_by')['imdb_rating'].mean().nlargest(5)
        st.dataframe(top_5_writerss_more_views)

    with right_column:
        # Load and display image
        image_path = "images_simpsons/7.jpg"
        image = Image.open(image_path)
        #size picture
        new_width = image.width // 2
        new_height = image.height // 2
        resized_image = image.resize((new_width, new_height))
        # Show picture
        st.image(resized_image, caption=' ')
    
    # Plotting the line chart
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(top_5_writerss_more_views.index, top_5_writerss_more_views.values, marker='o')
    ax.set_xlabel('Written By')
    ax.set_ylabel('Mean Viewers (Millions)')
    ax.set_title('Top 5 Writers by Mean Viewers')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True)

    # Truncate the labels on the x-axis
    labels = [name[:15] + '...' if len(name) > 15 else name for name in top_5_writerss_more_views.index]
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)

    # Setting y-axis limit to start from 0
    ax.set_ylim(bottom=0)

    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(fig)

    

if category == "Writers" and feature == "Bottom 5 (Less popular)":
    # Subtitle
    st.subheader("Bottom 5 Writers According to number of views")
        # Divide the screen into two columns
    left_column, right_column = st.columns(2)

    with left_column:
        top_5_writerss_less_views = df.groupby('written_by')['us_viewers_in_millions'].mean().nsmallest(5)
        st.dataframe(top_5_writerss_less_views)

    with right_column:
        # Load and display image
        image_path = "images_simpsons/8.jpg"
        image = Image.open(image_path)
        #size picture
        new_width = image.width // 2
        new_height = image.height // 2
        resized_image = image.resize((new_width, new_height))
        # Show picture
        st.image(resized_image, caption=' ')
    

    

    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(top_5_writerss_less_views.index, top_5_writerss_less_views.values, marker='o')
    ax.set_xlabel('Written By')
    ax.set_ylabel('Mean Viewers (Millions)')
    ax.set_title('Bottom 5 Writers by Mean Viewers')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True)

    # Truncate the labels on the x-axis
    labels = [name[:15] + '...' if len(name) > 15 else name for name in top_5_writerss_less_views.index]
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)

    # Setting y-axis limit to start from 0
    ax.set_ylim(bottom=0)

    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(fig)

    # Subtitle
    st.subheader("Bottom 5 Writers According to IMDb Rating")
        # Divide the screen into two columns
    left_column, right_column = st.columns(2)

    with left_column:
        top_5_writerss_less_views_imdb = df.groupby('written_by')['imdb_rating'].mean().nsmallest(5)
        st.dataframe(top_5_writerss_less_views_imdb)

    with right_column:
        # Load and display image
        image_path = "images_simpsons/9.jpg"
        image = Image.open(image_path)
        #size picture
        new_width = image.width // 2
        new_height = image.height // 2
        resized_image = image.resize((new_width, new_height))
        # Show picture
        st.image(resized_image, caption=' ')

    

    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(top_5_writerss_less_views_imdb.index, top_5_writerss_less_views_imdb.values, marker='o')
    ax.set_xlabel('Written By')
    ax.set_ylabel('Mean IMDb Rating')
    ax.set_title('Bottom 5 Writers by Mean IMDb Rating')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True)

    # Truncate the labels on the x-axis
    labels = [name[:15] + '...' if len(name) > 15 else name for name in top_5_writerss_less_views_imdb.index]
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)

    # Setting y-axis limit to start from 0
    ax.set_ylim(bottom=0)

    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(fig)



if category == "Writers" and feature == "Overall Performance":
    
    
    #Don't show warning
    st.set_option('deprecation.showPyplotGlobalUse', False)

   # Calculate average viewership for each writer
    avg_viewers_by_writer = df.groupby('written_by')['us_viewers_in_millions'].mean()

    # Get top 5 and bottom 5 writers by average viewership
    top_5_writers = avg_viewers_by_writer.nlargest(5).index
    bottom_5_writers = avg_viewers_by_writer.nsmallest(5).index

    # Filter the original dataframe to include only top and bottom 5 writers
    filtered_df = df[df['written_by'].isin(top_5_writers) | df['written_by'].isin(bottom_5_writers)]

    # Create a pivot table with average viewership for each writer
    pivot_table = filtered_df.pivot_table(index='written_by', values='us_viewers_in_millions', aggfunc='mean')

    # Sort the pivot table by average viewership
    sorted_pivot_table = pivot_table.reindex(avg_viewers_by_writer.nlargest(5).index.tolist() + avg_viewers_by_writer.nsmallest(5).index.tolist())


    # Show the heatmap in the Streamlit app
    st.write("### Heatmap of Average Views by Top 5 & Bottom 5 Writers")
    plt.figure(figsize=(12, 8))
    sns.heatmap(sorted_pivot_table, annot=True, cmap='coolwarm')
    plt.ylabel('written_by')
    plt.xlabel('Average Views')
    plt.title('Average Views by Writer')
    plt.yticks(range(10), sorted_pivot_table.index)
    st.pyplot()

    
    # Don't show warning
    st.set_option('deprecation.showPyplotGlobalUse', False)

    # Calculate average IMDb rating for each writer
    avg_imdb_by_writer = df.groupby('written_by')['imdb_rating'].mean()

    # Get top 5 and bottom 5 writers by average IMDb rating
    top_5_writers = avg_imdb_by_writer.nlargest(5).index
    bottom_5_writers = avg_imdb_by_writer.nsmallest(5).index

    # Filter the original dataframe to include only top and bottom 5 writers
    filtered_df = df[df['written_by'].isin(top_5_writers) | df['written_by'].isin(bottom_5_writers)]

    # Create a pivot table with average IMDb rating for each writer
    pivot_table = filtered_df.pivot_table(index='written_by', values='imdb_rating', aggfunc='mean')

    # Sort the pivot table by average IMDb rating
    sorted_pivot_table = pivot_table.reindex(avg_imdb_by_writer.nlargest(5).index.tolist() + avg_imdb_by_writer.nsmallest(5).index.tolist())

    # Truncate written_by to maximum of 20 characters and add ellipsis if truncated
    sorted_pivot_table.index = sorted_pivot_table.index.map(lambda x: (x[:20] + '...') if len(x) > 20 else x)

    # Show the heatmap in the Streamlit app
    st.write("### Heatmap of Average IMDb Ratings by Top 5 & Bottom 5 Writers")
    plt.figure(figsize=(12, 8))
    sns.heatmap(sorted_pivot_table, annot=True, cmap='coolwarm')
    plt.ylabel('written_by')
    plt.xlabel('Average IMDb Ratings')
    plt.title('Average IMDb Ratings by Writer')
    plt.yticks(range(10), sorted_pivot_table.index)
    st.pyplot()

if category == "Directors" and feature == "Top 5 (More popular)":

    # Subtitle
    st.subheader("Top 5 Directors According to number of views")
        # Divide the screen into two columns
    left_column, right_column = st.columns(2)

    with left_column:
        top_5_directed_more_views = df.groupby('directed_by')['us_viewers_in_millions'].mean().nlargest(5)
        st.dataframe(top_5_directed_more_views)
    with right_column:
        # Load and display image
        image_path = "images_simpsons/10.jpg"
        image = Image.open(image_path)
        #size picture
        new_width = image.width // 2
        new_height = image.height // 2
        resized_image = image.resize((new_width, new_height))
        # Show picture
        st.image(resized_image, caption=' ')
    

    # Plotting the line chart
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(top_5_directed_more_views.index, top_5_directed_more_views.values, marker='o')
    ax.set_xlabel('Directed By')
    ax.set_ylabel('Mean Viewers (Millions)')
    ax.set_title('Top 5 Directors by Mean Viewers')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True)
    plt.tight_layout()

    # Setting y-axis limit to start from 0
    ax.set_ylim(bottom=0)

    plt.tight_layout()

    # Displaying the plot in Streamlit
    st.pyplot(fig)

    # Subtitle
    st.subheader("Top 5 Directors According to IMDb Rating")
        # Divide the screen into two columns
    left_column, right_column = st.columns(2)

    with left_column:
        top_5_directed_more_views_imdb = df.groupby('directed_by')['imdb_rating'].mean().nlargest(5)
        st.dataframe(top_5_directed_more_views_imdb)
    with right_column:
        # Load and display image
        image_path = "images_simpsons/11.jpg"
        image = Image.open(image_path)
        #size picture
        new_width = image.width // 2
        new_height = image.height // 2
        resized_image = image.resize((new_width, new_height))
        # Show picture
        st.image(resized_image, caption=' ')
    

    # Plotting the line chart
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(top_5_directed_more_views_imdb.index, top_5_directed_more_views_imdb.values, marker='o')
    ax.set_xlabel('Directed By')
    ax.set_ylabel('Mean IMDb Rating')
    ax.set_title('Top 5 Directors by Mean IMDb Rating')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True)

    # Truncate the labels on the x-axis
    labels = [name[:15] + '...' if len(name) > 15 else name for name in top_5_directed_more_views_imdb.index]
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)

    # Setting y-axis limit to start from 0
    ax.set_ylim(bottom=0)

    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(fig)

if category == "Directors" and feature == "Bottom 5 (Less popular)":
    
    # Subtitle
    st.subheader("Bottom 5 Directors According to number of views")
        # Divide the screen into two columns
    left_column, right_column = st.columns(2)

    with left_column:
        top_5_directed_less_views = df.groupby('directed_by')['us_viewers_in_millions'].mean().nsmallest(5)
        st.dataframe(top_5_directed_less_views)
    with right_column:
        # Load and display image
        image_path = "images_simpsons/12.jpg"
        image = Image.open(image_path)
        #size picture
        new_width = image.width // 2
        new_height = image.height // 2
        resized_image = image.resize((new_width, new_height))
        # Show picture
        st.image(resized_image, caption=' ')

    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(top_5_directed_less_views.index, top_5_directed_less_views.values, marker='o')
    ax.set_xlabel('Directed By')
    ax.set_ylabel('Mean Viewers (Millions)')
    ax.set_title('Bottom 5 Directors by Mean Viewers')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True)

    # Truncate the labels on the x-axis
    labels = [name[:15] + '...' if len(name) > 15 else name for name in top_5_directed_less_views.index]
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)

    # Setting y-axis limit to start from 0
    ax.set_ylim(bottom=0)

    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(fig)

    # Subtitle
    st.subheader("Bottom 5 Directors According to IMDb Rating")
        # Divide the screen into two columns
    left_column, right_column = st.columns(2)

    with left_column:
        top_5_directed_less_views_imdb = df.groupby('directed_by')['imdb_rating'].mean().nsmallest(5)
        st.dataframe(top_5_directed_less_views_imdb)
    with right_column:
        # Load and display image
        image_path = "images_simpsons/13.jpg"
        image = Image.open(image_path)
        #size picture
        new_width = image.width // 2
        new_height = image.height // 2
        resized_image = image.resize((new_width, new_height))
        # Show picture
        st.image(resized_image, caption=' ')
    

    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(top_5_directed_less_views_imdb.index, top_5_directed_less_views_imdb.values, marker='o')
    ax.set_xlabel('Directed By')
    ax.set_ylabel('Mean IMDb Rating')
    ax.set_title('Bottom 5 Directors by Mean IMDb Rating')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True)

    # Truncate the labels on the x-axis
    labels = [name[:15] + '...' if len(name) > 15 else name for name in top_5_directed_less_views_imdb.index]
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)

    # Setting y-axis limit to start from 0
    ax.set_ylim(bottom=0)

    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(fig)


if category == "Directors" and feature == "Overall Performance":
    # Don't show warning
    st.set_option('deprecation.showPyplotGlobalUse', False)

    # Calculate average viewership for each director
    avg_viewers_by_director = df.groupby('directed_by')['us_viewers_in_millions'].mean()

    # Get top 5 and bottom 5 directors by average viewership
    top_5_directors = avg_viewers_by_director.nlargest(5).index
    bottom_5_directors = avg_viewers_by_director.nsmallest(5).index

    # Filter the original dataframe to include only top and bottom 5 directors
    filtered_df = df[df['directed_by'].isin(top_5_directors) | df['directed_by'].isin(bottom_5_directors)]

    # Create a pivot table with average viewership for each director
    pivot_table = filtered_df.pivot_table(index='directed_by', values='us_viewers_in_millions', aggfunc='mean')

    # Sort the pivot table by average viewership
    sorted_pivot_table = pivot_table.reindex(avg_viewers_by_director.nlargest(5).index.tolist() + avg_viewers_by_director.nsmallest(5).index.tolist())

    # Truncate directed_by to maximum of 20 characters and add ellipsis if truncated
    sorted_pivot_table.index = sorted_pivot_table.index.map(lambda x: (x[:20] + '...') if len(x) > 20 else x)

    # Show the heatmap in the Streamlit app
    st.write("### Heatmap of Average Views by Top 5 & Bottom 5 Directors")
    plt.figure(figsize=(12, 8))
    sns.heatmap(sorted_pivot_table, annot=True, cmap='coolwarm')
    plt.ylabel('directed_by')
    plt.xlabel('Average Views')
    plt.title('Average Views by Director')
    plt.yticks(range(10), sorted_pivot_table.index)
    st.pyplot()
    
    
    
    # Don't show warning
    st.set_option('deprecation.showPyplotGlobalUse', False)

    # Calculate average IMDb rating for each director
    avg_imdb_by_director = df.groupby('directed_by')['imdb_rating'].mean()

    # Get top 5 and bottom 5 directors by average IMDb rating
    top_5_directors = avg_imdb_by_director.nlargest(5).index
    bottom_5_directors = avg_imdb_by_director.nsmallest(5).index

    # Filter the original dataframe to include only top and bottom 5 directors
    filtered_df = df[df['directed_by'].isin(top_5_directors) | df['directed_by'].isin(bottom_5_directors)]

    # Create a pivot table with average IMDb rating for each director
    pivot_table = filtered_df.pivot_table(index='directed_by', values='imdb_rating', aggfunc='mean')

    # Sort the pivot table by average IMDb rating
    sorted_pivot_table = pivot_table.reindex(avg_imdb_by_director.nlargest(5).index.tolist() + avg_imdb_by_director.nsmallest(5).index.tolist())

    # Truncate directed_by to maximum of 20 characters and add ellipsis if truncated
    sorted_pivot_table.index = sorted_pivot_table.index.map(lambda x: (x[:20] + '...') if len(x) > 20 else x)

    # Show the heatmap in the Streamlit app
    st.write("### Heatmap of Average IMDb Ratings by Top 5 & Bottom 5 Directors")
    plt.figure(figsize=(12, 8))
    sns.heatmap(sorted_pivot_table, annot=True, cmap='coolwarm')
    plt.ylabel('directed_by')
    plt.xlabel('Average IMDb Ratings')
    plt.title('Average IMDb Ratings by Director')
    plt.yticks(range(10), sorted_pivot_table.index)
    st.pyplot()

#### Episodes
if category == "Episodes" and feature == "Top 5 (More popular)":
    
    #IMDb rating
    # Get the top 5 titles with highest IMDb rating
    top_5_titles = df.nlargest(5, 'imdb_rating')

    # Create a new DataFrame with the selected columns
    top_5_episodes_views = top_5_titles[['season', 'number_in_season', 'imdb_rating', 'us_viewers_in_millions', 'title', 'description', 'written_by', 'directed_by']].copy()

    # Display the new DataFrame in the dashboard
    st.write("#### Top 5 episodes with Highest IMDb Rating")
    st.write(top_5_episodes_views)
    # Load and display image
    image_path = "images_simpsons/14.jpg"
    image = Image.open(image_path)
    st.image(image, caption=' ', use_column_width=True)

    #Number of Views
    # Get the top 5 titles with highest number of views in US
    top_5_titles = df.nlargest(5, 'us_viewers_in_millions')

    # Create a new DataFrame with the selected columns
    top_5_episodes_views = top_5_titles[['season', 'number_in_season', 'us_viewers_in_millions', 'imdb_rating', 'title', 'description', 'written_by', 'directed_by']].copy()

    # Display the new DataFrame in the dashboard
    st.write("#### Top 5 episodes with Highest Number of views")
    st.write(top_5_episodes_views)

    # Load and display image
    image_path = "images_simpsons/15.jpg"
    image = Image.open(image_path)
    st.image(image, caption=' ', use_column_width=True)

if category == "Episodes" and feature == "Bottom 5 (Less popular)":
    
    #IMDb rating
    # Get the top 5 titles with highest IMDb rating
    top_5_titles = df.nsmallest(5, 'imdb_rating')

    # Create a new DataFrame with the selected columns
    top_5_episodes_views = top_5_titles[['season', 'number_in_season', 'imdb_rating', 'us_viewers_in_millions', 'title', 'description', 'written_by', 'directed_by']].copy()

    # Display the new DataFrame in the dashboard
    st.write("#### Top 5 episodes with Lowest IMDb Rating")
    st.write(top_5_episodes_views)

    # Load and display image
    image_path = "images_simpsons/16.jpg"
    image = Image.open(image_path)
    st.image(image, caption=' ', use_column_width=True)
    
    #Number of Views
    # Get the top 5 titles with highest number of views in US
    top_5_titles = df.nsmallest(5, 'us_viewers_in_millions')

    # Create a new DataFrame with the selected columns
    top_5_episodes_views = top_5_titles[['season', 'number_in_season', 'us_viewers_in_millions', 'imdb_rating', 'title', 'description', 'written_by', 'directed_by']].copy()

    # Display the new DataFrame in the dashboard
    st.write("#### Top 5 episodes with Lowest Number of views")
    st.write(top_5_episodes_views)

    # Load and display image
    image_path = "images_simpsons/17.jpg"
    image = Image.open(image_path)
    st.image(image, caption=' ', use_column_width=True)

if category == "Episodes" and feature == "Overall Performance":
    #Number of episode with more views per season
    # Find the row with the maximum 'us_viewers_in_millions' for each 'season'
    max_viewers_rows = df.loc[df.groupby('season')['us_viewers_in_millions'].idxmax()]

    # Create the line plot
    fig = px.line(max_viewers_rows, x='season', y='us_viewers_in_millions', text='number_in_season', labels={'us_viewers_in_millions': 'US Viewers (Millions)'})
    fig.update_traces(textposition="bottom center", hoverinfo='skip', name='Number in Season')
    fig.update_layout(title='Number of episode with more views per season', xaxis_title='Season', yaxis_title='US Viewers (Millions)')

    # Display the plot in Streamlit
    st.plotly_chart(fig)

    #Number of episode with highest IMDb rating per season
    # Find the row with the maximum 'imdb_rating' for each 'season'
    max_rating_rows = df.loc[df.groupby('season')['imdb_rating'].idxmax()]

    # Create the line plot
    fig = px.line(max_rating_rows, x='season', y='imdb_rating', text='number_in_season', labels={'imdb_rating': 'IMDb Rating'})
    fig.update_traces(textposition="bottom center", hoverinfo='skip', name='Number in Season')
    fig.update_layout(title='Number of episode with highest IMDb rating per season', xaxis_title='Season', yaxis_title='IMDb Rating')

    # Display the plot in Streamlit
    st.plotly_chart(fig)

if category == "Correlations" and feature == "Viewers & Ratings":
    # Create a scatter plot for the relationship between 'us_viewers_in_millions' and 'imdb_rating'
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x='us_viewers_in_millions', y='imdb_rating', ax=ax)
    ax.set_xlabel('US Viewers (Millions)')
    ax.set_ylabel('IMDb Rating')
    ax.set_title('Relationship between Viewers and IMDb Rating')
    st.pyplot(fig)


if category == "Correlations" and feature == "Viewers & Season":
    # Create a scatter plot for the relationship between 'us_viewers_in_millions' and 'season'
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x='season', y='us_viewers_in_millions', ax=ax)
    ax.set_xlabel('Season')
    ax.set_ylabel('US Viewers (Millions)')
    ax.set_title('Relationship between Season and Viewers')
    st.pyplot(fig)

if category == "Correlations" and feature == "Season & Ratings":
    # Create a scatter plot for the relationship between 'imdb_rating' and 'season'
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x='season', y='imdb_rating', ax=ax)
    ax.set_xlabel('Season')
    ax.set_ylabel('IMDb Rating')
    ax.set_title('Relationship between Season and IMDb Rating')
    st.pyplot(fig)
