import pickle
import streamlit as st
import pandas as pd
import numpy as np
import shap
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Rectangle
import plotly.graph_objects as go
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="EAFITure", page_icon="🎓", layout="wide")

# Configurar estilo dos gráficos
sns.set_style("whitegrid")
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']

# Dicionário de traduções
TRANSLATIONS = {
    'pt': {
        'title': 'Sistema de Predição de Desempenho Estudantil',
        'select_week': '📅 Selecione a semana',
        'input_method': 'Escolha o método de entrada de dados:',
        'form_method': 'Formulário Interativo',
        'csv_method': 'Upload de CSV',
        'student_data': 'Preencha os dados do estudante',
        'basic_info': '**Informações Básicas**',
        'group': 'Grupo',
        'gender': 'Gênero',
        'male': 'Masculino',
        'female': 'Feminino',
        'stem_course': 'Curso STEM?',
        'yes': 'Sim',
        'no': 'Não',
        'period': 'Período',
        'age_minor': 'Idade menor que 18? 0 (maior de 18) ou 1 (menor de 18)',
        'partials_projects': '**Parciais e Projetos**',
        'partial': 'Parcial',
        'project_part': 'Projeto Parte',
        'quizzes': '**Quizzes**',
        'quiz': 'Quiz',
        'time': 'Tempo',
        'minutes': 'min',
        'make_prediction': 'Fazer Predição',
        'prediction_result': 'Resultado da Predição',
        'high_risk': '⚠️ Alto Risco de Reprovação',
        'low_risk': '✅ Baixo Risco de Reprovação',
        'reproval_prob': 'Probabilidade de Reprovação',
        'approval_prob': 'Probabilidade de Aprovação',
        'view_processed': 'Dados Processados',
        'shap_analysis': 'Análise de Importância das Features',
        'shap_explanation': 'Entenda quais fatores mais influenciaram esta predição:',
        'shap_red': '🔴 Vermelho = aumenta o risco de reprovação',
        'shap_blue': '🔵 Azul = diminui o risco de reprovação',
        'shap_waterfall': 'Contribuição Individual das Features',
        'shap_force': 'Distribuição de Impacto',
        'feature_importance': 'Top Features mais Importantes',
        'performance_overview': 'Visão Geral do Desempenho',
        'risk_gauge': 'Medidor de Risco',
        'csv_upload': 'Upload de arquivo CSV',
        'csv_format': '**Formato esperado do CSV para {week}:**',
        'csv_instructions': 'O arquivo deve conter as seguintes colunas (use estes nomes exatos):',
        'required_fields': '**Campos Obrigatórios:**',
        'group_desc': '**Grupo**: Número do grupo (ex: 1, 2, 3...)',
        'gender_desc': '**Genero**: "Masculino" ou "Feminino"',
        'stem_desc': '**STEM**: "Sim" ou "Não" (indica se é curso STEM)',
        'age_desc': '**Edad_Menor**: 0 (maior de 18) ou 1 (menor de 18)',
        'evaluations_needed': '**Avaliações Necessárias para esta semana:**',
        'partials_grades': 'Parciais',
        'projects_grades': 'Projetos',
        'quizzes_grades': 'Quizzes',
        'quiz_times': 'Tempos de Quiz',
        'grades_range': 'notas de 0.0 a 5.0',
        'time_range': 'tempo em minutos, 0 a 120',
        'no_partial': 'Nenhum parcial necessário ainda',
        'no_project': 'Nenhum projeto necessário ainda',
        'no_quiz': 'Nenhum quiz necessário ainda',
        'download_template': '⬇️ Baixar template CSV para {week}',
        'upload_csv': 'Faça upload do arquivo CSV',
        'preview_data': 'Preview dos dados carregados:',
        'process_predictions': 'Processar e Fazer Predições',
        'predictions_complete': '✅ Predições concluídas!',
        'total_at_risk': 'Total de Alunos em Risco',
        'percent_at_risk': 'Percentual em Risco',
        'download_results': '⬇️ Baixar resultados',
        'prediction_column': 'Predicao',
        'prediction_text': 'Predicao_Texto',
        'approved': 'Aprovado',
        'failed': 'Reprovado',
        'reproval_prob_column': 'Probabilidade_Reprovacao_%',
        'error_processing': '❌ Erro ao processar arquivo:',
        'error_prediction': '❌ Erro ao fazer predição:',
        'no_models': '❌ Nenhum modelo foi carregado. Verifique se os arquivos .pkl estão no diretório "models/".',
        'model_error': '❌ Não foi possível extrair as features do modelo.',
        'tip': '**Dica**: Baixe o template abaixo com exatamente as colunas necessárias!',
        'footer': 'EAFITure - Sistema de Predição de Desempenho Estudantil',
        'language': '🌐 Idioma',
        'top_features': 'Features mais Importantes',
        'shap_value': 'Valor SHAP',
        'feature_value': 'Valor',
        'impact': 'Impacto',
        'positive_impact': 'Impacto Positivo (reduz risco)',
        'negative_impact': 'Impacto Negativo (aumenta risco)',
        'recommendation': 'Recomendações',
        'risk_factors': '⚠️ Principais Fatores de Risco',
        'protective_factors': '✅ Fatores Protetivos',
        'action_items': 'Ações Recomendadas',
        'student_profile': 'Perfil do Estudante',
        'batch_results': 'Resultados em Lote',
        'risk_distribution': 'Distribuição de Risco',
        'class_overview': 'Visão Geral da Turma',
        'high_risk_students': 'Estudantes em Alto Risco',
        'medium_risk_students': 'Estudantes em Risco Médio',
        'low_risk_students': 'Estudantes em Baixo Risco',
        'average_performance': 'Desempenho Médio',
        'risk_by_group': 'Distribuição de Risco por Grupo',
        'performance_metrics': 'Métricas de Desempenho'
    },
    'es': {
        'title': 'Sistema de Predicción de Rendimiento Estudiantil',
        'select_week': '📅 Seleccione la semana',
        'input_method': 'Elija el método de entrada de datos:',
        'form_method': 'Formulario Interactivo',
        'csv_method': 'Carga de CSV',
        'student_data': 'Complete los datos del estudiante',
        'basic_info': '**Información Básica**',
        'group': 'Grupo',
        'gender': 'Género',
        'male': 'Masculino',
        'female': 'Femenino',
        'stem_course': '¿Carrera STEM?',
        'yes': 'Sí',
        'no': 'No',
        'period': 'Período',
        'age_minor': '¿Edad menor de 18? 0 (mayor de 18) o 1 (menor de 18)',
        'partials_projects': '**Parciales y Proyectos**',
        'partial': 'Parcial',
        'project_part': 'Proyecto Parte',
        'quizzes': '**Quizzes**',
        'quiz': 'Quiz',
        'time': 'Tiempo',
        'minutes': 'min',
        'make_prediction': 'Hacer Predicción',
        'prediction_result': 'Resultado de la Predicción',
        'high_risk': '⚠️ Alto Riesgo de Reprobación',
        'low_risk': '✅ Bajo Riesgo de Reprobación',
        'reproval_prob': 'Probabilidad de Reprobación',
        'approval_prob': 'Probabilidad de Aprobación',
        'view_processed': 'Datos Procesados',
        'shap_analysis': 'Análisis de Importancia de Características',
        'shap_explanation': 'Comprenda qué factores influyeron más en esta predicción:',
        'shap_red': '🔴 Rojo = aumenta el riesgo de reprobación',
        'shap_blue': '🔵 Azul = disminuye el riesgo de reprobación',
        'shap_waterfall': 'Contribución Individual de Características',
        'shap_force': 'Distribución de Impacto',
        'feature_importance': 'Top Características más Importantes',
        'performance_overview': 'Visión General del Rendimiento',
        'risk_gauge': 'Medidor de Riesgo',
        'csv_upload': 'Carga de archivo CSV',
        'csv_format': '**Formato esperado del CSV para {week}:**',
        'csv_instructions': 'El archivo debe contener las siguientes columnas (use estos nombres exactos):',
        'required_fields': '**Campos Obligatorios:**',
        'group_desc': '**Grupo**: Número del grupo (ej: 1, 2, 3...)',
        'gender_desc': '**Genero**: "Masculino" o "Femenino"',
        'stem_desc': '**STEM**: "Sí" o "No" (indica si es carrera STEM)',
        'age_desc': '**Edad_Menor**: 0 (mayor de 18) o 1 (menor de 18)',
        'evaluations_needed': '**Evaluaciones Necesarias para esta semana:**',
        'partials_grades': 'Parciales',
        'projects_grades': 'Proyectos',
        'quizzes_grades': 'Quizzes',
        'quiz_times': 'Tiempos de Quiz',
        'grades_range': 'notas de 0.0 a 5.0',
        'time_range': 'tiempo en minutos, 0 a 120',
        'no_partial': 'Ningún parcial necesario aún',
        'no_project': 'Ningún proyecto necesario aún',
        'no_quiz': 'Ningún quiz necesario aún',
        'download_template': '⬇️ Descargar plantilla CSV para {week}',
        'upload_csv': 'Suba el archivo CSV',
        'preview_data': 'Vista previa de los datos cargados:',
        'process_predictions': 'Procesar y Hacer Predicciones',
        'predictions_complete': '✅ ¡Predicciones completadas!',
        'total_at_risk': 'Total de Estudiantes en Riesgo',
        'percent_at_risk': 'Porcentaje en Riesgo',
        'download_results': '⬇️ Descargar resultados',
        'prediction_column': 'Prediccion',
        'prediction_text': 'Prediccion_Texto',
        'approved': 'Aprobado',
        'failed': 'Reprobado',
        'reproval_prob_column': 'Probabilidad_Reprobacion_%',
        'error_processing': '❌ Error al procesar archivo:',
        'error_prediction': '❌ Error al hacer predicción:',
        'no_models': '❌ No se cargó ningún modelo. Verifique que los archivos .pkl estén en el directorio "models/".',
        'model_error': '❌ No fue posible extraer las características del modelo.',
        'tip': '**💡 Consejo**: ¡Descargue la plantilla a continuación con exactamente las columnas necesarias!',
        'footer': 'EAFITure - Sistema de Predicción de Rendimiento Estudiantil',
        'language': '🌐 Idioma',
        'top_features': 'Características más Importantes',
        'shap_value': 'Valor SHAP',
        'feature_value': 'Valor',
        'impact': 'Impacto',
        'positive_impact': 'Impacto Positivo (reduce riesgo)',
        'negative_impact': 'Impacto Negativo (aumenta riesgo)',
        'recommendation': '💡 Recomendaciones',
        'risk_factors': '⚠️ Principales Factores de Riesgo',
        'protective_factors': '✅ Factores Protectores',
        'action_items': '📋 Acciones Recomendadas',
        'student_profile': '👤 Perfil del Estudiante',
        'batch_results': 'Resultados en Lote',
        'risk_distribution': '📈 Distribución de Riesgo',
        'class_overview': 'Visión General de la Clase',
        'high_risk_students': 'Estudiantes en Alto Riesgo',
        'medium_risk_students': 'Estudiantes en Riesgo Medio',
        'low_risk_students': 'Estudiantes en Bajo Riesgo',
        'average_performance': 'Rendimiento Promedio',
        'risk_by_group': 'Distribución de Riesgo por Grupo',
        'performance_metrics': 'Métricas de Rendimiento'
    }
}

def t(key, lang='pt', **kwargs):
    text = TRANSLATIONS.get(lang, TRANSLATIONS['pt']).get(key, key)
    if kwargs:
        return text.format(**kwargs)
    return text

if 'language' not in st.session_state:
    st.session_state.language = 'pt'

@st.cache_resource
def load_models():
    models = {}
    weeks = ['week4', 'week8', 'week12', 'week15']
    
    for week in weeks:
        try:
            with open(f"models/model_{week}.pkl", "rb") as f:
                models[week] = pickle.load(f)
        except FileNotFoundError:
            st.warning(f"⚠️ Model file for {week} not found.")
    
    return models

@st.cache_resource
def create_shap_explainer(_model):
    try:
        explainer = shap.TreeExplainer(_model)
        return explainer
    except:
        try:
            explainer = shap.LinearExplainer(_model, masker=shap.maskers.Independent(data=np.zeros((1, len(_model.feature_names_in_)))))
            return explainer
        except:
            return None

def create_risk_gauge(probability, lang='pt'):
    """Cria um gráfico gauge para mostrar o nível de risco"""
    
    # Determinar cor baseada no risco
    if probability >= 70:
        color = "#d32f2f"  # Vermelho
        risk_level = "ALTO"
    elif probability >= 40:
        color = "#f57c00"  # Laranja
        risk_level = "MÉDIO" if lang == 'pt' else "MEDIO"
    else:
        color = "#388e3c"  # Verde
        risk_level = "BAIXO"
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = probability,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"Risco: {risk_level}", 'font': {'size': 24, 'color': color}},
        number = {'suffix': "%", 'font': {'size': 40}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkgray"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 40], 'color': '#c8e6c9'},
                {'range': [40, 70], 'color': '#fff3e0'},
                {'range': [70, 100], 'color': '#ffcdd2'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        font={'size': 12}
    )
    
    return fig

def create_probability_bars(prob_reproval, lang='pt'):
    """Cria barras horizontais mostrando probabilidades"""
    
    prob_approval = 100 - prob_reproval
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=[t('approval_prob', lang)],
        x=[prob_approval],
        orientation='h',
        marker=dict(color='#4caf50'),
        text=f'{prob_approval:.1f}%',
        textposition='inside',
        name=t('approved', lang)
    ))
    
    fig.add_trace(go.Bar(
        y=[t('reproval_prob', lang)],
        x=[prob_reproval],
        orientation='h',
        marker=dict(color='#f44336'),
        text=f'{prob_reproval:.1f}%',
        textposition='inside',
        name=t('failed', lang)
    ))
    
    fig.update_layout(
        title=t('prediction_result', lang),
        xaxis=dict(title='Probabilidade (%)', range=[0, 100]),
        height=200,
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

def plot_feature_impact_chart(shap_df, lang='pt'):
    """Cria gráfico de impacto das features com Plotly"""
    
    # Pegar top 10 features
    top_features = shap_df.nlargest(10, 'Impacto Absoluto')
    
    # Definir cores baseadas no sinal
    colors = ['#f44336' if x > 0 else '#4caf50' for x in top_features[t('shap_value', lang)]]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=top_features['Feature'],
        x=top_features[t('shap_value', lang)],
        orientation='h',
        marker=dict(color=colors),
        text=top_features[t('shap_value', lang)].apply(lambda x: f'{x:.3f}'),
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>' +
                     f'{t("shap_value", lang)}: %{{x:.4f}}<br>' +
                     '<extra></extra>'
    ))
    
    fig.update_layout(
        title=t('top_features', lang),
        xaxis_title=t('shap_value', lang),
        yaxis_title='',
        height=400,
        margin=dict(l=150, r=20, t=50, b=50),
        yaxis={'categoryorder':'total ascending'}
    )
    
    # Adicionar linha vertical no zero
    fig.add_vline(x=0, line_dash="dash", line_color="gray")
    
    return fig

def plot_student_profile(model_input, lang='pt'):
    """Cria um gráfico radar do perfil do estudante"""
    
    # Selecionar features relevantes para o radar
    relevant_features = []
    values = []
    
    for col in model_input.columns:
        if any(x in col for x in ['Quiz', 'Parcial', 'Proyecto']):
            if 'Tiempo' not in col:
                relevant_features.append(col)
                values.append(model_input[col].values[0])
    
    if len(relevant_features) == 0:
        return None
    
    # Limitar a 8 features para melhor visualização
    if len(relevant_features) > 8:
        relevant_features = relevant_features[:8]
        values = values[:8]
    
    # Normalizar valores para 0-100
    normalized_values = [(v / 5.0) * 100 for v in values]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=normalized_values + [normalized_values[0]],
        theta=relevant_features + [relevant_features[0]],
        fill='toself',
        fillcolor='rgba(63, 81, 181, 0.3)',
        line=dict(color='#3f51b5', width=2),
        name=t('student_profile', lang)
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                ticksuffix='%'
            )
        ),
        showlegend=False,
        title=t('performance_overview', lang),
        height=400
    )
    
    return fig

def create_batch_visualizations(data, predictions, probabilities_list, lang='pt'):
    """Cria visualizações para análise em lote"""
    
    # Adicionar predições ao dataframe
    data_viz = data.copy()
    data_viz[t('prediction_column', lang)] = predictions
    data_viz[t('reproval_prob_column', lang)] = probabilities_list
    
    # 1. Distribuição de Risco
    risk_categories = []
    for prob in probabilities_list:
        if prob >= 70:
            risk_categories.append(t('high_risk_students', lang))
        elif prob >= 40:
            risk_categories.append(t('medium_risk_students', lang))
        else:
            risk_categories.append(t('low_risk_students', lang))
    
    data_viz['Categoria_Risco'] = risk_categories
    
    # Gráfico de pizza - Distribuição de risco
    risk_counts = pd.Series(risk_categories).value_counts()
    
    fig_pie = go.Figure(data=[go.Pie(
        labels=risk_counts.index,
        values=risk_counts.values,
        hole=.4,
        marker=dict(colors=['#388e3c', '#f57c00','#d32f2f' ]),
        textinfo='label+percent',
        textposition='outside'
    )])
    
    fig_pie.update_layout(
        title=t('risk_distribution', lang),
        height=400,
        showlegend=True
    )
    
    # 2. Histograma de probabilidades
    fig_hist = go.Figure()
    
    fig_hist.add_trace(go.Histogram(
        x=probabilities_list,
        nbinsx=20,
        marker=dict(
            color=probabilities_list,
            colorscale='RdYlGn_r',
            showscale=True,
            colorbar=dict(title="Prob. (%)")
        ),
        hovertemplate='Probabilidade: %{x:.1f}%<br>Frequência: %{y}<extra></extra>'
    ))
    
    fig_hist.update_layout(
        title='Distribuição de Probabilidades de Reprovação',
        xaxis_title='Probabilidade de Reprovação (%)',
        yaxis_title='Número de Estudantes',
        height=400
    )
    
    # 3. Box plot por grupo (se houver coluna Grupo)
    fig_box = None
    if 'Grupo' in data_viz.columns:
        fig_box = go.Figure()
        
        for grupo in sorted(data_viz['Grupo'].unique()):
            grupo_data = data_viz[data_viz['Grupo'] == grupo]
            fig_box.add_trace(go.Box(
                y=grupo_data[t('reproval_prob_column', lang)],
                name=f'Grupo {grupo}',
                boxmean='sd'
            ))
        
        fig_box.update_layout(
            title=t('risk_by_group', lang),
            yaxis_title='Probabilidade de Reprovação (%)',
            height=400,
            showlegend=True
        )
    
    # 4. Tabela de estatísticas
    stats_data = {
        'Métrica': [
            'Total de Estudantes',
            'Alto Risco (≥70%)',
            'Risco Médio (40-70%)',
            'Baixo Risco (<40%)',
            'Probabilidade Média',
            'Probabilidade Mediana'
        ],
        'Valor': [
            len(data_viz),
            len([p for p in probabilities_list if p >= 70]),
            len([p for p in probabilities_list if 40 <= p < 70]),
            len([p for p in probabilities_list if p < 40]),
            f"{np.mean(probabilities_list):.1f}%",
            f"{np.median(probabilities_list):.1f}%"
        ]
    }
    
    stats_df = pd.DataFrame(stats_data)
    
    return fig_pie, fig_hist, fig_box, stats_df, data_viz

def plot_shap_analysis(explainer, model_input, lang='pt'):
    """Gera visualizações SHAP para a predição"""
    
    shap_values = explainer(model_input)
    
    is_multioutput = hasattr(shap_values, 'shape') and len(shap_values.shape) == 3
    
    if is_multioutput:
        shap_values_class1 = shap_values[:, :, 1]
    else:
        shap_values_class1 = shap_values
    
    st.markdown(f"### {t('shap_analysis', lang)}")
    st.info(t('shap_explanation', lang))
    
    tab1, tab2, tab3 = st.tabs([
        t('shap_waterfall', lang), 
        t('feature_importance', lang),
        t('view_processed', lang)
    ])
    
    with tab1:
        st.markdown(f"#### {t('shap_waterfall', lang)}")
        fig, ax = plt.subplots(figsize=(10, 6))
        
        try:
            shap.plots.waterfall(shap_values_class1[0], max_display=15, show=False)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Erro no waterfall plot: {e}")
        finally:
            plt.close()
    
    with tab2:
        st.markdown(f"#### {t('top_features', lang)}")
        
        # Extrair valores SHAP corretamente
        try:
            if hasattr(shap_values_class1, 'values'):
                shap_vals = shap_values_class1.values[0]
            else:
                shap_vals = shap_values_class1[0]
            
            if not isinstance(shap_vals, np.ndarray):
                shap_vals = np.array(shap_vals)
                
        except Exception as e:
            st.error(f"Erro ao extrair valores SHAP: {e}")
            shap_vals = np.zeros(len(model_input.columns))
        
        feature_vals = model_input.values[0]
        feature_names = model_input.columns.tolist()
        
        shap_df = pd.DataFrame({
            'Feature': feature_names,
            t('feature_value', lang): feature_vals,
            t('shap_value', lang): shap_vals,
            'Impacto Absoluto': np.abs(shap_vals)
        })
        shap_df = shap_df.sort_values('Impacto Absoluto', ascending=False)
        shap_df = shap_df[shap_df['Impacto Absoluto'] > 0.001]
        
        # Plotly bar chart
        fig_bar = plot_feature_impact_chart(shap_df, lang)
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # Tabela detalhada
        st.markdown("---")
        st.dataframe(
            shap_df.style.format({
                t('feature_value', lang): '{:.2f}',
                t('shap_value', lang): '{:.4f}',
                'Impacto Absoluto': '{:.4f}'
            }).background_gradient(subset=[t('shap_value', lang)], cmap='RdYlGn_r'),
            use_container_width=True
        )
    
    with tab3:
        st.dataframe(model_input)

def prepare_user_data(user_input, week, lang='pt'):
    processed_data = {}
    
    numeric_fields = {
        'Grupo': 'Grupo',
        'Parcial_1': 'Parcial_1',
        'Quiz1': 'Quiz1',
        'TiempoQ1': 'TiempoQ1',
        'Quiz2': 'Quiz2',
        'TiempoQ2': 'TiempoQ2',
        'Quiz3': 'Quiz3',
        'TiempoQ3': 'TiempoQ3',
        'Quiz4': 'Quiz4',
        'TiempoQ4': 'TiempoQ4',
        'Quiz5': 'Quiz5',
        'TiempoQ5': 'TiempoQ5',
        'Quiz6': 'Quiz6',
        'TiempoQ6': 'TiempoQ6',
        'Quiz7': 'Quiz7',
        'TiempoQ7': 'TiempoQ7',
        'Projeto_Parte1': 'Proyecto_Parte1',
        'Edad_Menor': 'Edad_Menor'
    }
    
    for key, model_key in numeric_fields.items():
        if key in user_input:
            processed_data[model_key] = user_input[key]
    
    genero = user_input.get('Genero', 'Masculino')
    if genero in ['Masculino', 'Femenino']:
        processed_data['Genero_femenino'] = 1 if genero == 'Femenino' else 0
        processed_data['Genero_masculino'] = 1 if genero == 'Masculino' else 0
    else:
        processed_data['Genero_femenino'] = 1 if genero == 'Feminino' else 0
        processed_data['Genero_masculino'] = 1 if genero == 'Masculino' else 0
    
    stem = user_input.get('STEM', 'Não')
    if stem in ['Sim', 'Sí']:
        processed_data['STEM_SI'] = 1
    else:
        processed_data['STEM_SI'] = 0
    
    
    return processed_data

def create_model_input(processed_data, required_features):
    model_input = {feature: 0 for feature in required_features}
    model_input.update(processed_data)
    df = pd.DataFrame([model_input])
    df = df[required_features]
    return df

col_lang, col_empty = st.columns([1, 5])
with col_lang:
    language = st.selectbox(
        "🌐",
        options=['pt', 'es'],
        format_func=lambda x: 'Português 🇧🇷' if x == 'pt' else 'Español 🇪🇸',
        key='lang_selector',
        label_visibility='collapsed'
    )
    st.session_state.language = language

lang = st.session_state.language

st.text("")
st.image("assets/logo.png", width=200)
st.subheader(t('title', lang))
st.markdown("---")

models = load_models()

if not models:
    st.error(t('no_models', lang))
    st.stop()

col1, col2 = st.columns([1, 3])
weeks = ["Semana 4", "Semana 8", "Semana 12", "Semana 15"]
with col1:
    week = st.selectbox(t('select_week', lang), options=list(weeks))

# Mapeia a semana selecionada para o modelo correspondente
if week == 'Semana 4':
    week = 'week4'
elif week == 'Semana 8':
    week = 'week8'
elif week == 'Semana 12':
    week = 'week12'
elif week == 'Semana 15':
    week = 'week15'

model = models[week]

try:
    required_features = list(model.feature_names_in_)
except AttributeError:
    st.error(t('model_error', lang))
    st.stop()

st.markdown("---")

input_method = st.radio(
    t('input_method', lang),
    [t('form_method', lang), t('csv_method', lang)]
)

if input_method == t('form_method', lang):
    st.subheader(t('student_data', lang))
    
    col1, col2, col3 = st.columns(3)
    
    user_input = {}
    
    with col1:
        st.markdown(t('basic_info', lang))
        user_input['Grupo'] = st.number_input(t('group', lang), min_value=1, max_value=10, value=1)
        
        if lang == 'pt':
            user_input['Genero'] = st.selectbox(t('gender', lang), [t('male', lang), t('female', lang)])
            user_input['STEM'] = st.selectbox(t('stem_course', lang), [t('yes', lang), t('no', lang)])
        else:
            user_input['Genero'] = st.selectbox(t('gender', lang), ["Masculino", "Femenino"])
            user_input['STEM'] = st.selectbox(t('stem_course', lang), ["Sí", "No"])
        
        user_input['Edad_Menor'] = st.selectbox(t('age_minor', lang), [0, 1])
    
    with col2:
        st.markdown(t('partials_projects', lang))
        if 'Parcial_1' in required_features:
            user_input['Parcial_1'] = st.number_input(f"{t('partial', lang)} 1", min_value=0.0, max_value=5.0, value=0.0, step=0.1)
        if 'Proyecto_Parte1' in required_features:
            user_input['Projeto_Parte1'] = st.number_input(f"{t('project_part', lang)} 1", min_value=0.0, max_value=5.0, value=0.0, step=0.1)
    
    with col3:
        st.markdown(t('quizzes', lang))
        quiz_map = {
            'week4': ['Quiz1'],
            'week8': ['Quiz1', 'Quiz2', 'Quiz3'],
            'week12': ['Quiz1', 'Quiz2', 'Quiz3', 'Quiz4', 'Quiz5'],
            'week15': ['Quiz1', 'Quiz2', 'Quiz3', 'Quiz4', 'Quiz5', 'Quiz6', 'Quiz7']
        }
        
        quizzes_needed = quiz_map.get(week, [])
        for quiz in quizzes_needed:
            if quiz in required_features:
                user_input[quiz] = st.number_input(f"{t('quiz', lang)} {quiz[4:]}", min_value=0.0, max_value=5.0, value=0.0, step=0.1)
                if f'TiempoQ{quiz[4:]}' in required_features:
                    user_input[f'TiempoQ{quiz[4:]}'] = st.number_input(
                        f"{t('time', lang)} {t('quiz', lang)} {quiz[4:]} ({t('minutes', lang)})", 
                        min_value=0, 
                        max_value=120, 
                        value=0
                    )
    
    st.markdown("---")
    
    if st.button(t('make_prediction', lang), type="primary", use_container_width=True):
        processed_data = prepare_user_data(user_input, week, lang)
        model_input = create_model_input(processed_data, required_features)
        
        try:
            prediction = model.predict(model_input)[0]
            
            try:
                probabilities = model.predict_proba(model_input)[0]
                prob_reprovacao = probabilities[1] * 100
            except:
                prob_reprovacao = None
            
            st.markdown("---")
            st.subheader(t('prediction_result', lang))
            
            # Dashboard principal
            col1, col2 = st.columns([1, 2])
            
            with col1:
                if prob_reprovacao is not None:
                    fig_gauge = create_risk_gauge(prob_reprovacao, lang)
                    st.plotly_chart(fig_gauge, use_container_width=True)
            
            with col2:
                if prob_reprovacao is not None:
                    fig_bars = create_probability_bars(prob_reprovacao, lang)
                    st.plotly_chart(fig_bars, use_container_width=True)
                
                if prediction == 1:
                    st.error(f"### {t('high_risk', lang)}")
                else:
                    st.success(f"### {t('low_risk', lang)}")
            
            # Perfil do estudante
            st.markdown("---")
            fig_radar = plot_student_profile(model_input, lang)
            if fig_radar:
                st.plotly_chart(fig_radar, use_container_width=True)
            
            # Análise SHAP
            st.markdown("---")
            explainer = create_shap_explainer(model)
            
            if explainer:
                plot_shap_analysis(explainer, model_input, lang)
                
            else:
                with st.expander(t('view_processed', lang)):
                    st.dataframe(model_input)
                
        except Exception as e:
            st.error(f"{t('error_prediction', lang)} {e}")
            import traceback
            st.code(traceback.format_exc())

else:  # CSV Upload
    st.subheader(t('csv_upload', lang))
    
    def get_user_fields_for_week(required_features):
        user_fields = {
            'obrigatorios': ['Grupo', 'Genero', 'STEM', 'Edad_Menor'],
            'parciais': [],
            'projetos': [],
            'quizzes': [],
            'tempos': []
        }
        
        for i in range(1, 5):
            if f'Parcial_{i}' in required_features:
                user_fields['parciais'].append(f'Parcial_{i}')
        
        if 'Proyecto_Parte1' in required_features:
            user_fields['projetos'].append('Projeto_Parte1')
        
        for i in range(1, 10):
            if f'Quiz{i}' in required_features:
                user_fields['quizzes'].append(f'Quiz{i}')
            if f'TiempoQ{i}' in required_features:
                user_fields['tempos'].append(f'TiempoQ{i}')
        
        return user_fields
    
    user_fields = get_user_fields_for_week(required_features)
    
    partials_text = f"- **{t('partials_grades', lang)}**: {', '.join(user_fields['parciais'])} ({t('grades_range', lang)})" if user_fields['parciais'] else f"- {t('no_partial', lang)}"
    projects_text = f"- **{t('projects_grades', lang)}**: {', '.join(user_fields['projetos'])} ({t('grades_range', lang)})" if user_fields['projetos'] else f"- {t('no_project', lang)}"
    quizzes_text = f"- **{t('quizzes_grades', lang)}**: {', '.join(user_fields['quizzes'])} ({t('grades_range', lang)})" if user_fields['quizzes'] else f"- {t('no_quiz', lang)}"
    times_text = f"- **{t('quiz_times', lang)}**: {', '.join(user_fields['tempos'])} ({t('time_range', lang)})" if user_fields['tempos'] else ""
    
    st.info(f"""
    {t('csv_format', lang, week=week.upper())}
    
    {t('csv_instructions', lang)}
    
    {t('required_fields', lang)}
    - {t('group_desc', lang)}
    - {t('gender_desc', lang)}
    - {t('stem_desc', lang)}
    - {t('age_desc', lang)}
    
    {t('evaluations_needed', lang)}
    {partials_text}
    {projects_text}
    {quizzes_text}
    {times_text}
    
    {t('tip', lang)}
    """)
    
    def create_template_for_week(user_fields, lang):
        if lang == 'pt':
            template_data = {
                'Grupo': [1],
                'Genero': ['Masculino'],
                'STEM': ['Sim'],
                'Edad_Menor': [0]
            }
        else:
            template_data = {
                'Grupo': [1],
                'Genero': ['Masculino'],
                'STEM': ['Sí'],
                'Edad_Menor': [0]
            }
        
        for parcial in user_fields['parciais']:
            template_data[parcial] = [0.0]
        for projeto in user_fields['projetos']:
            template_data[projeto] = [0.0]
        for quiz in user_fields['quizzes']:
            template_data[quiz] = [0.0]
        for tempo in user_fields['tempos']:
            template_data[tempo] = [0]
        
        return pd.DataFrame(template_data)
    
    template_df = create_template_for_week(user_fields, lang)
    csv_template = template_df.to_csv(index=False)
    
    st.download_button(
        label=t('download_template', lang, week=week.upper()),
        data=csv_template,
        file_name=f"template_predicao_{week}.csv",
        mime="text/csv"
    )
    
    uploaded_file = st.file_uploader(t('upload_csv', lang), type=["csv"])
    
    if uploaded_file is not None:
        try:
            data = pd.read_csv(uploaded_file)
            
            st.write(t('preview_data', lang))
            st.dataframe(data.head())
            
            if st.button(t('process_predictions', lang), type="primary"):
                predictions = []
                probabilities_list = []
                
                progress_bar = st.progress(0)
                for idx, row in data.iterrows():
                    user_input = row.to_dict()
                    processed_data = prepare_user_data(user_input, week, lang)
                    model_input = create_model_input(processed_data, required_features)
                    
                    pred = model.predict(model_input)[0]
                    predictions.append(pred)
                    
                    try:
                        probs = model.predict_proba(model_input)[0]
                        probabilities_list.append(probs[1] * 100)
                    except:
                        probabilities_list.append(None)
                    
                    progress_bar.progress((idx + 1) / len(data))
                
                progress_bar.empty()
                
                # Criar visualizações
                fig_pie, fig_hist, fig_box, stats_df, data_viz = create_batch_visualizations(
                    data, predictions, probabilities_list, lang
                )
                
                # Salvar no session_state
                st.session_state['predictions_done'] = True
                st.session_state['data_viz'] = data_viz
                st.session_state['fig_pie'] = fig_pie
                st.session_state['fig_hist'] = fig_hist
                st.session_state['fig_box'] = fig_box
                st.session_state['stats_df'] = stats_df
                st.session_state['predictions'] = predictions
                st.session_state['probabilities_list'] = probabilities_list
            
            # Mostrar resultados se já foram processados
            if st.session_state.get('predictions_done', False):
                data_viz = st.session_state['data_viz']
                fig_pie = st.session_state['fig_pie']
                fig_hist = st.session_state['fig_hist']
                fig_box = st.session_state['fig_box']
                stats_df = st.session_state['stats_df']
                predictions = st.session_state['predictions']
                probabilities_list = st.session_state['probabilities_list']
                
                st.success(t('predictions_complete', lang))
                
                # Métricas principais
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    total_reprovados = sum(predictions)
                    st.metric(t('total_at_risk', lang), total_reprovados)
                with col2:
                    perc_risco = (total_reprovados / len(predictions)) * 100
                    st.metric(t('percent_at_risk', lang), f"{perc_risco:.1f}%")
                with col3:
                    st.metric(t('average_performance', lang), f"{np.mean(probabilities_list):.1f}%")
                with col4:
                    st.metric("Total de Estudantes", len(data))
                
                # Gráficos
                st.markdown("---")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.plotly_chart(fig_pie, use_container_width=True)
                
                with col2:
                    st.plotly_chart(fig_hist, use_container_width=True)
                
                if fig_box:
                    st.plotly_chart(fig_box, use_container_width=True)
                
                # Tabela de estatísticas
                st.markdown("---")
                st.subheader(t('performance_metrics', lang))
                st.dataframe(stats_df, use_container_width=True)
                
                # Dados completos com filtros
                st.markdown("---")
                st.subheader(t('batch_results', lang))
                
                # Filtros interativos
                st.markdown("#### 🔍 Filtros")
                filter_cols = st.columns(4)
                
                with filter_cols[0]:
                    # Filtro por categoria de risco
                    risk_options = ['Todos'] + sorted(data_viz['Categoria_Risco'].unique().tolist())
                    selected_risk = st.selectbox('Categoria de Risco', risk_options)
                
                with filter_cols[1]:
                    # Filtro por grupo
                    if 'Grupo' in data_viz.columns:
                        group_options = ['Todos'] + sorted(data_viz['Grupo'].unique().tolist())
                        selected_group = st.selectbox('Grupo', group_options)
                    else:
                        selected_group = 'Todos'
                
                with filter_cols[2]:
                    # Filtro por gênero
                    if 'Genero' in data_viz.columns:
                        gender_options = ['Todos'] + sorted(data_viz['Genero'].unique().tolist())
                        selected_gender = st.selectbox('Gênero', gender_options)
                    else:
                        selected_gender = 'Todos'
                
                with filter_cols[3]:
                    # Filtro por STEM
                    if 'STEM' in data_viz.columns:
                        stem_options = ['Todos'] + sorted(data_viz['STEM'].unique().tolist())
                        selected_stem = st.selectbox('STEM', stem_options)
                    else:
                        selected_stem = 'Todos'
                
                # Aplicar filtros
                filtered_data = data_viz.copy()
                
                if selected_risk != 'Todos':
                    filtered_data = filtered_data[filtered_data['Categoria_Risco'] == selected_risk]
                
                if selected_group != 'Todos':
                    filtered_data = filtered_data[filtered_data['Grupo'] == selected_group]
                
                if selected_gender != 'Todos':
                    filtered_data = filtered_data[filtered_data['Genero'] == selected_gender]
                
                if selected_stem != 'Todos':
                    filtered_data = filtered_data[filtered_data['STEM'] == selected_stem]
                
                # Mostrar contagem de resultados filtrados
                st.info(f"Mostrando {len(filtered_data)} de {len(data_viz)} estudantes")
                
                # Função para colorir a célula de risco
                def color_risk_category(val):
                    if t('high_risk_students', lang) in str(val):
                        return 'background-color: #ffcdd2; color: #b71c1c; font-weight: bold'
                    elif t('medium_risk_students', lang) in str(val):
                        return 'background-color: #fff3e0; color: #e65100; font-weight: bold'
                    elif t('low_risk_students', lang) in str(val):
                        return 'background-color: #c8e6c9; color: #2e7d32; font-weight: bold'
                    return ''
                
                # Função para colorir probabilidades
                def color_probability(val):
                    try:
                        prob = float(val)
                        if prob >= 70:
                            return 'background-color: #ffcdd2; color: #b71c1c; font-weight: bold'
                        elif prob >= 40:
                            return 'background-color: #fff3e0; color: #e65100'
                        else:
                            return 'background-color: #c8e6c9; color: #2e7d32'
                    except:
                        return ''
                
                
                prob_col_name = t('reproval_prob_column', lang)
                
                # Verificar se a coluna existe antes de aplicar estilo
                if prob_col_name in filtered_data.columns:
                    styled_df = filtered_data.style.applymap(
                        color_risk_category, 
                        subset=['Categoria_Risco']
                    ).applymap(
                        color_probability,
                        subset=[prob_col_name]
                    )
                else:
                    styled_df = filtered_data.style.applymap(
                        color_risk_category, 
                        subset=['Categoria_Risco']
                    )
                
                # Formatar colunas numéricas
                format_dict = {}
                for col in filtered_data.columns:
                    if filtered_data[col].dtype in ['float64', 'float32']:
                        if 'Probabilidade' in col or 'Prob' in col:
                            format_dict[col] = '{:.1f}'
                        else:
                            format_dict[col] = '{:.2f}'
                
                if format_dict:
                    styled_df = styled_df.format(format_dict)
                
                st.dataframe(styled_df, use_container_width=True, height=400)
                
                # Estatísticas dos dados filtrados
                if len(filtered_data) > 0:
                    st.markdown("---")
                    st.markdown("#### Estatísticas dos Dados Filtrados")
                    
                    stats_filtered_cols = st.columns(4)
                    with stats_filtered_cols[0]:
                        filtered_at_risk = len(filtered_data[filtered_data[t('prediction_column', lang)] == 1])
                        st.metric("Em Risco (Filtrado)", filtered_at_risk)
                    
                    with stats_filtered_cols[1]:
                        filtered_perc = (filtered_at_risk / len(filtered_data)) * 100 if len(filtered_data) > 0 else 0
                        st.metric("% em Risco (Filtrado)", f"{filtered_perc:.1f}%")
                    
                    with stats_filtered_cols[2]:
                        filtered_avg = filtered_data[t('reproval_prob_column', lang)].mean()
                        st.metric("Prob. Média (Filtrado)", f"{filtered_avg:.1f}%")
                    
                    with stats_filtered_cols[3]:
                        st.metric("Total (Filtrado)", len(filtered_data))
                
                # Download - sempre com dados completos
                st.markdown("---")
                csv_result = data_viz.to_csv(index=False)
                st.download_button(
                    label=t('download_results', lang),
                    data=csv_result,
                    file_name=f"predicoes_{week}.csv",
                    mime="text/csv"
                )
                
        except Exception as e:
            st.error(f"{t('error_processing', lang)} {e}")
            import traceback
            st.code(traceback.format_exc())

st.markdown("---")
st.caption(t('footer', lang))