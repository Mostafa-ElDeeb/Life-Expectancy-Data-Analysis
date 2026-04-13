# Import necessary libraries
import pandas as pd
import plotly.express as px
import streamlit as st

# Set Dashboard page and title
st.set_page_config(page_title='Life Expectancy Dashboard',layout='wide')
st.title('Life Expectancy Dashboard',text_alignment='center')

# Load cleaned Data
life = pd.read_csv('life_expectancy_cleaned1.csv')

# Set sidebar
# Set page navigator
with st.sidebar:
    st.header('Pages',text_alignment='center')
    page = st.radio('Select a Page',['Overview','Correlation Analysis','Time Series Analysis','Regional Analysis','Recommendations'])

# Set filters
# Set filter header and subheader
    st.header('Filters',text_alignment='center')
# Create year filter
    st.subheader('Year')
    year_range = st.slider(label='Select Year',min_value=life['year'].min(),max_value=life['year'].max(),value=(life['year'].min(),life['year'].max()))
# Create country development status filter  
    st.subheader('Country Development Status')
    status = st.radio('Select Development Status',['All']+list(life['status'].unique()))
# Create continents filter    
    st.subheader('Continent')
# Define logic for sequential filtering to display only continents within a specific development status
# All option is considered to allow flexible filtering to be able to select all rows in the dataset when needed
    if status=='All':
        all_continent=['All']+list(life['continent'].unique())
    else:
        all_continent=['All']+list(life[life['status']==status]['continent'].unique())
    continent = st.selectbox('Select Continent',all_continent)
    st.subheader('Country')
# Define logic for sequential filtering to display only countries within a specific development status and/or continent
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

# Create filtered DataFrame by regional categories with resepect to filtering logic we defined earlier
region_filtered_life = life.copy()
if status != 'All':
    region_filtered_life = region_filtered_life[region_filtered_life['status'] == status]

if continent != 'All':
    region_filtered_life = region_filtered_life[region_filtered_life['continent'] == continent]

if country != 'All':
    region_filtered_life = region_filtered_life[region_filtered_life['country'] == country]

# Create filtered DataFrame by year
filtered_year = life['year'].between(year_range[0],year_range[1])
year_filtered_life = life[filtered_year]

# Create filtered DataFrame by year and regional categories
region_year_filtered_life = region_filtered_life[region_filtered_life['year'].between(year_range[0],year_range[1])]

# Prepare first page in the dashboard
if page=='Overview':
    st.subheader('Overview')
# Create tabs to distribute our insight in
    tab1,tab2=st.tabs(['Introduction','Plots'])
    with tab1:
        st.subheader('Life Expectancy')
        st.markdown("""Life Expectancy at Birth is the average number of years a person is expected to live.
                    It is one of the most important indicators of population overall health and well-being, reflecting
                    the quality of healthcare, living conditions, education and economy.
                    The target of our analysis is to find key factors that affect life expectancy of an individual 
                    across different regions around the world.""")
        st.divider()
        st.subheader('Schooling')
        st.markdown("""Average number of years of education received by individual.""")
        st.subheader('Income Composition of Resources')
        st.markdown("""Human Development Index (HDI).
                    It is a fractional index (scaled from 0 to 1) that measures how effectively a country 
                    transforms its national income into human development resources.""")
        st.subheader('GDP')
        st.markdown("""Gross Domestic Product. 
                    represents the total monetary of all the finished goods and services produced 
                    within a country's borders in a specific time period.""")
        st.subheader('Adult Mortality')
        st.markdown("""Probability of dying between 15 and 60 years of age per 1000 population.""")
        
    with tab2:
# Design page layout
# Prepare key metrics
        col1,col2,col3,col4,col5=st.columns(5)
        with col1:
            st.metric('Total Countries',life['country'].nunique())
        with col2:
            st.metric('Average Life Expectancy',life['life_expectancy'].mean().round(2))
        with col3:
            st.metric('Average HDI',life['income_composition_of_resources'].mean().round(2))
        with col4:    
          st.metric('Average Schooling',life['schooling'].mean().round(2))
        with col5:
            st.metric('Average Adult Mortality',life['adult_mortality'].mean().round(2))
        
        second_col1,second_col2=st.columns(2)
# Visualize life expectancy trend
        with second_col1:
            with st.container(border=True):
                life_ex_trend = life.groupby(['year'])['life_expectancy'].mean().sort_index().reset_index()
                st.plotly_chart(px.line(life_ex_trend,x='year',y='life_expectancy',labels={'year':'Year','life_expectancy':'Life Expectancy'},
                        title='Average Life Expectancy Trend by Year'),use_container_width=True)

# GDP contribution by country status from total GDP
            with st.container(border=True):
                gdp_per_status = life.groupby('status')['gdp'].sum().sort_values(ascending=False).reset_index().round(2)
                gdp_per_status_pie = px.pie(gdp_per_status,names='status',values='gdp',hole=0.5,height=531,title='Contribution to Total GDP:<br>Developed vs. Developing Nations')
                gdp_per_status_pie.update_traces(textinfo='percent+label',showlegend=False)
                st.plotly_chart(gdp_per_status_pie,use_container_width=True)

                st.divider()
                st.markdown('Developed countries account for 52.6% of the total GDP in the dataset, while developing nations represent the remaining 47.4%.')
        with second_col2:
# Display percentage of developed vs developing countries
            with st.container(border=True):
                status_percent =px.pie(life.groupby('status')['country'].nunique().reset_index(), names='status', values='country',title='Distribution of Countries by Economic<br>Development Status')
                status_percent.update_traces(textinfo='percent+label', textposition='inside', showlegend=False)
                st.plotly_chart(status_percent,use_container_width=True)
                
                st.divider()
                st.markdown('82.2% of countries are developing while 17.8% are developed',text_alignment='center')

# Visualizing Average GDP by Continent
            with st.container(border=True):
                continent_gdp = life.groupby('continent')['gdp'].mean().sort_values(ascending=False).reset_index()
                st.plotly_chart(px.histogram(continent_gdp,x='continent',y='gdp',
                            title='Average GDP by Continent').update_layout(yaxis_title='GDP',xaxis_title='Continent'),use_container_width=True)
                
                st.divider()
                st.markdown('Highest average GDP appears in Europe while lowest appears in Africa.')

        thrd_col1,=st.columns(1)
        with thrd_col1:
# Visualizing country count per continent
            with st.container(border=True):
                country_count_per_cont = life.groupby(['continent','status'])['country'].nunique().reset_index().sort_values(by='country',ascending=False)
                st.plotly_chart(px.histogram(country_count_per_cont,x='continent',y='country',color='status', text_auto=True,barmode='group',
                                title='Country Count Per Continent').update_layout(xaxis_title='Continent',yaxis_title='Country'),use_container_width=True)

# Prepare second page in the dashboard
elif page =='Correlation Analysis':
    st.subheader('Correlation Analysis')

# Create tabs to distribute our insight in
    page2_tab1,page2_tab2,page2_tab3,page2_tab4,page2_tab5 = st.tabs(['Overall Correlations','Socioeconomic Factors','Healthcare Factors','Nutritional Status Factotrs','Conclusion'])
# Design page layout    
    with page2_tab1:
        page2_tab1_col1,=st.columns(1)
        with page2_tab1_col1:
# Studying factors affecting our target column (Life Expectancy)
            num_clean= life.select_dtypes(include='number')
            life_exp_corr = num_clean['life_expectancy']
            st.plotly_chart(px.imshow(num_clean.corrwith(life_exp_corr).sort_values(ascending=False).to_frame().round(2) , text_auto=True, width=1000, height=800,color_continuous_scale='RdYlGn', 
                                    zmin=-1,zmax=1,title='Correlation with Life Expectancy'),use_container_width=True)
            st.divider()
            st.markdown("""
                        The top three factors positively correlated with Life Expectancy are Schooling, 
                        Income Composition of Resources, and BMI. Conversely, the top three factors negatively 
                        correlated with Life Expectancy are Adult Mortality, HIV/AIDS, and Thinnes.
                        """)
                                

        with page2_tab2:
# Study correlations between socioeconomic factors
            key_se_factors = ['gdp','schooling','income_composition_of_resources','percentage_expenditure']
            with st.container(border=True):
                st.plotly_chart(px.imshow(region_year_filtered_life[key_se_factors].corr().round(2),color_continuous_scale='RdYlGn',text_auto=True,width=800, height=600
                        ,zmin=-1,zmax=1,title='Correlation between Socioeconomic Factors'),use_container_width=True)
                
                st.divider()
                st.markdown("""
                            *   Schooling and Income Composition of Resources are strongly correlated with each other.
                            *   GDP is strongly correlated with Healthcare expenditure percentage.
                            """)
            
            page2_tab2_second_col, page2_tab2_second_col2 =st.columns(2)
            with page2_tab2_second_col:
# Display the average health expenditure percentage from GDP for each country status
                status_exp_percent = year_filtered_life.groupby('status')['expenditure_percent_from_gdp'].mean().round(2).reset_index()
                status_exp_percent_pie = px.pie(status_exp_percent,names='status',values='expenditure_percent_from_gdp',
                                title='Average Health Expenditure Percentage from GDP<br>by Development Status')
                status_exp_percent_pie.update_traces(texttemplate='%{label}<br>%{value} %<br>(%{percent})',showlegend=False)

                with st.container(border=True):
                    st.plotly_chart(status_exp_percent_pie,use_container_width=True)
                    st.divider()
                    st.markdown("""In developed countries about 10% on average from GDP goes to healthcare expenditure unlike developing countries which spend 7%. """)
            with page2_tab2_second_col2:
# Life expectancy per country development status
                lifeex_per_status = life.groupby('status')['life_expectancy'].mean().reset_index()
                with st.container(border=True):
                    st.plotly_chart(px.histogram(lifeex_per_status,x='status',y='life_expectancy',height=476,title='Average Life Expectancy per Development Status').update_layout(
                            xaxis_title='Development Status', yaxis_title='Life Expectancy'),use_container_width=True)
                    st.divider()
                    st.markdown("""The Average Life Expectancy in developed countries is greater than that of developing countries. """)

            page2_tab2_thrd_col1,page2_tab2_thrd_col2=st.columns(2)
            with page2_tab2_thrd_col1:
# Average Schooling per country development status
                schol_per_status = life.groupby('status')['schooling'].mean().reset_index()
                with st.container(border=True):
                    st.plotly_chart(px.histogram(schol_per_status,x='status',y='schooling',title='Average Schooling Per Development Status').update_layout(
                    xaxis_title='Development Status', yaxis_title='Schooling'),use_container_width=True)

                    st.divider()
                    st.markdown("""The Average Schooling in developed countries is greater than that of developing countries.""")

 # Average HDI per country development status 
            with page2_tab2_thrd_col2:
                hdi_per_status = life.groupby('status')['income_composition_of_resources'].mean().reset_index()
                with st.container(border=True):
                    st.plotly_chart(px.histogram(hdi_per_status,x='status',y='income_composition_of_resources',title='Average HDI Per Development Status').update_layout(
                             xaxis_title='Development Status', yaxis_title='HDI'),use_container_width=True)  
                    st.divider()
                    st.markdown("""The Average Income Composition of Resources in developed countries is greater than that of developing countries. """) 


        with page2_tab3:
# Corrleation between life expectancy and health factors            
            region_year_filtered_life_num = region_year_filtered_life.select_dtypes('number')
            soc_life_corr= region_year_filtered_life_num[['hepatitis_b','polio','diphtheria','hiv/aids','adult_mortality']].corrwith(region_year_filtered_life_num['life_expectancy']).round(2).sort_values(ascending=False).to_frame()
            st.plotly_chart(px.imshow(soc_life_corr,color_continuous_scale='RdYlGn',title='Life Expectancy and Health Factors',text_auto=True,zmin=-1,zmax=1))
            
            page2_tab3_col1,page2_tab3_col2=st.columns(2)
            with page2_tab3_col1:
# Corrleation between schooling and health factors
                schol_health_corr = region_year_filtered_life_num[['hepatitis_b','polio','diphtheria','hiv/aids','adult_mortality']].corrwith(
                    region_year_filtered_life_num['schooling']).round(2).sort_values(ascending=False).to_frame()
                st.plotly_chart(px.imshow(schol_health_corr,color_continuous_scale='RdYlGn',title='Schooling and Health Factors',text_auto=True,zmin=-1,zmax=1))
            
            with page2_tab3_col2:
# Corrleation between HDI and health factors
                hdi_health_corr =region_year_filtered_life_num[['hepatitis_b','polio','diphtheria','hiv/aids','adult_mortality']].corrwith(
                    region_year_filtered_life_num['income_composition_of_resources']).round(2).sort_values(ascending=False).to_frame()
                st.plotly_chart(px.imshow(hdi_health_corr,color_continuous_scale='RdYlGn',title='HDI and Health Factors',text_auto=True,zmin=-1,zmax=1))

        with page2_tab4:
            page2_tab4_col1, page2_tab4_col2 = st.columns(2)
            with page2_tab4_col1:
# Visualizing correlation between GDP and BMI segmented by country status
                st.plotly_chart(px.scatter(life,x='gdp',y='bmi',color='status',trendline='ols',
                            labels={'bmi':'BMI','gdp':'GDP','status':'Status'},
                            title='GDP and BMI by Country Development Status'),use_container_width=True)
            with page2_tab4_col2:
# Visualizing correlation between GDP and Thinness(5-9 Years) segmented by country status
                st.plotly_chart(px.scatter(life,x='gdp',y='thinness_5-9_years',color='status',trendline='ols',
                            labels={'gdp':'GDP','thinness_5-9_years':'Thinness(5-9 Years)','status':'Status'},
                            title='GDP and Thinness(5-9 Years) by Country Development Status'),use_container_width=True)
            page2_tab4_second_col1, = st.columns(1)
            with page2_tab4_second_col1:
# Visualizing correlation between GDP and Thinness(10-19 Years) segmented by country status
                st.plotly_chart(px.scatter(life,x='gdp',y='thinness_10-19_years',color='status',trendline='ols',
                         labels={'gdp':'GDP','thinness_10-19_years':'Thinness(10-19 Years)','status':'Status'},
                        title='GDP and Thinness(10-19 Years) by Country Development Status'),use_container_width=True)
 # Write conclusion page
        with page2_tab5:   
            st.subheader('Conclusion')
            st.markdown("""
*   Schooling, Income Composition of Resources and Adult Mortality are strongly correlate with Life Expectancy.
*   GDP is strongly correlated with Healthcare Percentage Expenditure.
*   In developed countries about 10% on average from GDP goes to healthcare expenditure unlike developing countries which spend 7% , 
    putting in considerations that developed countries have higher GDP.
*   There is obvious correlation between Polio/Diphtheria vaccinations and Life Expectancy in developing countries unlike developed ones. 
*   In developing countries larger portion of GDP is spent on food which is suggested to be a priority in those countries.
""")    
# Prepare third page in dashboard
elif page=='Time Series Analysis':
    st.subheader('Time Series Analysis')

# Create tabs to distribute our insight in
    page3_tab1,page3_tab2 = st.tabs(['Plots','Conclusion'])
# Design page layout
    with page3_tab1:

        page3_tab1_col1,page3_tab1_col2 = st.columns(2)

    with page3_tab1_col1:
# Visualizing average GDP trend
            gdp_per_year = region_filtered_life.groupby('year')['bmi'].mean().sort_index().reset_index()
            st.plotly_chart(px.line(gdp_per_year,x='year',y='bmi',
            labels={'gdp':'GDP','bmi':'BMI'},
                    title='Average BMI trend by Year'),use_container_width=True)
            
# Visualizing average schooling trend
            schooling_trend = region_filtered_life.groupby('year')['schooling'].mean().sort_index().reset_index()
            st.plotly_chart(px.line(schooling_trend,x='year',y='schooling',
                                    title='Average Schooling Trend').update_layout(xaxis_title='Year',yaxis_title='Schooling'),use_container_width=True)
            
    with page3_tab1_col2:
# Visualizing average Income Composition of Resources trend
            income_trend = region_filtered_life.groupby('year')['income_composition_of_resources'].mean().sort_index().reset_index()
            st.plotly_chart(px.line(income_trend,x='year',y='income_composition_of_resources',title='Average HDI Trend').update_layout(
                    xaxis_title='Year',yaxis_title='HDI'),use_container_width=True)
            
# Visualizing average adult mortality trend
            adult_mortality_trend = region_filtered_life.groupby('year')['adult_mortality'].mean().sort_index().reset_index()
            st.plotly_chart(px.line(adult_mortality_trend,x='year',y='adult_mortality',title='Average Adult Mortality Trend').update_layout(
                    xaxis_title='Year',yaxis_title='Adult Mortality'),use_container_width=True)
            
 # Write conclusion page
    with page3_tab2:
        st.subheader('Conclusion')
        st.markdown("""
*   Life Expectancy increased over time.
*   There is a rising trend in BMI/Schooling and Income Composition of Resources while a downward trend is observed in Adult Mortality.
*   These factors are strongly correlated to Life Expectancy which led to its increase.
 """)
# Prepare fourth page in dashboard
elif page == 'Regional Analysis':
    st.subheader('Regional Analysis')

# Create tabs to distribute our insight in
    page4_tab1,page4_tab2= st.tabs(['Plots','Conclusion'])

# Design page layout
    with page4_tab1:
        page4_tab1_col1, page4_tab1_col2 = st.columns(2)

        with page4_tab1_col1:
# Visualizing average life expectancy by continent
            life_expectancy_per_continent = year_filtered_life.groupby('continent')['life_expectancy'].mean().round(2).sort_values().reset_index()
            st.plotly_chart(px.histogram(life_expectancy_per_continent,x='life_expectancy',y='continent',text_auto=True,title='Average Life Expectancy by Continent').update_layout(
                        xaxis_title='Life Expectancy',yaxis_title='Continent'),use_container_width=True)
            
# Visualizing average income composition of resources by continent
            hdi_per_cont=year_filtered_life.groupby('continent')['income_composition_of_resources'].mean().sort_values().reset_index().round(2)
            st.plotly_chart(px.histogram(hdi_per_cont,y='continent',x='income_composition_of_resources',text_auto=True,title='Average HDI by Continent').update_layout(
                         xaxis_title='HDI',yaxis_title='Continent'),use_container_width=True)
# Top 10 countries by life expectancy
            country_per_lifeex =region_year_filtered_life.groupby(['country','status'])['life_expectancy'].mean().sort_values(ascending=False).reset_index()
            st.plotly_chart(px.histogram(country_per_lifeex.head(10),x='country',y='life_expectancy',color='status',title='Top 10 Countries by Life Expectancy',color_discrete_map={'Developed': 'green', 'Developing': 'red'}).update_layout(
                            xaxis_title='Country',yaxis_title='Life Expectancy',legend_title='Status'),use_container_width=True)
# Visualizing average thinness in 10-19 year by continent
            thin1019_per_cont = year_filtered_life.groupby('continent')['thinness_10-19_years'].mean().sort_values().reset_index().round(2)
            st.plotly_chart(px.histogram(thin1019_per_cont,y='continent',x='thinness_10-19_years',text_auto=True,title='Average Thinness (10-19 Years) by Continent').update_layout(
                xaxis_title='Thinness (10-19 Years)',yaxis_title='Continent'),use_container_width=True)
                
        with page4_tab1_col2:
# Visualizing average schooling by continent
            school_per_cont = year_filtered_life.groupby('continent')['schooling'].mean().sort_values().reset_index().round(2)
            st.plotly_chart(px.histogram(school_per_cont,y='continent',x='schooling',text_auto=True,title='Average Schooling by Continent').update_layout(
                            xaxis_title='Schooling',yaxis_title='Continent'),use_container_width=True)
# Visualizing average adult mortality by continent
            bmi_per_cont = year_filtered_life.groupby('continent')['adult_mortality'].mean().round(2).sort_values().reset_index()
            st.plotly_chart(px.histogram(bmi_per_cont,x='adult_mortality', y='continent',text_auto=True ,title='Average Adult Mortality by Continent').update_layout(
                xaxis_title='Continent', yaxis_title='Adult Mortality'),use_container_width=True)        
# Bottom 10 countries by life expectancy
            st.plotly_chart(px.histogram(country_per_lifeex.tail(10).iloc[::-1],x='country',y='life_expectancy',color='status',title='Bottom 10 Countries by Life Expectancy',color_discrete_map={'Developed': 'green', 'Developing': 'red'}).update_layout(
                        xaxis_title='Country',yaxis_title='Life Expectancy',legend_title='Status'),use_container_width=True)
            
# Visualizing average thinness in 5-9 year by continent
            thin59_per_cont=year_filtered_life.groupby('continent')['thinness_5-9_years'].mean().sort_values().reset_index().round(2)
            st.plotly_chart(px.histogram(thin59_per_cont,y='continent',x='thinness_5-9_years',text_auto=True,title='Average Thinness (5-9 Years) by Continent').update_layout(
                xaxis_title='Thinness (5-9 Years)',yaxis_title='Continent'),use_container_width=True)




    with page4_tab2:
        st.subheader('Observation')
        st.markdown("""
*    Japan has highest Life Expectancy; however, it is in Asia which comes directly after Africa that has the lowest Life Expectancy.
*    Something needs more investigation, we are going to focus on key drivers for Life Expectancy (Schooling, HDI, Adult Mortality). """)
        st.divider()
# Investigating Japan aganist other countries to study the reason of its highest life expectancy
        page4_tab2_second_col1, page4_tab2_second_col2=st.columns(2)
        with page4_tab2_second_col1:
            if country == 'All':
                st.info('Select One Country')
            else:
                country_df = life[life['country'] == country]
                st.plotly_chart(px.line(country_df,x='year',y='life_expectancy',labels={'year':'Year','life_expectancy':'Life Expectancy'},
                        title=f'Life Expectancy Trend in {country}'),use_container_width=True)
                
            if country == 'All':
                st.info('Select One Country')
            else:
                country_df = life[life['country'] == country]
                st.plotly_chart(px.line(country_df,x='year',y='income_composition_of_resources',labels={'year':'Year','income_composition_of_resources':'HDI'},
                        title=f'HDI Trend in {country}'),use_container_width=True)
                
        with page4_tab2_second_col2:
            if country == 'All':
                st.info('Select One Country')
            else:
                country_df = life[life['country'] == country]
                st.plotly_chart(px.line(country_df,x='year',y='schooling',labels={'year':'Year','schooling':'Schooling'},
                        title=f'Schooling Trend in {country}'),use_container_width=True)
            if country == 'All':
                st.info('Select One Country')
            else:
                country_df = life[life['country'] == country]
                st.plotly_chart(px.line(country_df,x='year',y='adult_mortality',labels={'year':'Year','adult_mortality':'Adult Mortality'},
                        title=f'Adult Mortality Trend in {country}'),use_container_width=True)
        page4_tab2_thrd_col1,=st.columns(1)
        with page4_tab2_thrd_col1:
# Create DataFrame for top Life Expectancy and Schooling countries (Japan, Italy, Spain)
            top_three_lifeex_school = life[life['country'].isin(['Japan','Italy','Spain'])].groupby('country')['gdp'].mean().round(2).sort_values(ascending=False).reset_index()
# Calculating their contribution in total GDP in our dataset
            top_three_lifeex_school['global_gdp']=life['gdp'].sum().round(2)
            top_three_lifeex_school['global_gdp_contribution']=((top_three_lifeex_school['gdp']/top_three_lifeex_school['global_gdp'])*100).round(2)
# Study their Percentage Expenditure
            exp_lookup= life[life['country'].isin(['Japan','Italy','Spain'])].groupby('country')['percentage_expenditure'].mean().round(2)
            top_three_lifeex_school['percentage_expenditure']=top_three_lifeex_school['country'].map(exp_lookup)
# Study their Expenditure percentage that goes to healthcare from GDP
            percnt_exp_lookup = life[life['country'].isin(['Japan','Italy','Spain'])].groupby('country')['expenditure_percent_from_gdp'].mean().round(2)
            top_three_lifeex_school['expenditure_percent_from_gdp']=top_three_lifeex_school['country'].map(percnt_exp_lookup)
# Drop global_gdp column as it is not necessary we just used it as helper in some calculations
            top_three_lifeex_school=top_three_lifeex_school.drop(columns=['global_gdp'])
# Rename Columns 
            top_three_lifeex_school=top_three_lifeex_school.rename(columns=
                                        {'country':'Country','gdp':'GDP','global_gdp_contribution':'Global GDP Contribution (%)',
                                            'percentage_expenditure':'Percentage Expenditure','expenditure_percent_from_gdp':'Expenditure Percent from GDP'})
            st.dataframe(top_three_lifeex_school)

 # Write conclusion page
        st.divider()
        st.subheader('Conclusion')
        st.markdown("""
*   Highest Life Expectancy appears in Europe while Lowest appear in Africa.
*   Europe has the highest average Schooling, HDI, and lowest Adult Mortality rates. In addition, it has the highest count of developed countries, all of which justify its high average Life Expectancy.
*   While Africa has the highest count of countries -none of them are developed- it has the lowest average schooling and HDI, and the highest adult mortality rates, all of which justify its low average Life Expectancy.
*   Average Life Expectancy in Asia appears to be the lowest among the remaining continents; however, it has the highest count of developed countries among them. This can be justified by the prevalence of thinness in the region.
*   Japan has the highest life expectancy in the dataset showing consistent uptrend in Life Expectancy unlike other top 10 countries.
*   After further investigation top 10 countries shows similar trends in HDI and Adult Mortality.
*   Japan shows consistent uptrend in Schooling and same observed in Italy and Spain.
*   After investigation we observed that Japan has highest Global GDP Contribution Percentage and Percentage Expenditure.
*   Spain has highest Expenditure Percent from GDP but putting in consideration it has relatively low Global GDP Contribution Percentage and Percentage Expenditure than Japan.
*   While GDP and percentage expenditure serve as moderate influencers of life expectancy, they allow Japan to dominate over other countries.
*   All of which justifies that Japan can spend more for healthcare excellence compared to Italy and Spain concluding that it is reasonable to find Japan has the highest Average Life Expectancy in our dataset.                 
 """)
# Prepare Recommendation Page       
elif page == 'Recommendations':
    st.subheader('Recommendations')
    st.success("""
The strong association between schooling and the Human Development Index (HDI), 
along with their combined influence on life expectancy, highlights education as 
a key driver of population outcomes. Effective educational strategies 
contribute to aware and more skilled population capable of allocating resources efficiently, 
which in turn supports the development of stronger education systems, 
creating a cycle of sustained socio-economic improvement.
 """)



            

    








            
            
            

               
            


           



