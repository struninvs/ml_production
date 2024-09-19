import streamlit as st

from services.trends_indicator.ml import predict_trends

st.set_page_config(
    page_title="DLS | Trends Indicator",
    page_icon="💬"
)

def clear_text() -> None:
    st.session_state["text_input_area"] = ""

def main()-> None:

    st.header(f"Классификация Пользовательского контента", divider='rainbow')     
    
    st.markdown("<b>Описание:</b><br>\
                В рамках данного примера, мы решаем задачу множественной классификации для определения всех классов, к которым можно отнести отзыв Пользователя о Сервисе.\
                Множественная классификация отличается от многоклассовой тем, что экземпляр данных может одновременно относиться сразу к нескольким классам.\
                На вход модели мы подаём только комментарий Пользователя и пытаемся определить для него 50 различных меток классов, к которым он может относиться.", unsafe_allow_html = True)

    review = st.text_area(label = "Введите текст отзыва:", key = "text_input_area", value = "")

    col_1, col_2 = st.columns(2)

    col_1.button("Очистить", use_container_width = True, on_click=clear_text)
    if col_2.button("Отправить", type = "primary", use_container_width = True):
        if len(review) == 0:
            st.write(":red[Длина сообщения не может быть нулевой!]")
        else:
            response = predict_trends(data = review)
            response_dict = response.json()
            if len(response_dict["trends_list"]) > 0:
                st.write("<br><br>".join([f"<b>Name:</b> {trend[0]}<br><b>Description:</b><br>{trend[1]}" for trend in response_dict["trends_list"]]), unsafe_allow_html = True)
            else:
                st.write(":red[Не удалось определить тренды:(]")
    
    return None

if __name__ == "__main__":
    main()