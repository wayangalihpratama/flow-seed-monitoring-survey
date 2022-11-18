import os
import time
from datetime import timedelta
from db import crud_question
from db import crud_data
from db.connection import Base, SessionLocal, engine
from db.truncator import truncate
from db import crud_answer
from models.question import QuestionType
from models.answer import Answer
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
        form_id=form_id, page_size=300)
    if not data:
        print(f"{form_id}: seed ERROR!")
        break
    formInstances = data.get('formInstances')
    nextPageUrl = data.get('nextPageUrl')
    for fi in formInstances:
        answers = []
        geoVal = None
        # fetching answers value into answer model
        for key, value in fi.get('responses').items():
            for val in value:
                for kval, aval in val.items():
                    question = crud_question.get_question_by_id(
                        session=session, id=kval)
                    if not question:
                        print(f"{kval}: 404 not found")
                        continue
                    if question.type == QuestionType.geo:
                        geoVal = [aval.get('lat'), aval.get('long')]
                    answer = Answer(
                        data=fi.get('id'),
                        question=question.id,
                        created=fi.get('createdAt'))
                    answer = crud_answer.append_value(
                        answer=answer, value=aval, type=question.type)
                    answers.append(answer)
        data = crud_data.add_data(
            session=session,
            id=fi.get('id'),
            name=fi.get('displayName'),
            form=form_id,
            geo=geoVal,
            created=fi.get('createdAt'),
            answers=answers)
        print(f"Datapoint: {data.id}")
    print(f"{form_id}: seed complete")
    print("------------------------------------------")

elapsed_time = time.process_time() - start_time
elapsed_time = str(timedelta(seconds=elapsed_time)).split(".")[0]
print(f"\n-- DONE IN {elapsed_time}\n")
