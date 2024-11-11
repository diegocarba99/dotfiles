import subprocess
import platform
import os
import argparse

def print_banner():
    print("""
       .--,--.
       `.  ,.'
        |___|           ___       __               _            
        :o o:   O      / _ |__ __/ /____      ____(_)______ ____
       _`~^~'_  |     / __ / // / __/ _ \    / __/ / __/ -_/ __/
     /'   ^   `\=)   /_/ |_\_,_/\__/\___/   /_/ /_/\__/\__/_/   
   .'  _______ '~|
   `(<=|     |= /'   by diej99
       |     |
       |_____|
~~~~~~~ ===== ~~~~~~~~
""")


class Ricer:
    PACKAGES = ["i3", "rofi", "i3blocks", "zsh", "git", "fzf", "zoxide", "flameshot"]
    OFFENSIVE_TOOLS = [
        "kali-tools-database",
        "kali-tools-exploitation",
        "kali-tools-fuzzing",
        "kali-tools-forensics",
        "kali-tools-hardware",
        "kali-tools-identify",
        "kali-tools-information-gathering",
        "kali-tools-passwords",
        "kali-tools-post-exploitation",
        "kali-tools-respond",
        "kali-tools-reverse-engineering",
        "kali-tools-rfid",
        "kali-tools-vulnerability",
        "kali-tools-web",
        "kali-tools-windows-resources",
    ]
    OS_UBUNTU = "ubuntu"
    OS_DEBIAN = "debian"
    OS_KALI = "kali linux"
    OS_UNKNOWN = "unknown"
    CONFIG_DIR = os.path.expanduser("~/.config-test")
    HOME_DIR = os.path.expanduser("~")
    SOURCE_CONFIG = "./files/config-files/*"
    SOURCE_STANDALONE_CONFIG = "files/standlone-config-files/."

    def __init__(self):
        self.args = self.parse_args()
        self.os_type = self.get_os_type()

    def update_system(self):
        try:
            self.info("updating system")
            subprocess.check_call(["sudo", "apt-get", "update"])
            self.info("system updated successfully.")
        except subprocess.CalledProcessError as e:
            self.error(f"an error occurred during system update: {e}")
        except Exception as e:
            self.error(f"an unknown error occurred: {e}")

    def install_packages(self):
        try:
            self.info("installing packages: " + ", ".join(self.PACKAGES))
            subprocess.check_call(["sudo", "apt-get", "install", "-y"] + self.PACKAGES)
            self.info("package installation completed successfully")
        except subprocess.CalledProcessError as e:
            self.error(f"an error occurred during installation: {e}")
        except Exception as e:
            self.error(f"an unknown error occurred: {e}")

    def set_default_shell(self):
        try:
            self.info("setting ZSH as default shell. root password required to run chsh command")
            zsh_path = subprocess.check_output(["which", "zsh"]).decode().strip()
            subprocess.check_call(["chsh", "-s", zsh_path])
            self.success("default shell set to ZSH successfully.")
        except subprocess.CalledProcessError as e:
            self.error(f"an error occurred during setting default shell: {e}")
        except Exception as e:
            self.error(f"an unknown error occurred: {e}")

    def get_os_type(self):
        os_type = platform.system().lower()
        if os_type == "linux":
            try:
                with open("/etc/os-release") as f:
                    os_info = f.read().lower()
                    if "ubuntu" in os_info:
                        self.info(f"detected OS type: {self.OS_UBUNTU}")
                        return self.OS_UBUNTU
                    elif "debian" in os_info:
                        self.info(f"detected OS type: {self.OS_UBUNTU}")
                        return self.OS_DEBIAN
                    elif "kali" in os_info:
                        self.info(f"detected OS type: {self.OS_KALI}")
                        return self.OS_KALI
            except FileNotFoundError:
                self.error("could not determine the Linux distribution.")
        return self.OS_UNKNOWN

    def copy_config_files(self):
        try:
            self.info("copying configuration files")
            if not os.path.exists(os.path.expanduser(self.CONFIG_DIR)):
                self.info(f"no {self.CONFIG_DIR} directory found. creating configuration directory")
                os.makedirs(os.path.expanduser(self.CONFIG_DIR))
            if not os.path.exists(self.SOURCE_CONFIG.rstrip('*')):
                self.error(f"source configuration directory {self.SOURCE_CONFIG} does not exist. Check the configuration.")
                return
            # This is dirty as fuck, but idk why python complains too much when trying to do this using subprocess.check_call()
            # like this: subprocess.check_call(["cp", "-r", SOURCE_CONFIG, CONFIG_DIR])
            os.system(f"cp -r {self.SOURCE_CONFIG} {self.CONFIG_DIR}")
            os.system(f"cp -r {self.SOURCE_STANDALONE_CONFIG} {self.HOME_DIR}")
            self.success("configuration files copied successfully.")
        except subprocess.CalledProcessError as e:
            self.error(f"an error occurred during copying: {e}")
        except Exception as e:
            self.error(f"an unknown error occurred: {e}")


    def install_nerd_fonts(self):
        fonts = [
            "Noto",
        ]
        self.info("install nerd fonts")
        version = "2.1.0"
        fonts_dir = os.path.expanduser("~/.local/share/fonts")
        for font in fonts:
            self.info(f"checking if font {font} is already installed.")
            if any(font in file for file in os.listdir(fonts_dir)):
                self.success(f"font {font} is already installed. Skipping download.")
                return
        if not os.path.exists(fonts_dir):
            os.makedirs(fonts_dir)

        for font in fonts:
            zip_file = f"{font}.zip"
            download_url = f"https://github.com/ryanoasis/nerd-fonts/releases/download/v{version}/{zip_file}"
            self.info(f"downloading {download_url}")
            try:
                subprocess.check_call(["wget", download_url])
                subprocess.check_call(["unzip", zip_file, "-d", fonts_dir])
                os.remove(zip_file)
            except subprocess.CalledProcessError as e:
                self.error(f"an error occurred during downloading or extracting {zip_file}: {e}")
            except Exception as e:
                self.error(f"an unknown error occurred: {e}")

        try:
            subprocess.check_call(["find", fonts_dir, "-name", "*Windows Compatible*", "-delete"])
            subprocess.check_call(["fc-cache", "-fv"])
            self.success("nerd fonts installed successfully.")
        except subprocess.CalledProcessError as e:
            self.error(f"an error occurred during font cache update: {e}")
        except Exception as e:
            self.error(f"an unknown error occurred: {e}")

    def install_offensive_tools(self):
        try:
            self.info("installing offensive tools" + ", ".join(self.OFFENSIVE_TOOLS))
            subprocess.check_call(['sudo', 'sh', '-c', 'echo "deb http://http.kali.org/kali kali-rolling main contrib non-free" > /etc/apt/sources.list.d/kali.list'])
            subprocess.check_call(['wget', '-q', '-O', '-', 'https://archive.kali.org/archive-key.asc'], stdout=subprocess.PIPE)
            subprocess.check_call(['sudo', 'apt-key', 'add', '-'], stdin=subprocess.PIPE)
            self.update_system()
            subprocess.check_call(["sudo", "apt-get", "install", "-y"] + self.OFFENSIVE_TOOLS)
            self.success("offensive tools installed successfully.")
        except subprocess.CalledProcessError as e:
            self.error(f"an error occurred during installation: {e}")
        except Exception as e:
            self.error(f"an unknown error occurred: {e}")

    def info(self, msg: str):
        if self.args.verbose:
            print(f"\033[1;34m[i] {msg} \033[0m")

    def error(self, msg: str):
        print(f"\033[1;31m[i] {msg} \033[0m")

    def success(self, msg: str):
        print(f"\033[1;32m[i] {msg} \033[0m")

    def parse_args(self):
        parser = argparse.ArgumentParser(description="automate the installation of the i3wm rice.")
        parser.add_argument("--no-install-offensive-tools", action="store_true", help="install the suite of offensive tools.")
        parser.add_argument("--no-install-packages", action="store_true", help="install the suite of offensive tools.")
        parser.add_argument("--verbose", action="store_true", help="increase output verbosity.")
        parser.add_argument("--bannerless", action="store_true", help="avoid printing the banner.")
        return parser.parse_args()
    
    def cook(self):
        print_banner() if not self.args.bannerless else None
        self.parse_args()
        self.update_system() if not self.args.no_install_packages else None
        self.install_packages() if not self.args.no_install_packages else None
        self.install_nerd_fonts() if not self.args.no_install_packages else None
        self.set_default_shell()
        self.copy_config_files()
        self.install_offensive_tools() if self.os_type != self.OS_KALI and not self.args.install_offensive_tools else None
        self.success("installation completed")


if __name__ == "__main__":

    ricer = Ricer()
    ricer.cook()
