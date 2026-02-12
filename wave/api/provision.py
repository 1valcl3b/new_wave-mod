from pathlib import Path
import subprocess
import time
import yaml

class Provision:
    def __init__(self, script_dir: Path):
        self.__script_dir = str(script_dir)
    
    def get_topology_type(self):
        config_path = Path(self.get_script_dir()) / "config.yaml"
        try:
            with open(config_path, "r") as f:
                data = yaml.safe_load(f)
            
            for item in data:
                if "topology" in item:
                    return item["topology"].get("type")

        except Exception as e:
            print(f"[WAVE] Error reading topology: {e}")

        return None

    # Auxiliary functions for provisioning the mininet environment

    def start_mininet(self, topology_type):
        switch_file = Path("/tmp/ultimo_switch.txt")
        switch_file.unlink(missing_ok=True)

        script = Path(self.get_script_dir()) / "mininet_up.sh"
        subprocess.Popen(["bash", str(script), topology_type])

    def wait_mininet_ready(self, timeout=60):
        switch_file = Path("/tmp/ultimo_switch.txt")
        start = time.time()

        while not switch_file.exists():
            if time.time() - start > timeout:
                raise RuntimeError("Mininet startup timeout")
            time.sleep(1)
    
    def stop_mininet(self):
        script = Path(self.get_script_dir()) / "mininet_down.sh"
        
        subprocess.Popen(["bash", str(script)])
    
    ## ///

    def get_script_dir(self):
        return self.__script_dir

    def set_script_dir(self, setPath):
        self.__script_dir = setPath

    def execute_command(self, command):
        try:
            result = subprocess.Popen(
                f"cd {self.get_script_dir()}; {command}",
                shell=True, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            return
            # return result.stdout.decode()
        except subprocess.CalledProcessError as e:
            return
            # return e.stderr.decode()

    def up(self, platform):
        # Start the environment (Docker or Vagrant and Mininet)

        topology_type = self.get_topology_type()
        
        if topology_type in ["tree", "linear"]:
            self.start_mininet(topology_type)
            self.wait_mininet_ready()
        
        command = "vagrant up" if platform == "vm" else "docker compose up -d"
        return self.execute_command(command)

    def down(self, platform):
        # Destroy the environment (Docker or Vagrant and Mininet)
        command = "vagrant destroy -f" if platform == "vm" else "docker compose down"
        self.execute_command(command)

        time.sleep(30)    
        self.stop_mininet()

    def execute_scenario(self, *args):
        # Execute scenarios based on user input
        if args[1] == "docker":
            if args[0] == 'sin':
                command = f"""docker exec -it client ./run_wave.sh -l sinusoid {args[2]} {args[3]} {args[4]} {args[5]}"""
            elif args[0] == "step":
                command = f"""docker exec -it client ./run_wave.sh -l stair_step {args[2]} {args[3]} {args[4]}"""
            elif args[0] == "flashc":
                command = f"""docker exec -it client ./run_wave.sh -l flashcrowd {args[2]} {args[3]} {args[4]}"""
            else:
                return "Invalid scenario. Use: 'sin', 'step' or 'flashc'."
        else:
            if args[0] == 'sin':
                command = f"""vagrant ssh client -c './wave/run_wave.sh -l sinusoid {args[2]} {args[3]} {args[4]} {args[5]}'"""
            elif args[0] == "step":
                command = f"""vagrant ssh client -c './wave/run_wave.sh -l stair_step {args[2]} {args[3]} {args[4]}'"""
            elif args[0] == "flashc":
                command = f"""vagrant ssh client -c './wave/run_wave.sh -l flashcrowd {args[2]} {args[3]} {args[4]}'"""
            else:
                return "Invalid scenario. Use: 'sin', 'step' or 'flashc'."
        return self.execute_command(command)
    
    def run_microburst(self, *args):
        if args[0] == "docker":
            command = f"""docker exec -it client 'sudo ./run_microburst.sh -l {args[1]} {args[2]}'"""
        else:
            command = f"""vagrant ssh client -c './wave/run_microburst.sh -l {args[1]} {args[2]}'"""

        return self.execute_command(command)