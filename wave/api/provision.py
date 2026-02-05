from pathlib import Path
import subprocess

class Provision:
    def __init__(self, script_dir: Path):
        self.__script_dir = str(script_dir)

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
        # Start the environment (Docker or Vagrant)
        command = "vagrant up" if platform == "vm" else "docker compose up -d"
        return self.execute_command(command)

    def down(self, platform):
        # Destroy the environment (Docker or Vagrant)
        command = "vagrant destroy -f" if platform == "vm" else "docker compose down"
        return self.execute_command(command)

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