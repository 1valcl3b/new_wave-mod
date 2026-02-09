import os
import requests
from flask import render_template, request, redirect
from flask import abort, flash
from pathlib import Path
from dotenv import load_dotenv
from provision.confYaml import ConfYaml



def configure(app):

    path_app = Path(os.path.abspath("app"))
    conf_yaml = ConfYaml()
    load_dotenv()

    IP_HOST_API = os.environ.get("IP_HOST_API")
    URL_API = f"http://{IP_HOST_API}:8181/provision"
    URL_GRAFANA = f"http://{IP_HOST_API}:3000"

    @app.route('/', methods=["GET", "POST"])
    def index():
        value = "Configurator - WAVE"

        if request.method == "GET":
            return render_template("index.html", value=value)
        else:
            conf = f"""\
---
- traffic: server
  ip: "{request.form.get("ipserver")}"
  ram: "{request.form.get('memserver')}"
  vcpu: "{request.form.get('cpuserver')}"
  platform: {request.form.get('plafmserver')}

- traffic: client
  ip: "{request.form.get("ipclient")}"
  ram: "{request.form.get('memclient')}"
  vcpu: "{request.form.get('cpuclient')}"
  platform: {request.form.get('plafmclient')}

"""

            # bloco mininet
            topology_type = request.form.get("topology-type")
            delay = request.form.get("delay")

            conf_topology = f"""           
- topology:
    type: "{topology_type}"
"""

            
            if topology_type == "tree":
                conf_topology += f"""\
    depth: "{request.form.get('depth')}"
    branching: "{request.form.get('branching')}"
    max_switches: "{request.form.get('switchs')}"
"""

            
            elif topology_type == "linear":
                conf_topology += f"""\
    num_switches: "{request.form.get('linear_switchs')}"
"""
            
            if delay and delay.isdigit() and int(delay) > 0:
                conf_topology += f"""\
    delay: "{delay}"
"""

        if (request.form.get('select-model') == 'sin'):

            conf_model_sin = f"""\
- model: {request.form.get('select-model')}
  a: "{request.form.get('amp-sin')}"
  p: "{request.form.get('ped-sin')}"
  d: "{request.form.get('drn-sin')}"
  l: "{request.form.get('lmd-sin')}"
  microburst: "{request.form.get('microburst', 'off')}"
"""
            conf_yaml.set_conf(conf + conf_topology)
            conf_yaml.set_conf_model(conf + conf_model_sin + conf_topology)

        elif (request.form.get('select-model') == 'flashc'):

            conf_model_flashc = f"""\
- model: {request.form.get('select-model')}
  nl: "{request.form.get('nload-flashc')}"
  sl: "{request.form.get('shkl-flashc')}"
  crd: "{request.form.get('constrp-flashc')}"
  microburst: "{request.form.get('microburst', 'off')}"
"""
            conf_yaml.set_conf(conf + conf_topology)
            conf_yaml.set_conf_model(conf + conf_model_flashc + conf_topology) 
        elif (request.form.get('select-model') == 'step'):

            conf_model_step = f"""\
- model: {request.form.get('select-model')}
  i: "{request.form.get('itvl-step')}"
  j: "{request.form.get('jmp-step')}"
  d: "{request.form.get('drn-step')}"
  microburst: "{request.form.get('microburst', 'off')}"
"""
            conf_yaml.set_conf(conf + conf_topology)
            conf_yaml.set_conf_model(conf + conf_model_step + conf_topology)
        else:
            conf_yaml.set_conf(conf + conf_topology)

        return redirect('/config')

    # Render page with the configuration result to provision the environment

    @app.route('/config')
    def config_result():
        config_yaml_dir = Path(path_app, "provision", "config.yaml")
        try:
            with open(config_yaml_dir, "w") as f:
                conf = conf_yaml.get_conf()
                f.write(conf)
                return render_template('config-result.html',
                                       conf=conf_yaml.get_conf_model())

        except FileNotFoundError:
            value = "Failed to generate the configuration file!"
            return render_template('default.html', value=value)
        except (AttributeError, TypeError) as value:
            value = """The configuration for provisioning was not completed,
        return to the Home page to set up the provisioning environment."""
            return render_template('default.html', value=value)

    # Requesting provisioning API

    @app.route('/up')
    def provision_up():
        try:
            conf_dict = conf_yaml.conf_model_dict()
            pl = conf_dict[0]['platform']
            resquest = requests.get(f"{URL_API}/up?pl={pl}")
            res_result = resquest.json()
            

            if 'error' in res_result:
                abort(404)

            elif res_result["provision"] == "up":
                flash("Provisioning successful!", "success")
                return redirect("/execute")

        except requests.exceptions.ConnectionError:
            flash("Connection API Fail!", "danger")
            return redirect('/config')

    @app.route('/down')
    def provision_down():
        try:
            conf_dict = conf_yaml.conf_model_dict()
            pl = conf_dict[0]['platform']
            resquest = requests.get(f"{URL_API}/down?pl={pl}")
            res_result = resquest.json()
    

            if 'error' in res_result:
                abort(404)
            elif res_result["provision"] == "down":

                flash("Environment destroyed successfully!", "success")

                return redirect('/')

        except requests.exceptions.ConnectionError:
            flash("Connection API Fail!", "error")
            return redirect('/results')

    @app.route('/execute')
    def execute_scenario():

        try:
            conf_dict = conf_yaml.conf_model_dict()

            if conf_dict[2]['microburst'] == 'on':
                server_ip = conf_dict[0]["ip"]
                d = conf_dict[2].get('d') if conf_dict[2]['model'] != 'flashc' else "10"
                pl = conf_dict[0]['platform']
                requests.get(f"{URL_API}/execute/microburst?server_ip={server_ip}&d={d}&pl={pl}")

            if conf_dict[2]['model'] == 'sin':
                a = conf_dict[2]['a']
                p = conf_dict[2]['p']
                d = conf_dict[2]['d']
                l = conf_dict[2]['l']
                pl = conf_dict[0]['platform']
                resquest = requests.get(
                    f"{URL_API}/execute/model/sin?a={a}&p={p}&d={d}&l={l}&pl={pl}")
                res_result = resquest.json()

            if conf_dict[2]['model'] == 'flashc':
                nl = conf_dict[2]['nl']
                sl = conf_dict[2]['sl']
                crd = conf_dict[2]['crd']
                pl = conf_dict[0]['platform']
                resquest = requests.get(
                    f"{URL_API}/execute/model/flashc?nl={nl}&sl={sl}&crd={crd}&pl={pl}")
                res_result = resquest.json()

            if conf_dict[2]["model"] == "step":
                i = conf_dict[2]['i']
                j = conf_dict[2]['j']
                d = conf_dict[2]['d']
                pl = conf_dict[0]['platform']
                resquest = requests.get(
                    f"{URL_API}/execute/model/step?i={i}&j={j}&d={d}&pl={pl}")
                res_result = resquest.json()

            if 'error' in res_result:
                abort(404)
            elif res_result["provision"] == "executed":
                return redirect("/results")
        except requests.exceptions.ConnectionError:
            flash("Connection API Fail!", "danger")
            return redirect('/config')

    @app.route('/results')
    def analysis_result():
        try:
            conf_dict = conf_yaml.conf_model_dict()
            platform_option = conf_dict[0]['platform']
            if conf_dict[2]['model'] == 'sin':
                model = 'sinusoid'
            elif conf_dict[2]['model'] == 'flashc':
                model = 'flashcrowd'
            else:
                model = 'stair_step'
            resquest_gr = requests.get(
                f"""{URL_API}/grafana/config?host_promts={conf_dict[0]['ip']}&wave_model={model}&platform={platform_option}""")

            config_gr = resquest_gr.json()

            dashboard_uid = config_gr['dashboardUid']

            if 'error' in config_gr:
                abort(404)

            return render_template('analysis-result.html',
                                   url_grafana=URL_GRAFANA,
                                   dashboard_uid=dashboard_uid,
                                   platform=platform_option)

        except requests.exceptions.ConnectionError:
            flash("Connection API Fail!", "danger")
            return redirect('/config')
        except AttributeError:
            value = """The configuration for provisioning was not completed,
        return to the Home page to set up the provisioning environment."""
            return render_template('default.html', value=value)

    @app.errorhandler(404)
    def not_found(error):
        value = error
        return render_template('default.html', value=value), 404
