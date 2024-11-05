import subprocess
import platform
import os


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

def update_system():
    try:
        subprocess.check_call(["sudo", "apt-get", "update"])
        success("System updated successfully.")
    except subprocess.CalledProcessError as e:
        error(f"An error occurred during system update: {e}")
    except Exception as e:
        error(f"An unknown error occurred: {e}")

def install_packages():
    try:
        subprocess.check_call(["sudo", "apt-get", "install", "-y"] + PACKAGES)
        print("Installation completed successfully.")
    except subprocess.CalledProcessError as e:
        error(f"An error occurred during installation: {e}")
    except Exception as e:
        error(f"An unknown error occurred: {e}")

def set_default_shell():
    try:
        zsh_path = subprocess.check_output(["which", "zsh"]).decode().strip()
        subprocess.check_call(["chsh", "-s", zsh_path])
        success("Default shell set to ZSH successfully.")
    except subprocess.CalledProcessError as e:
        error(f"An error occurred during setting default shell: {e}")
    except Exception as e:
        error(f"An unknown error occurred: {e}")

def get_os_type():
    os_type = platform.system().lower()
    if os_type == "linux":
        try:
            with open("/etc/os-release") as f:
                os_info = f.read().lower()
                if "ubuntu" in os_info:
                    return OS_UBUNTU
                elif "debian" in os_info:
                    return OS_DEBIAN
                elif "kali" in os_info:
                    return OS_KALI
        except FileNotFoundError:
            error("Could not determine the Linux distribution.")
    return OS_UNKNOWN

def copy_config_files():
    try:
        if not os.path.exists(os.path.expanduser(CONFIG_DIR)):
            info(f"no {CONFIG_DIR} directory found. creating configuration directory")
            os.makedirs(os.path.expanduser(CONFIG_DIR))
        if not os.path.exists(SOURCE_CONFIG.rstrip('*')):
            error(f"Source configuration directory {SOURCE_CONFIG} does not exist. Check the configuration.")
            return
        # This is dirty as fuck, but idk why python complains too much when trying to do this using subprocess.check_call()
        # like this: subprocess.check_call(["cp", "-r", SOURCE_CONFIG, CONFIG_DIR])
        os.system(f"cp -r {SOURCE_CONFIG} {CONFIG_DIR}")
        os.system(f"cp -r {SOURCE_STANDALONE_CONFIG} {HOME_DIR}")
        success("configuration files copied successfully.")
    except subprocess.CalledProcessError as e:
        error(f"an error occurred during copying: {e}")
    except Exception as e:
        error(f"an unknown error occurred: {e}")


def install_nerd_fonts():
    fonts = [
        "Noto",
    ]
    version = "2.1.0"
    fonts_dir = os.path.expanduser("~/.local/share/fonts")
    for font in fonts:
        info(f"Checking if font {font} is already installed.")
        if any(font in file for file in os.listdir(fonts_dir)):
            success(f"Font {font} is already installed. Skipping download.")
            return
    if not os.path.exists(fonts_dir):
        os.makedirs(fonts_dir)

    for font in fonts:
        zip_file = f"{font}.zip"
        download_url = f"https://github.com/ryanoasis/nerd-fonts/releases/download/v{version}/{zip_file}"
        info(f"Downloading {download_url}")
        try:
            subprocess.check_call(["wget", download_url])
            subprocess.check_call(["unzip", zip_file, "-d", fonts_dir])
            os.remove(zip_file)
        except subprocess.CalledProcessError as e:
            error(f"An error occurred during downloading or extracting {zip_file}: {e}")
        except Exception as e:
            error(f"An unknown error occurred: {e}")

    try:
        subprocess.check_call(["find", fonts_dir, "-name", "*Windows Compatible*", "-delete"])
        subprocess.check_call(["fc-cache", "-fv"])
        success("Nerd fonts installed successfully.")
    except subprocess.CalledProcessError as e:
        error(f"An error occurred during font cache update: {e}")
    except Exception as e:
        error(f"An unknown error occurred: {e}")

def install_offensive_tools():
    try:
        subprocess.check_call(['sudo', 'sh', '-c', 'echo "deb http://http.kali.org/kali kali-rolling main contrib non-free" > /etc/apt/sources.list.d/kali.list'])
        subprocess.check_call(['wget', '-q', '-O', '-', 'https://archive.kali.org/archive-key.asc'], stdout=subprocess.PIPE)
        subprocess.check_call(['sudo', 'apt-key', 'add', '-'], stdin=subprocess.PIPE)
        update_system()
        subprocess.check_call(["sudo", "apt-get", "install", "-y"] + OFFENSIVE_TOOLS)
        success("Offensive tools installed successfully.")
    except subprocess.CalledProcessError as e:
        error(f"An error occurred during installation: {e}")
    except Exception as e:
        error(f"An unknown error occurred: {e}")

def info(msg: str):
    print(f"\033[1;34m[i] {msg} \033[0m")

def error(msg: str):
    print(f"\033[1;31m[i] {msg} \033[0m")

def success(msg: str):
    print(f"\033[1;32m[i] {msg} \033[0m")

def get_input(msg: str):
    return input(f"\033[1;35m[i] {msg} \033[0m")


if __name__ == "__main__":
    
    info("starting installation")

    info("updating system")
    update_system()

    os_type = get_os_type()
    info(f"detected OS type: {os_type}")

    info("installing packages: " + ", ".join(PACKAGES))
    install_packages()

    info("install nerd fonts")
    install_nerd_fonts()

    info("setting ZSH as default shell. root password required to run chsh command")
    set_default_shell()

    info("copying configuration files")
    copy_config_files()

    if os_type != OS_KALI:
        choice = get_input("Do you want to install the suite of offensive tools? This will take a while (y/n)")
        if choice.lower() == "y":
            info("installing offensive tools" + ", ".join(OFFENSIVE_TOOLS))
            install_offensive_tools()

    info("installation completed")