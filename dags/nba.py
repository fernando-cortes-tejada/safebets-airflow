import sys
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

sys.path.append("../../opt/airflow/")

from src.surebets import main as surebets

# This are the only lines that need to be changed to run the DAG for another category

# we declare the default arguments for the DAG
# this includes: which league, category, start date, schedule interval, etc.
websites = ["pinnacle"]
league = "nba"
# category = "triples"
# minute to initiate
initiate = 0
# minute interval to trigger again
interval = 3
# seconds to timeout
timeout = 120


# get the cron minutes
minutes = ",".join(
    [str(initiate + i * interval) for i in range(60) if initiate + i * interval < 60]
)

# declare the DAG
dag = DAG(
    f"{league}",
    start_date=datetime(2022, 10, 1),
    # run at the specified minutes and hours (UTC-5) where I am located
    # the hours are the hours I can bet
    schedule_interval=f"{minutes} 0,1,14,15,16,17,18,19,20,21,22,23 * * *",
    dagrun_timeout=timedelta(minutes=interval),
    catchup=False,
    tags=[league, "scrape", "surebets", "telegram", "selenium"],
)

# we declare the tasks (all of them are PythonOperators)
with dag:
    trigger_task = PythonOperator(
        task_id="trigger_task",
        python_callable=surebets.trigger,
        provide_context=True,
        op_kwargs={"league": league, "websites": websites},
    )

    # scrape pinnacle site
    pinnacle_scrape_task = PythonOperator(
        task_id="pinnacle_scrape_task",
        python_callable=surebets.scrape,
        provide_context=True,
        op_kwargs={"league": league, "website": "pinnacle", "max_time": timeout},
    )

    # scrape chuntala site
    # chuntala_scrape_task = PythonOperator(
    # task_id="chuntala_scrape_task",
    # python_callable=chuntala.scrape,
    # provide_context=True,
    # op_kwargs={"league": league, "category": category, "max_time": timeout},
    # )

    # scrape betano site
    # betano_scrape_task = PythonOperator(
    # task_id="betano_scrape_task",
    # python_callable=betano.scrape,
    # provide_context=True,
    # op_kwargs={"league": league, "category": category, "max_time": timeout},
    # )

    surebet_calc_task = PythonOperator(
        task_id="surebet_calc_task",
        python_callable=surebets.calculate,
        provide_context=True,
        trigger_rule="all_done",
        op_kwargs={"league": league, "websites": websites},
    )

    surebet_clean_task = PythonOperator(
        task_id="surebet_clean_task",
        python_callable=surebets.clean,
        provide_context=True,
        trigger_rule="all_done",
        op_kwargs={"league": league},
    )

    # trigger_task >> chuntala_scrape_task >> surebet_calc_task >> surebet_clean_task
    # trigger_task >> betano_scrape_task >> surebet_calc_task >> surebet_clean_task
    trigger_task >> pinnacle_scrape_task >> surebet_calc_task >> surebet_clean_task
