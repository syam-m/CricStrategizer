from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner': 'admin',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'CricStrategizer',
    default_args=default_args,
    description='Cricket Strategizer DAG',
    schedule_interval=None,
)

def run_data_extraction():
    from src.Data_Extraction import main
    main()

def run_data_cleaning():
    from src.Data_Cleaning import main
    main()

def run_feature_engineering():
    from src.Feature_Engineering import main
    main()

def run_eda():
    from src.EDA_Visuals import main
    main()

def run_model_creation():
    from src.Model_Creation import main
    main()

task_extraction = PythonOperator(
    task_id='data_extraction',
    python_callable=run_data_extraction,
    dag=dag,
)

task_cleaning = PythonOperator(
    task_id='data_cleaning',
    python_callable=run_data_cleaning,
    dag=dag,
)

task_engineering = PythonOperator(
    task_id='feature_engineering',
    python_callable=run_feature_engineering,
    dag=dag,
)

task_eda = PythonOperator(
    task_id='eda',
    python_callable=run_eda,
    dag=dag,
)

task_model_creation = PythonOperator(
    task_id='model_creation',
    python_callable=run_model_creation,
    dag=dag,
)

task_extraction >> task_cleaning >> task_engineering >> task_eda >> task_model_creation
