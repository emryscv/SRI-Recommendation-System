import streamlit as st
import dealer


def delete(item):
    st.session_state.user_ratings.pop(item)


def find(term, item):
    term = term.lower()
    return (
        term in item["Product Name"].lower()
        or term in item["Brand"].lower()
        or term in item["Category"].lower()
        or term in item["Color"].lower()
    )


def to_str(item):
    return (
        str(item.name)
        + ", "
        + item["Product Name"]
        + ", "
        + item["Brand"]
        + ", "
        + item["Category"]
        + ", "
        + item["Color"]
    )


# Inicializar el estado de la sesión para las selecciones y valoraciones
if "user_ratings" not in st.session_state:
    st.session_state.user_ratings = {}

if not (dealer.get_load_state):
    dealer.load_dataset()

items_list = dealer.get_items()
categories = dealer.get_categories()

st.title("Sistema de Recomendación")

st.write("Filtro de Categorias. Danos un poco de información sobre tus preferencias")

colL, colR = st.columns(2, gap="large")

colL1, colL2 = colL.columns(2)

filtered_categories = {}

for id, (cat, values) in enumerate(categories.items()):
    if id % 2 == 0:
        filtered_categories[cat] = colL1.multiselect(cat, values)
    else:
        filtered_categories[cat] = colL2.multiselect(cat, values)

max_price = colL.slider("Precio maximo", 0, dealer.get_max_price(), 60)
filtered_categories["Price"] = max_price

colR.write()

# Barra de búsqueda
search_term = colR.text_input("Valora los items que has comprado (0-5).")

# Filtrar los items basados en el término de búsqueda
filtered_items = [to_str(item) for item in items_list if find(search_term, item)]

colR1, colR2 = colR.columns([0.8, 0.2])
# Crear un widget de selección múltiple para los items filtrados
selected_items = []
selected_item = colR1.selectbox("Selecciona los items comprados", filtered_items)
if colR2.button("Add"):
    selected_items.append(selected_item)
    
# Actualizar el estado de la sesión con las nuevas selecciones y sus valoraciones
for item in selected_items:
    if item not in st.session_state.user_ratings:
        st.session_state.user_ratings[item] = 3  # Valoración por defecto

items_to_delete = []

# Mostrar sliders para todos los items seleccionados y permitir que el usuario les dé una valoración
if st.session_state.user_ratings:
    colR.write("Items seleccionados y valoraciones:")
    cols = {}
    for index, item in enumerate(st.session_state.user_ratings):
        cols[index] = colR.columns([0.9, 0.1])
        st.session_state.user_ratings[item] = cols[index][0].slider(
            f"Item: {item}", 1, 5, st.session_state.user_ratings[item]
        )
        if cols[index][1].button("X", item):
            items_to_delete.append(item)

for item in items_to_delete:
    st.session_state.user_ratings.pop(item)
    if item in selected_items:
        selected_items.remove(item)
# Botón para obtener recomendaciones
if st.button("Obtener Recomendaciones"):
    if len(st.session_state.user_ratings) == 0:
        st.write("Selecciona algun elemento")
    else:
        recommendations = dealer.get_recomendations(
            filtered_categories, st.session_state.user_ratings
        )
        st.write("Items recomendados:")
        for item, score in recommendations.items():
            st.write(f"Item: {item}, Puntuación: {score}")
