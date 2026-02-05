from provision import Provision
from flask import Flask
from flask_restx import Resource, Api, reqparse
from conf_grafana import generateAPIKey, createDataSources, createDashboard
from paths import config_dir
import time

app = Flask(__name__)
api = Api(app, version='1.0', title='LoadGen API',
          description='Provision API LoadGen',
          default='API', default_label='Default namespace')

pro_env = Provision(config_dir)

parser_up = reqparse.RequestParser()
parser_up.add_argument('pl', type=str, help='Platform')

parser_down = reqparse.RequestParser()
parser_down.add_argument('pl', type=str, help='Platform')

parser_mb = reqparse.RequestParser()
parser_mb.add_argument('pl', type=str, help='Platform')
parser_mb.add_argument('server_ip', type=str, help='Server IP')
parser_mb.add_argument('d', type=str, help='Duration')


parser_sin = reqparse.RequestParser()
parser_sin.add_argument('pl', type=str, help='Platform')
parser_sin.add_argument('a', type=str, help='Sinusoid - Amplitude')
parser_sin.add_argument('p', type=str, help='Sinusoid - Period')
parser_sin.add_argument('d', type=str, help='Sinusoid - Duration')
parser_sin.add_argument('l', type=str, help='Sinusoid - Lambd')

parser_flashc = reqparse.RequestParser()
parser_flashc.add_argument('pl', type=str, help='Platform')
parser_flashc.add_argument('nl', type=str, help='Flashcrowd - Normal Load')
parser_flashc.add_argument('sl', type=str, help='Flashcrowd - Shock Level')
parser_flashc.add_argument('crd', type=str, help='Flashcrowd - Const RanpDown')

parser_step = reqparse.RequestParser()
parser_step.add_argument('pl', type=str, help='Platform')
parser_step.add_argument('i', type=str, help='Step - Interval')
parser_step.add_argument('j', type=str, help='Step - Jump')
parser_step.add_argument('d', type=str, help='Step - Duration')


parser_config_grafana = reqparse.RequestParser()
parser_config_grafana.add_argument(
    'host_promts', type=str, help='IP Host runner Promethues')
parser_config_grafana.add_argument(
    'wave_model', type=str, help='Wave model')
parser_config_grafana.add_argument(
    'platform', type=str, help='Platform')


@api.route('/provision/up')
class ProvisionInit(Resource):
    @api.doc(parser=parser_up)
    def get(self):
        args = parser_up.parse_args()
        pro_env.up(args['pl'])

        while not config_dir.joinpath('logs/ready.txt').exists():
            time.sleep(2)

        return {'provision': 'up'}


@api.route('/provision/grafana/config')
class ProvisionGrafana(Resource):
    @api.doc(parser=parser_config_grafana)
    def get(self):
        # conf Grafana
        host_promts = parser_config_grafana.parse_args()['host_promts']
        wave_model = parser_config_grafana.parse_args()['wave_model']
        platform = parser_config_grafana.parse_args()['platform']
        
        PROMETHEUS_IP= "192.168.56.11"
        prometheus_url = PROMETHEUS_IP if platform == "vm" else "prometheus"

        api_key = generateAPIKey.create_api_key_grf()

        promts_data_src_uid = createDataSources.create_data_src(
            f'http://{prometheus_url}:9090', api_key, 'prometheus')['uid']

        csv_data_src_uid = createDataSources.create_data_src(
            f'/var/lib/grafana/csv/{wave_model}_wave.csv',
            api_key, 'csv')['uid']

        dashboard_uid = createDashboard.create_dashboard(
            api_key, promts_data_src_uid, csv_data_src_uid, platform)

        response = {
            'provision': 'executed',
            'apiKey': api_key,
            'promtsDataSrcUid': promts_data_src_uid,
            'CSVDataSrcUid': csv_data_src_uid,
            'dashboardUid': dashboard_uid
        }

        return response


@api.route('/provision/down')
class ProvisionDestroy(Resource):
    @api.doc(parser=parser_down)
    def get(self):
        args = parser_down.parse_args()
        pro_env.down(args['pl'])
        time.sleep(2) # wait for the vms or containers to be destroyed

        for log_file in config_dir.joinpath('logs').iterdir():
            log_file.unlink()

        return {'provision': 'down'}

@api.route('/provision/execute/microburst')
class ProvisionExecuteMicroBurst(Resource):
    @api.doc(parser=parser_mb)
    def get(self):
        args = parser_mb.parse_args()
        pro_env.run_microburst(args['pl'], args['server_ip'], args['d'])

        return {'provision': 'executed'}

@api.route('/provision/execute/model/sin')
class ProvisionExcuteScenarioSin(Resource):
    @api.doc(parser=parser_sin)
    def get(self):
        args = parser_sin.parse_args()
        pro_env.execute_scenario(
            'sin', args['pl'],args['a'], args['p'], args['d'], args['l'])

        return {'provision': 'executed'}


@api.route('/provision/execute/model/flashc')
class ProvisionExcuteScenarioFlashc(Resource):
    @api.doc(parser=parser_flashc)
    def get(self):
        args = parser_flashc.parse_args()
        pro_env.execute_scenario('flashc', args['pl'], args['nl'], args['sl'], args['crd'])
        return {'provision': 'executed'}

@api.route('/provision/execute/model/step')
class ProvisionExcuteScenarioStep(Resource):
    @api.doc(parser=parser_step)
    def get(self):
        args = parser_step.parse_args()
        pro_env.execute_scenario('step', args['pl'], args['i'], args['j'], args['d'])
        return {'provision': 'executed'}


@app.errorhandler(404)
def not_found(error):
    return {'error': 'Not found'}, 404


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8181)