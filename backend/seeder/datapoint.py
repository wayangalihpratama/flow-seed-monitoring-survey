import os
import time
from datetime import timedelta
from db import crud_question_group
from db import crud_question
from db import crud_data
from db.connection import Base, SessionLocal, engine
from db.truncator import truncate
from models.question import QuestionType
import flow.auth as flow_auth

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Base.metadata.create_all(bind=engine)
session = SessionLocal()

start_time = time.process_time()
token = flow_auth.get_token()

for table in ["data", "answer", "history"]:
    action = truncate(session=session, table=table)
    print(action)

for form_id in [flow_auth.registraton_form, flow_auth.monitoring_form]:
    # fetch datapoint
    data = flow_auth.get_datapoint(
        token=token, survey_id=flow_auth.survey_id,
        form_id=form_id, page_size=100)
    formInstances = data.get('formInstances')
    nextPageUrl = data.get('nextPageUrl')
    # find geo question and get geo value
    qgeo = crud_question.get_question(
        session=session, form=form_id, type=QuestionType.geo.value)
    qgeo = qgeo[0] if len(qgeo) else None
    for fi in formInstances:
        # find geo question and get geo value
        responses = []
        for attr, value in fi.get('responses').items():
            responses.append(value)
        crud_data.add_data(
            session=session,
            id=fi.get('id'),
            name=fi.get('displayName'),
            form=form_id,
            created=fi.get('createdAt'),
            answers=[])
    print(f"{form_id}: seed complete")
