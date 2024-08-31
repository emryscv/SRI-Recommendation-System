import streamlit as st
import dealer


# Inicializar el estado de la sesión para las selecciones y valoraciones
if 'user_ratings' not in st.session_state:
    st.session_state.user_ratings = {}

if(not(dealer.get_load_state)):
    dealer.load_dataset()

items_list = dealer.get_items()


def get_recommendations(user_ratings):
   
    return user_ratings


st.title('Sistema de Recomendación')


st.write('Selecciona los items que has comprado y dales una valoración (0-5). Luego, presiona el botón para obtener recomendaciones.')

# Barra de búsqueda
search_term = st.text_input('Buscar items')

# Filtrar los items basados en el término de búsqueda
filtered_items = [item for item in items_list if search_term.lower() in item.lower()]

# Crear un widget de selección múltiple para los items filtrados
selected_items = st.multiselect('Selecciona los items comprados', filtered_items)

# Actualizar el estado de la sesión con las nuevas selecciones y sus valoraciones
for item in selected_items:
    if item not in st.session_state.user_ratings:
        st.session_state.user_ratings[item] = 3  # Valoración por defecto

# Mostrar sliders para todos los items seleccionados y permitir que el usuario les dé una valoración
if st.session_state.user_ratings:
    st.write("Items seleccionados y valoraciones:")
    for item in st.session_state.user_ratings:
        st.session_state.user_ratings[item] = st.slider(f'Valoración para el item {item}', 1, 5, st.session_state.user_ratings[item])

# Botón para obtener recomendaciones
if st.button('Obtener Recomendaciones'):
    recommendations = get_recommendations(st.session_state.user_ratings)
    st.write('Items recomendados:')
    for item, score in recommendations.items():
        st.write(f'Item: {item}, Puntuación: {score}')





