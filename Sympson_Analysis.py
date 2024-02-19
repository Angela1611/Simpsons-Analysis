import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re
from matplotlib.colors import ListedColormap
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go





st.set_page_config(page_title="The Simpsons - Analysis",
                   page_icon="bar_chart:",
                   layout="wide")
                

df= pd.read_csv("simpsons_episodes.csv")
df['original_air_date'] = pd.to_datetime(df['original_air_date'])
df['year'] = df['original_air_date'].dt.year

#______________ Side bar _________
st.sidebar.header("Please filter here:")
category = st.sidebar.selectbox(
    "Category",
    [" ", "Season", "Characters", "Writers", "Directors", "Episodes"]
)

feature = st.sidebar.selectbox(
    "Feature to analyze",
    [" ", "Top 5 (More popular)", "Bottom 5 (Less popular)", "Overall Performance"]
)


# Filter info by user selection
if category == "Season" and feature == "Top 5 (More popular)":
    top_5_us_viewers = df.groupby("season")["us_viewers_in_millions"].mean().nlargest(5).reset_index()
    fig3 = px.bar(top_5_us_viewers, x="season", y="us_viewers_in_millions", title="Top 5 Seasons by US Viewers (Millions)")
    fig3.update_layout(width=400, height=400)  # graphic size
    
    st.plotly_chart(fig3, use_container_width=True)
    
    st.write("\n")  # space between graphics
    
    top_5_imdb_ratings = df.groupby("season")["imdb_rating"].mean().nlargest(5).reset_index()
    fig1 = px.bar(top_5_imdb_ratings, x="season", y="imdb_rating", title="Top 5 Seasons by Imdb Rating")
    
    top_5_tmdb_ratings = df.groupby("season")["tmdb_rating"].mean().nlargest(5).reset_index()
    fig2 = px.bar(top_5_tmdb_ratings, x="season", y="tmdb_rating", title="Top 5 Seasons by Tmdb Rating")
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.plotly_chart(fig3, use_container_width=True)
        

if category == "Season" and feature == "Bottom 5 (Less popular)":
    top_5_us_viewers = df.groupby("season")["us_viewers_in_millions"].mean().reset_index()
    top_5_us_viewers = top_5_us_viewers.sort_values(by="us_viewers_in_millions", ascending=True).head(5)
    fig3 = px.bar(top_5_us_viewers, x="season", y="us_viewers_in_millions", title="Bottom 5 Seasons by US Viewers (Millions)")
    fig3.update_layout(width=400, height=400, bargap=0.1)  
    
    st.plotly_chart(fig3, use_container_width=True)
    
    st.write("\n") 
    
    top_5_imdb_ratings = df.groupby("season")["imdb_rating"].mean().nsmallest(5).reset_index()
    top_5_imdb_ratings = top_5_imdb_ratings.dropna()
    fig1 = px.bar(top_5_imdb_ratings, x="season", y="imdb_rating", title="Bottom 5 Seasons by Imdb Rating")
    
    top_5_tmdb_ratings = df.groupby("season")["tmdb_rating"].mean().nsmallest(5).reset_index()
    top_5_tmdb_ratings = top_5_tmdb_ratings.dropna()
    fig2 = px.bar(top_5_tmdb_ratings, x="season", y="tmdb_rating", title="Bottom 5 Seasons by Tmdb Rating")
    fig2.update_layout(bargap=0.1)  
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.plotly_chart(fig2, use_container_width=True)

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

    # Add line trace for average TMDb rating
    fig.add_trace(go.Scatter(x=year_avg_ratings['year'], y=year_avg_ratings['tmdb_rating'],
                             mode='lines+markers',
                             name='Average TMDb Rating',
                             line=dict(color='green')), secondary_y=True)

    # Update layout
    fig.update_layout(title='Average US Viewers, IMDb, and TMDb Ratings Over Time',
                      xaxis_title='Year',
                      yaxis_title='Average US Viewers (Millions)',
                      yaxis2_title='Average Rating',
                      legend=dict(x=0, y=1.4),
                      title_x=0.5)

    # Show the figure
    st.plotly_chart(fig, use_container_width=True)

if category == "Characters" and feature == "Top 5 (More popular)":
    
    # Subtitle
    st.write("According to number of views")
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

    #IMDb Rating
    # Subtitle
    st.write("According to IMDb Rating")
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

#TMDb Rating
    # Subtitle
    st.write("According to TMDb Rating")
    # Create a new DataFrame with the average of 'tmdb_rating' per character
    characters_tmdb_avg = df2.groupby('characters')['tmdb_rating'].mean().reset_index()

    # Sort the DataFrame by the average of 'imdb_rating' in descending order
    characters_tmdb_avg = characters_tmdb_avg.sort_values(by='tmdb_rating', ascending=False)

    # Select the top 5 characters and reset the index to start from 1
    characters_tmdb_avg_top_5 = characters_tmdb_avg.head(5).reset_index(drop=True)

    # Add 1 to the index to start from 1
    characters_tmdb_avg_top_5.index += 1

    # Display the DataFrame with the average of 'imdb_rating' per character
    st.dataframe(characters_tmdb_avg_top_5)

if category == "Characters" and feature == "Bottom 5 (Less popular)":
    
    # Subtitle
    st.write("According to number of views")

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

    #IMDb Rating
    
    # Subtitle
    st.write("According to IMDb Rating")

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

    # Display the DataFrame with the average of 'imdb_rating' per character
    st.dataframe(characters_imdb_avg_bottom_5)

#TMDb Rating
    
    # Subtitle
    st.write("According to TMDb Rating")

    # Create a new DataFrame with the average of 'tmdb_rating' per character
    characters_tmdb_avg = df2.groupby('characters')['tmdb_rating'].mean().reset_index()

    # Sort the DataFrame by the average of 'imdb_rating' in descending order
    characters_tmdb_avg = characters_tmdb_avg.sort_values(by='tmdb_rating', ascending=False)

    # Select the top 5 characters and reset the index to start from 1
    characters_tmdb_avg_bottom_5 = characters_tmdb_avg.tail(5).reset_index(drop=True)

    # Add 1 to the index to start from 1
    characters_tmdb_avg_bottom_5.index += 1

    # Display the DataFrame with the average of 'imdb_rating' per character
    st.dataframe(characters_tmdb_avg_bottom_5)

if category == "Characters" and feature == "Overall Performance":
    # Subtitle
    st.write("According to number of views")
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
    # Reset the index and rename the index column
    characters_views = characters_views.reset_index(drop=True).rename_axis('Rank')
    # Add 1 to the index to start from 1
    characters_views.index += 1

    st.dataframe(characters_views)

    # Subtitle
    st.write("According to IMDb Rating")

    # Create a new DataFrame with the average of 'tmdb_rating' per character
    characters_imdb_avg = df2.groupby('characters')['imdb_rating'].mean().reset_index()

    # Sort the DataFrame by the average of 'imdb_rating' in descending order
    characters_imdb_avg = characters_imdb_avg.sort_values(by='imdb_rating', ascending=False)
    # Reset the index and rename the index column
    characters_imdb_avg = characters_imdb_avg.reset_index(drop=True).rename_axis('Rank')
    # Add 1 to the index to start from 1
    characters_imdb_avg.index += 1

    st.dataframe(characters_imdb_avg)

    
    # Subtitle
    st.write("According to TMDb Rating")

    # Create a new DataFrame with the average of 'tmdb_rating' per character
    characters_tmdb_avg = df2.groupby('characters')['tmdb_rating'].mean().reset_index()

    # Sort the DataFrame by the average of 'imdb_rating' in descending order
    characters_tmdb_avg = characters_tmdb_avg.sort_values(by='tmdb_rating', ascending=False)
    # Reset the index and rename the index column
    characters_tmdb_avg = characters_tmdb_avg.reset_index(drop=True).rename_axis('Rank')
    # Add 1 to the index to start from 1
    characters_tmdb_avg.index += 1

    st.dataframe(characters_tmdb_avg)


###WRITERS
    
if category == "Writers" and feature == "Top 5 (More popular)":

    
    top_5_writerss_more_views = df.groupby('written_by')['us_viewers_in_millions'].mean().nlargest(5)
    st.dataframe(top_5_writerss_more_views)

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

    top_5_writerss_more_views = df.groupby('written_by')['imdb_rating'].mean().nlargest(5)
    st.dataframe(top_5_writerss_more_views)

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

    top_5_writerss_more_views = df.groupby('written_by')['tmdb_rating'].mean().nlargest(5)
    st.dataframe(top_5_writerss_more_views)
    # Plotting the line chart
    # Plotting the line chart
    # Plotting the line chart with X and Y axes swapped
    fig, ax = plt.subplots(figsize=(9, 4.5))  # Adjust the size as needed
    ax.plot(top_5_writerss_more_views.values, top_5_writerss_more_views.index, marker='o')  # Swap X and Y
    ax.set_xlabel('Mean Viewers (Millions)')  # Swap X and Y labels
    ax.set_ylabel('Written By')
    ax.set_title('Top 5 Writers by Mean Viewers')
    ax.tick_params(axis='y', rotation=0)  # Rotate Y axis labels
    ax.grid(True)

# Setting x-axis limit to start from 0
    ax.set_xlim(left=0)

    plt.tight_layout()

# Displaying the plot in Streamlit
    st.pyplot(fig)
    

if category == "Writers" and feature == "Bottom 5 (Less popular)":

    
    top_5_writerss_less_views = df.groupby('written_by')['us_viewers_in_millions'].mean().nsmallest(5)
    st.dataframe(top_5_writerss_less_views)

    top_5_writerss_less_views = df.groupby('written_by')['imdb_rating'].mean().nsmallest(5)
    st.dataframe(top_5_writerss_less_views)

    top_5_writerss_less_views = df.groupby('written_by')['tmdb_rating'].mean().nsmallest(5)
    st.dataframe(top_5_writerss_less_views)