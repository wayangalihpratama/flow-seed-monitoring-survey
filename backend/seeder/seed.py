import flow.auth as flow_auth
from seeder.form import form_seeder
from seeder.datapoint import datapoint_seeder


token = flow_auth.get_token()
form_seeder(token=token)
datapoint_seeder(token=token)
