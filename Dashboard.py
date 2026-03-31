import pandas as pd
import plotly.express as px
import streamlit as st

# Set Dashboard Title
st.set_page_config(page_title='Life Expectancy Dashboard',layout='wide')
st.title('Life Expectancy Dashboard',text_alignment='center')

# Load cleaned Data
life = pd.read_csv('life_expectancy_cleaned1.csv')

# Set Sidebar
# Set Page Navigator
with st.sidebar:
    st.header('Pages',text_alignment='center')
    page = st.radio('Select a Page',['Overview','Correlation Analysis','Time Series Analysis','Regional Analysis'])

# Set Filter 
    st.header('Filters',text_alignment='center')
    st.subheader('Year')
    year_range = st.slider(label='Select Year',min_value=life['year'].min(),max_value=life['year'].max(),value=(life['year'].min(),life['year'].max()))
    st.subheader('Country Development Status')
    status = st.radio('Select Development Status',['All']+list(life['status'].unique()))
    st.subheader('Continent')
    if status=='All':
        all_continent=['All']+list(life['continent'].unique())
    else:
        all_continent=['All']+list(life[life['status']==status]['continent'].unique())
    continent = st.selectbox('Select Continent',all_continent)
    st.subheader('Country')
    if status=='All':
        if continent=='All':
            all_country=['All']+list(life['country'].unique())
        else:
            all_country=['All']+list(life[life['continent']==continent]['country'].unique())
    else:
        if continent=='All':
            all_country=['All']+list(life[life['status']==status]['country'].unique())
        else:
            all_country=['All']+ list(life[(life['status']==status)&(life['continent']==continent)]['country'].unique())
    country = st.selectbox('Select Country',all_country)


if page=='Overview':
    tab1,tab2=st.tabs(['Plots','Summary'])
    with tab1:
        col1,col2,col3,col4,col5=st.columns(5)
        with col1:
            st.metric('Average Life Expectancy',life['life_expectancy'].mean().round(2))
        with col2:
            max_avg_continent=life.groupby('continent')['life_expectancy'].mean().idxmax()
            st.metric('Highest Continent',max_avg_continent)
        with col3:    
            max_avg_country =life.groupby('country')['life_expectancy'].mean().idxmax()
            st.metric('Highest Country', max_avg_country)
        with col4:
            lowest_avg_continent=life.groupby('continent')['life_expectancy'].mean().idxmin()
            st.metric('Lowest Continent',lowest_avg_continent)
        with col5:
            lowest_avg_country = life.groupby('country')['life_expectancy'].mean().idxmin() 
            st.metric('Lowest Country',lowest_avg_country)
        
        sec_col1,sec_col2=st.columns(2)
        with sec_col1:
            life_ex_trend = life.groupby(['year'])['life_expectancy'].mean().sort_index().reset_index()
            st.plotly_chart(px.line(life_ex_trend,x='year',y='life_expectancy',labels={'year':'Year','life_expectancy':'Life Expectancy'},
                    title='Average Life Expectancy Trend by Year'),use_container_width=True)

            # GDP contribution by country status from total GDP
            gdp_per_status = life.groupby('status')['gdp'].sum().sort_values(ascending=False).reset_index().round(2)
            gdp_per_status_pie = px.pie(gdp_per_status,names='status',values='gdp',hole=0.5,title='Contribution to Total GDP: Developed vs. Developing Nations')
            gdp_per_status_pie.update_traces(textinfo='percent+label',showlegend=False)
            st.plotly_chart(gdp_per_status_pie,use_container_width=True)
        with sec_col2:
            # Display percentage of developed vs developing countries
            status_percent =px.pie(life.groupby('status')['country'].nunique().reset_index(), names='status', values='country',title='Distribution of Countries by Economic Development Status')
            status_percent.update_traces(textinfo='percent+label', textposition='inside', showlegend=False)
            st.plotly_chart(status_percent,use_container_width=True)

            # Visualizing Average GDP by Continent
            continent_gdp = life.groupby('continent')['gdp'].mean().sort_values(ascending=False).reset_index()
            st.plotly_chart(px.histogram(continent_gdp,x='continent',y='gdp',
                        title='Average GDP by Continent').update_layout(yaxis_title='GDP',xaxis_title='Continent'),use_container_width=True)

        thrd_col1,=st.columns(1)
        with thrd_col1:
            # Visualizing country count per continent
            country_count_per_cont = life.groupby(['continent','status'])['country'].nunique().reset_index().sort_values(by='country',ascending=False)
            st.plotly_chart(px.histogram(country_count_per_cont,x='continent',y='country',color='status', text_auto=True,barmode='group',
                        title='Country Count Per Continent').update_layout(xaxis_title='Continent',yaxis_title='Country'),use_container_width=True)

elif page =='Correlation Analysis':
    p2_tab1,p2_tab2,p2_tab3 = st.tabs(['Overall Correlations','Socioeconomic Factors','Healthcare Factors'])
    
    with p2_tab1:
        p2t1_col1,=st.columns(1)
        with p2t1_col1:
            # Studying correlation between different factors in our dataset (Moderate to Strong correlations)
            num_clean= life.select_dtypes(include='number')
            corr_matrix = num_clean.corr()
            strong_corr = corr_matrix[((corr_matrix>0.5) & (corr_matrix<1)) | ((corr_matrix<-0.5) & (corr_matrix>-1))]
            st.plotly_chart(px.imshow(strong_corr.round(2), text_auto=True,width=1000, height=800,title='Moderate to Strong Correlated Factors'),use_container_width=True)

            # Studying factors affecting our target column (Life Expectancy)
            life_exp_corr = num_clean['life_expectancy']
            st.plotly_chart(px.imshow(num_clean.corrwith(life_exp_corr).sort_values(ascending=False).to_frame().round(2) , text_auto=True, width=1000, height=800, title='Correlation with Life Expectancy'),use_container_width=True)

        with p2_tab2:
            p2t2_col1,p2t2_col2=st.columns(2)
            se_filtered_life = life.copy()
            with p2t2_col1:

                if status != 'All':
                    se_filtered_life = se_filtered_life[se_filtered_life['status'] == status]

                if continent != 'All':
                    se_filtered_life = se_filtered_life[se_filtered_life['continent'] == continent]

                if country != 'All':
                    se_filtered_life = se_filtered_life[se_filtered_life['country'] == country]

                # Visualizing correlation between GDP and Life Expectancy segmented by country status
                st.plotly_chart(px.scatter(se_filtered_life,x='life_expectancy',y='gdp',trendline='ols',
                    labels={'gdp':'GDP','life_expectancy':'Life Expectancy','status':'Status'},
                    title='Correlation between GDP and Life Expectancy'),use_container_width=True)   
                
                # Visualizing correlation between Life Expectancy and Schooling segmented by country status
                st.plotly_chart(px.scatter(se_filtered_life,x='life_expectancy',y='schooling',trendline='ols',
                                labels={'life_expectancy':'Life Expectancy','schooling':'Schooling'},
                                title='Correlation between Life Expectancy and Schooling'),use_container_width=True)
            with p2t2_col2:   

                # Visualizing correlation between GDP and Percentage Expenditure
                st.plotly_chart(px.scatter(se_filtered_life,x='gdp',y='percentage_expenditure',trendline='ols',
                        labels={'gdp':'GDP','percentage_expenditure':'Percentage Expenditure'},
                        title='Correlation between GDP and Percentage Expenditure'),use_container_width=True)
                
                # Visualizing correlation between Life Expectancy and Income Composition of Resources segmented by country status
                st.plotly_chart(px.scatter(se_filtered_life,x='life_expectancy',y='income_composition_of_resources',trendline='ols',
                             labels={'life_expectancy':'Life Expectancy','income_composition_of_resources':'Income Composition of Resources'},
                            title='Correlation between Life Expectancy and HDI'),use_container_width=True)



            
            
            

               
            


           



