import plotly.graph_objects as go

def category_bar_html(rows):
    fig = go.Figure(go.Bar(
        x=[row['name'] for row in rows],
        y=[row['count'] for row in rows],
    )
    )
    fig.update_layout(title="Обращения по категориям")
    return fig.to_html(full_html=False, include_plotlyjs='cdn')

def status_pie_html(rows):
    fig = go.Figure(go.Pie(
        labels=[row['status'] for row in rows],
        values=[row['count'] for row in rows],
    )
    )
    fig.update_layout(title="Обращения по статусам")
    return fig.to_html(full_html=False, include_plotlyjs='cdn')
