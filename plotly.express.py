import plotly.express as px
import streamlit as st


# 브라우저 탭의 제목과 화면 폭 설정
st.set_page_config(
    page_title="GDP와 기대수명 변화",
    page_icon="🌍",
    layout="wide",
)

# 웹페이지에 표시할 제목과 안내
st.title("국가별 GDP와 기대수명 변화")
st.caption("Gapminder의 1952~2007년 자료를 5년 간격으로 살펴봅니다.")
st.write(
    "그래프 아래의 ▶ 버튼을 누르면 재생됩니다. "
    "연도 슬라이더로 원하는 연도를 선택할 수도 있습니다."
)


# 데이터 불러오기: 불러온 결과를 캐시에 저장
@st.cache_data
def load_data():
    return px.data.gapminder()


df = load_data()

labels = {
    "gdpPercap": "1인당 GDP (물가 조정 달러)",
    "lifeExp": "기대수명 (년)",
    "pop": "인구 (명)",
    "continent": "대륙",
    "year": "연도",
    "country": "국가",
}

# 연도가 시간 순서로 재생되도록 정렬
df_animation = df.sort_values(["year", "country"])

fig_animation = px.scatter(
    df_animation,
    x="gdpPercap",
    y="lifeExp",
    color="continent",          # 대륙마다 다른 색
    size="pop",                 # 인구를 점의 크기로 표현
    hover_name="country",       # 마우스를 올리면 국가명 표시
    hover_data=["year", "pop"],
    log_x=True,
    size_max=50,
    labels=labels,
    animation_frame="year",     # 연도별 장면 만들기
    animation_group="country",  # 장면이 바뀌어도 같은 국가의 점으로 식별
    range_x=[100, 150000],       # 모든 연도에 동일한 x축 범위 적용
    range_y=[20, 90],            # 모든 연도에 동일한 y축 범위 적용
    render_mode="svg",          # 점이 부드럽게 이동하도록 SVG로 표시
    height=650,
    title="국가별 GDP와 기대수명 변화: 1952~2007",
)

# Streamlit 웹페이지 안에 그래프 표시
st.plotly_chart(
    fig_animation,
    width="stretch",
    theme=None,
)

st.caption(
    "x축은 밑이 10인 로그 눈금이며, 눈금 숫자는 원래 GDP 값입니다. "
    "점의 색은 대륙, 크기는 인구를 나타냅니다."
)
