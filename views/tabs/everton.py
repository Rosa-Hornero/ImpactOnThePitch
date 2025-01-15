import streamlit as st

import pandas as pd
import plotly.express as px
import altair as alt


from utils import load_data, count_results, media_FIFA


def render_everton_tab():
    st.title('🏰 Everton')
    
    # Dividir el diseño en columnas
    cola, colb = st.columns([1, 3])  

    # Columna izquierda: Escudo del equipo
    with cola:
        st.image("static/images/escudos/everton_logo.png", caption="Logo of Everon", width=150)

    # Columna derecha: Historia del equipo
    with colb:
        st.write("""
                **Everton Football Club**  
                Established in 1878, Everton is one of England's most historic and successful football clubs. Known as "The Toffees," the team plays its home matches at the iconic Goodison Park in Liverpool. With their signature royal blue jerseys, Everton has a proud history that includes multiple league titles, FA Cups, and a European Cup Winners' Cup. Renowned for its passionate fan base and deep community ties, Everton continues to strive for success while honoring its rich tradition in English football.
            """)
    
    # Leemos los datos
    data = load_data()

    # Datos Everton
    everton_data = data[data['Team Name'] == 'Everton']


    # Filtrar por temporada
    seasons = everton_data['Season'].unique()  
    selected_season = st.selectbox("Select a Season", options=seasons)
    fil_seas_data = everton_data[everton_data['Season'] == selected_season]

    # Filtrado por jugador
    players = fil_seas_data['Name'].unique()
    selected_player = st.selectbox("Select a Player",index=None,placeholder="Select a player...", options=players)
    player_data =  fil_seas_data[fil_seas_data['Name'] == selected_player]

    ### CALCULOS DE ESTADISTICAS
    # Medias de duracion de la lesión
    try: 
        tiempo_ini = fil_seas_data['Date of Injury']
        tiempo_ini = pd.to_datetime(tiempo_ini, errors='coerce')

        tiempo_fin = fil_seas_data['Date of return']
        tiempo_fin = pd.to_datetime(tiempo_fin, errors='coerce')
        duracion = (tiempo_fin - tiempo_ini).dt.days
        average_injury_duration = duracion.mean()
    except:
        average_injury_duration=-1
    
    # Media de edad
    team_avg_age = fil_seas_data['Age'].mean()  
    
    # Media de FIFA rating
    team_avg_fifa_rating = fil_seas_data['FIFA rating'].mean()  


    if selected_player == None:
        st.header(f'General Metrics for {selected_season}')

        st.write(f"Here you can see the general injury metrics of **Everton for the session {selected_season}**. You can see the **total number of injured players**, the **average injury time** and the **average age** of the injured players. You can also view different graphs to see the **most frequent type of injury** and the **most affected positions**. Also included is a **calendar** where you can see **all the injuries** of the team this season.")

        ### Total de lesiones en la temporada
        total_injuries = fil_seas_data['Name'].nunique()
        colu11, colu12, colu13 = st.columns(3)
        colu11.metric(label=f"**Total players injured in {selected_season}**", value=int(total_injuries), border=True)


        ### Duración promedio de lesiones
        if average_injury_duration == -1:
            #st.write(f'No valid data available to calculate **average injury duration**.')
            show_time=0
            colu12.metric(label=f"**Average injury duration in {selected_season}**", value='NaN', border=True)
        else:
            #st.write(f"**Average injury duration in {selected_season}:** {average_injury_duration:.2f} days")
            colu12.metric(label=f"**Average injury duration in {selected_season}**", value=f'{average_injury_duration:.2f} days', border=True)
            show_time=1
        
        colu13.metric(label=f"**Average age of injured playersin {selected_season}**", value=f'{team_avg_age:.2f} years', border=True)

        ### Lesiones en gráfico
        common_injuries = fil_seas_data['Injury'].value_counts()

        common_injuries = fil_seas_data['Injury'].value_counts().reset_index()
        common_injuries.columns = ['Injury', 'Count']

        chart = alt.Chart(common_injuries).mark_bar().encode(
            x='Injury:O',
            y='Count:Q',
            color=alt.Color('Injury:N', scale=alt.Scale(scheme='category20b'))  
        ).properties(
            title="Most Common Injuries",
            width=600
        )

        st.altair_chart(chart, use_container_width=True)

        
        ### Número de jugadores lesionados por posición
        positions_data = fil_seas_data['Position'].value_counts().reset_index()
        positions_data.columns = ['Position', 'Count']

        # Crear gráfico de barras con colores
        fig = px.bar(
            positions_data,
            x='Position',
            y='Count',
            color='Position',  
            title="Number of Injured Players by Position",
            labels={'Count': 'Number of Players'},
            color_discrete_sequence=px.colors.qualitative.Set2  
        )

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig, use_container_width=True)


        # Agrupar datos por posición, tipo de lesión e incluir el promedio de edad
        grouped_data = fil_seas_data.groupby(['Position', 'Injury']).agg({
            'Age': 'mean',  # Edad promedio
            'Name': 'count'  # Número de jugadores lesionados por combinación
        }).reset_index()

        # Renombrar la columna 'Name' para que sea más descriptiva
        grouped_data.rename(columns={'Name': 'Num_Injuries'}, inplace=True)

        # Crear el gráfico de dispersión
        fig = px.scatter(
            grouped_data,
            x='Position',
            y='Injury',
            size='Num_Injuries',  # Tamaño del punto basado en el número de lesiones
            color='Age',  # Color según la edad promedio
            hover_data={'Num_Injuries': True, 'Age': True},  # Mostrar estos datos al pasar el mouse
            title="Comparación de Edad, Posición y Tipo de Lesión",
            labels={
                'Position': 'Position',
                'Injury': 'Type of Injury',
                'Num_Injuries': 'Number of Injuries',
                'Age': 'Average Age'
            }
        )

        # Mostrar el gráfico en Streamlit
        #st.plotly_chart(fig)

        # Agrupar datos por edad, posición y tipo de lesión
        grouped_data = fil_seas_data.groupby(['Age', 'Position', 'Injury']).agg({
            'Name': 'count'  # Número de jugadores lesionados en esta combinación
        }).reset_index()

        # Renombrar la columna 'Name' para mayor claridad
        grouped_data.rename(columns={'Name': 'Num_Injuries'}, inplace=True)

        # Crear el gráfico de dispersión
        fig = px.scatter(
            grouped_data,
            x='Age',  # Edad en el eje X
            y='Position',  # Posición en el eje Y
            size='Num_Injuries',  # Tamaño del punto basado en el número de lesiones
            color='Injury',  # Color basado en el tipo de lesión
            hover_data={'Num_Injuries': True},  # Mostrar el número de lesiones al pasar el mouse
            title="Relación entre Edad, Posición y Tipo de Lesión",
            labels={
                'Age': 'Age',
                'Position': 'Position',
                'Injury': 'Type of Injury',
                'Num_Injuries': 'Number of Injuries'
            }
        )

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig)

        ### Gráfico del tiempo
        if show_time==1:
            # Se asegura que este en datos de tiempo
            fil_seas_data['Date of Injury'] = pd.to_datetime(fil_seas_data['Date of Injury'], errors='coerce')
            fil_seas_data['Date of return'] = pd.to_datetime(fil_seas_data['Date of return'], errors='coerce')

            # Calcular días de recuperación
            fil_seas_data['Days Injured'] = (fil_seas_data['Date of return'] - fil_seas_data['Date of Injury']).dt.days

            
            # Crear un DataFrame para el diagrama de Gantt
            gantt_data = fil_seas_data[['Name', 'Position', 'Date of Injury', 'Date of return', 'Days Injured', 'Injury']].dropna()
            gantt_data = gantt_data.rename(columns={
                'Name': 'Player',
                'Date of Injury': 'Start',
                'Date of return': 'Finish',
                'Days Injured': 'Days'
            })

            # Crear el gráfico de Gantt
            fig = px.timeline(
                gantt_data,
                x_start="Start",
                x_end="Finish",
                y="Player",
                color="Position",  # Colorea las barras según la posición del jugador
                title="Timeline of Player Injuries",
                labels={"Player": "Player", "Position": "Position", "Days": "Days Injured", "Injury": "Injury Type"},
                hover_data=["Days", "Injury"]  # Información adicional al pasar el ratón
            )

            # Ajustar el diseño del gráfico
            fig.update_yaxes(categoryorder="total ascending")  # Ordenar los jugadores por total
            fig.update_layout(
                xaxis_title="Timeline",
                yaxis_title="Player",
                legend_title="Position",
                height=600,
                margin=dict(l=50, r=50, t=50, b=50),
            )

            # Mostrar el gráfico en Streamlit
            st.plotly_chart(fig, use_container_width=True)

        #st.dataframe(fil_seas_data)
    else:
        st.header(f'Metrics for {selected_player} in {selected_season}')
        
        posicion = player_data['Position'].values[0]
        if posicion == 'Central Midfielder ':
            posicion='Central Midfielder'


        # Dividir el diseño en columnas
        col1, col2 = st.columns([2, 3])  

        # Columna izquierda: Escudo del equipo
        with col1:
            st.image(f"static/images/positions/{posicion}.png", caption=f"Name: {selected_player}", width=250)
            if posicion == 'Attacking Midfielder':
                st.image(f"static/images/positions/Campo Central Midfielder.png", caption=f"Position: {posicion}", width=250)
            else: 
                st.image(f"static/images/positions/Campo {posicion}.png", caption=f"Position: {posicion}", width=250)
        # Columna derecha: Historia del equipo
        with col2:

            # METRICAS DE EDAD Y FIFA RATING
            st.write(' ')
            # Obtener datos del jugador seleccionado
            player_age = player_data['Age'].iloc[0]  # Edad del jugador
            fifa_rating_mean = player_data['FIFA rating'].mean()  # Calificación FIFA promedio

            # Calcular las diferencias (deltas)
            age_delta = player_age - team_avg_age
            fifa_delta = fifa_rating_mean - team_avg_fifa_rating  

            col21, col22 = st.columns(2) 
            col21.metric(label="Age", value=int(player_age), delta=f"{age_delta:.1f} years",delta_color="inverse", border=False)
            col21.caption(f"Compared to the team's average age of {team_avg_age:.1f} years.")
            col22.metric(label="Average FIFA Rating", value=f"{fifa_rating_mean:.1f}", delta=f"{fifa_delta:.1f} pts", delta_color="normal",  border=False)
            col22.caption(f"Compared to the team's average FIFA rating of {team_avg_fifa_rating:.1f}.")
            st.write(' ')
            # HISTORIAL DE LESIONES
            st.subheader("Injury History")
            #st.write(' ')
            st.write("""
                In this section, you can explore a detailed table of all recorded injuries for the selected player.  
                Additionally, the pie chart below provides a visual representation of the distribution of injury types, helping to identify patterns in the player's injury history.
            """)
            tiempo_ini = player_data['Date of Injury']
            tiempo_fin = player_data['Date of return']
 
            tiempo_ini = pd.to_datetime(tiempo_ini,errors='coerce')
            tiempo_fin = pd.to_datetime(tiempo_fin,errors='coerce')
            player_data['Duration in days'] = (tiempo_fin - tiempo_ini).dt.days
  

            col31, col32, col33 = st.columns([1,4,1]) 
            col32.dataframe(player_data[['Injury', 'Date of Injury', 'Date of return','Duration in days']], hide_index=True)

            # Filtrar datos por lesiones
            player_injury_data = player_data['Injury'].value_counts()

            # Crear gráfico circular con Plotly
            fig = px.pie(
                player_injury_data,
                names=player_injury_data.index,
                values=player_injury_data.values,
                title=f"Injury Type Distribution for {selected_player}",
                hole=0.4,  
                color_discrete_sequence=px.colors.sequential.Blues_r
            )
            st.plotly_chart(fig, use_container_width=True)

        # RENDIMIENTO DE PARTIDOS
        st.subheader("Performance Impact")

        st.write("""
        Here, you can explore how the selected player's injury impacted the team's performance. 
        First, choose a specific injury from the dropdown menu to display relevant metrics and visualizations. 

        The bar chart below  and the detailed table breaks provid a comparison of match results (wins, draws, and losses) across three key periods: 
        **before**, **during**, and **after** the injury. Additionally, you can review the **goal difference trends** for these periods, 
        offering deeper insights into the team's performance dynamics.  

        """)
        
        # Crear un ID de cada lesion
        player_data['Injury_Instance'] = player_data.groupby(['Name', 'Injury']).cumcount() + 1
        player_data['Injury_Display'] = player_data['Injury'] + " #" + player_data['Injury_Instance'].astype(str)
        
        # Selección de la lesión
        injury_list = player_data['Injury_Display'].unique()
        selected_injury = st.selectbox("Select an Injury to Analyze", options=injury_list)

        # Filtrar los datos por la instancia seleccionada
        injury_data = player_data[player_data['Injury_Display'] == selected_injury]
        
        name_injury = injury_data['Injury'].values[0]
        st.write(f"#### Performance Impact for {name_injury}")
        st.write(f"This section highlights the performance impact of the injury: **{name_injury}**. Metrics such as player ratings and team performance are analyzed.")
        
        col41, col42, col43 = st.columns(3)

        # Duración de la lesión
        injury_duration = injury_data['Duration in days'].iloc[0]  
        col41.metric(label="Injury Duration (days)", value=int(injury_duration), border=True)

        # Rendimiento antes y después
        pre_rating = injury_data[['Match1_before_injury_Player_rating', 'Match2_before_injury_Player_rating', 'Match3_before_injury_Player_rating']]
        post_rating = injury_data[['Match1_after_injury_Player_rating', 'Match2_after_injury_Player_rating', 'Match3_after_injury_Player_rating']]
        pre_rating_avg = media_FIFA(pre_rating.values.flatten())
        post_rating_avg = media_FIFA(post_rating.values.flatten())       
        delta_rating = post_rating_avg - pre_rating_avg

        col42.metric(label="Average Player Rating Before Injury", value=f"{pre_rating_avg:.1f}", border=True)
        col43.metric(label="Average Player Rating After Injury", value=f"{post_rating_avg:.1f}", delta=f"{delta_rating:.1f} pts", delta_color="normal",border=True)
        
        # RESULTADOS
        st.write(f"##### Results Before, During and After Injury")
        # Contar resultados por período
        results_before = injury_data[['Match1_before_injury_Result', 'Match2_before_injury_Result', 'Match3_before_injury_Result']].values.flatten()
        results_during = injury_data[['Match1_missed_match_Result', 'Match2_missed_match_Result', 'Match3_missed_match_Result']].values.flatten()
        results_after = injury_data[['Match1_after_injury_Result', 'Match2_after_injury_Result', 'Match3_after_injury_Result']].values.flatten()

        # Contar resultados para cada período
        before_counts = count_results(pd.Series(results_before))
        during_counts = count_results(pd.Series(results_during))
        after_counts = count_results(pd.Series(results_after))

        # Crear DataFrame para el gráfico
        data_chart = pd.DataFrame([
            {"Period": "Before Injury", "Result": "Win", "Count": before_counts["Win"]},
            {"Period": "Before Injury", "Result": "Draw", "Count": before_counts["Draw"]},
            {"Period": "Before Injury", "Result": "Loss", "Count": before_counts["Loss"]},
            {"Period": "During Injury", "Result": "Win", "Count": during_counts["Win"]},
            {"Period": "During Injury", "Result": "Draw", "Count": during_counts["Draw"]},
            {"Period": "During Injury", "Result": "Loss", "Count": during_counts["Loss"]},
            {"Period": "After Injury", "Result": "Win", "Count": after_counts["Win"]},
            {"Period": "After Injury", "Result": "Draw", "Count": after_counts["Draw"]},
            {"Period": "After Injury", "Result": "Loss", "Count": after_counts["Loss"]},
        ])

        # Crear gráfico de barras con Altair
        chart = alt.Chart(data_chart).mark_bar().encode(
            x=alt.X('Period:N', title="Period", sort=["Before Injury", "During Injury", "After Injury"] ),
            y=alt.Y('Count:Q', title="Number of Matches"),
            color=alt.Color('Result:N', title="Match Result", scale=alt.Scale(domain=["Win", "Draw", "Loss"],  range=["#002366", "#ADD8E6", "#FF0000"])),
            tooltip=['Period', 'Result', 'Count']
        ).properties(
            title="Team Performance Before, During, and After Injury",
            width=600,
            height=400
        )

        # Mostrar gráfico en Streamlit
        st.altair_chart(chart, use_container_width=True)

        # TABLA DE LOS RESULTADOS
        opposition_before = injury_data[['Match1_before_injury_Opposition', 'Match2_before_injury_Opposition', 'Match3_before_injury_Opposition']].values.flatten()
        opposition_during = injury_data[['Match1_missed_match_Opposition', 'Match2_missed_match_Opposition', 'Match3_missed_match_Opposition']].values.flatten()
        opposition_after = injury_data[['Match1_after_injury_Opposition', 'Match2_after_injury_Opposition', 'Match3_after_injury_Opposition']].values.flatten()

        before_o_r = pd.DataFrame([opposition_before, results_before], columns=("Match 1","Match 2", "Match 3"))
        during_o_r =  pd.DataFrame([results_during, opposition_during], columns=("Match 1","Match 2", "Match 3"))
        after_o_r =  pd.DataFrame([results_after, opposition_after], columns=("Match 1","Match 2", "Match 3"))

        col51, col52, col53 = st.columns(3) 
        col51.write('Matches before the injury')
        col51.dataframe(before_o_r, hide_index=True)
        col52.write('Matches during the injury')
        col52.dataframe(during_o_r, hide_index=True)
        col53.write('Matches after the injury')
        col53.dataframe(after_o_r, hide_index=True)

        # RESULTADOS
        st.write(f"##### Goal Difference Distribution")

        # Crear un DataFrame estructurado para las diferencias de goles
        gd_data = []

        for i in range(1, 4):
            # Antes de la lesión
            gd_data.append({
                "Period": "Before Injury",
                "Match": f"Match {i}",
                "Goal Difference": injury_data[f"Match{i}_before_injury_GD"].values[0]
            })
            # Durante la lesión
            gd_data.append({
                "Period": "During Injury",
                "Match": f"Match {i}",
                "Goal Difference": injury_data[f"Match{i}_missed_match_GD"].values[0]
            })
            # Después de la lesión
            gd_data.append({
                "Period": "After Injury",
                "Match": f"Match {i}",
                "Goal Difference": injury_data[f"Match{i}_after_injury_GD"].values[0]
            })

        # Convertir a DataFrame
        gd_df = pd.DataFrame(gd_data)

        # Reemplazar NaN por "No Data"
        gd_df['Goal Difference'] = gd_df['Goal Difference'].fillna("No Data")

        # Crear el gráfico de barras con diferenciación visual
        fig = px.bar(
            gd_df,
            x="Period",
            y="Goal Difference",
            color="Match",
            barmode="group",
            title=f"Goal Difference Analysis for {selected_player}",
            color_discrete_sequence=px.colors.qualitative.Dark24,  # Colores mejorados
            category_orders={"Period": ["Before Injury", "During Injury", "After Injury"]}  # Ordenar los períodos
        )

        # Personalizar la apariencia para "No Data"
        for trace in fig.data:
            trace.marker.line.width = 1  # Añadir borde a las barras
            trace.marker.line.color = "black"
            if "No Data" in gd_df['Goal Difference'].values:
                trace.marker.color = trace.marker.color.replace(
                    "#", "No Data Color Placeholder"
                )  # Cambiallo

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig)

        #st.dataframe(injury_data)
        #st.dataframe(player_data)

